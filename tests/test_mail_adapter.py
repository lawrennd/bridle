from email.message import EmailMessage
from unittest.mock import MagicMock

import pytest

from bridle import mail_adapter
from bridle.mail_config import load_config_from_toml
from bridle.policy import PolicyDenied

SAMPLE = """
[[accounts]]
id = "work"
host = "imap.example.com"
username = "me@example.com"
password_env = "BRIDLE_TEST_MAIL_PASS"
allowed_mailboxes = ["INBOX"]
allowed_from = ["*@example.com"]
max_list = 5
"""


def _header_bytes(**fields: str) -> bytes:
    msg = EmailMessage()
    for key, value in fields.items():
        msg[key] = value
    return msg.as_bytes()


@pytest.fixture
def cfg():
    return load_config_from_toml(SAMPLE)


@pytest.fixture
def mock_imap(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BRIDLE_TEST_MAIL_PASS", "s3cret")
    client = MagicMock()
    client.select.return_value = ("OK", [b"1"])
    client.uid.side_effect = [
        ("OK", [b"10 11 12"]),
        (
            "OK",
            [
                (b"1 (UID 12 BODY[HEADER] {10}", _header_bytes(
                    From="Alice <alice@example.com>",
                    To="me@example.com",
                    Subject="Hello",
                    Date="Mon, 20 Oct 2026 12:00:00 +0000",
                    **{"Message-ID": "<one@example.com>"},
                )),
                (b"2 (UID 11 BODY[HEADER] {10}", _header_bytes(
                    From="Eve <eve@evil.test>",
                    Subject="Nope",
                )),
                (b"3 (UID 10 BODY[HEADER] {10}", _header_bytes(
                    From="Bob <bob@example.com>",
                    Subject="World",
                )),
                b")",
            ],
        ),
    ]
    client.logout.return_value = ("BYE", [])

    def factory(host: str, port: int):
        assert host == "imap.example.com"
        assert port == 993
        return client

    monkeypatch.setattr(mail_adapter, "_IMAP_FACTORY", factory)
    return client


def test_mail_account_list(cfg) -> None:
    result = mail_adapter.mail_account_list(config=cfg)
    assert result["ok"] is True
    assert result["accounts"][0]["id"] == "work"
    assert result["accounts"][0]["mailboxes"] == ["INBOX"]


def test_mail_header_list_filters_sender(cfg, mock_imap) -> None:
    result = mail_adapter.mail_header_list("work", mailbox="INBOX", config=cfg)
    assert result["ok"] is True
    assert result["count"] == 2
    subjects = {m["subject"] for m in result["messages"]}
    assert subjects == {"Hello", "World"}
    assert all("body" not in m for m in result["messages"])
    # readonly EXAMINE
    mock_imap.select.assert_called_with("INBOX", readonly=True)
    fetch_call = mock_imap.uid.call_args_list[1]
    assert "BODY.PEEK[HEADER]" in fetch_call.args[2]


def test_mail_header_list_denies_unknown_account(cfg) -> None:
    with pytest.raises(PolicyDenied):
        mail_adapter.mail_header_list("nope", config=cfg)


def test_mail_header_view(cfg, mock_imap, monkeypatch: pytest.MonkeyPatch) -> None:
    # Second call path: search unused; single uid fetch
    mock_imap.uid.side_effect = [
        (
            "OK",
            [
                (b"1 (UID 12 BODY[HEADER] {10}", _header_bytes(
                    From="Alice <alice@example.com>",
                    Subject="Hello",
                )),
            ],
        ),
    ]
    mid = mail_adapter.encode_message_id("work", "INBOX", "12")
    result = mail_adapter.mail_header_view("work", mid, config=cfg)
    assert result["ok"] is True
    assert result["message"]["subject"] == "Hello"
    assert "body" not in result["message"]


def test_from_glob_filter(cfg, mock_imap) -> None:
    result = mail_adapter.mail_header_list(
        "work",
        mailbox="INBOX",
        from_glob="bob@*",
        config=cfg,
    )
    assert result["count"] == 1
    assert result["messages"][0]["from"] == "Bob <bob@example.com>"
