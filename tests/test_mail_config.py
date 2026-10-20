import pytest

from bridle.mail_config import (
    MailError,
    extract_email_address,
    load_config_from_toml,
    require_mail_access,
    resolve_password,
    sender_allowed,
)
from bridle.policy import PolicyDenied

SAMPLE = """
[[accounts]]
id = "work"
host = "imap.example.com"
username = "me@example.com"
password_env = "BRIDLE_TEST_MAIL_PASS"
allowed_mailboxes = ["INBOX", "Archive"]
allowed_from = ["*@example.com", "boss@corp.test"]
max_list = 10
"""


def test_load_config_and_require_access() -> None:
    cfg = load_config_from_toml(SAMPLE)
    acct = require_mail_access("work", "INBOX", config=cfg)
    assert acct.host == "imap.example.com"
    with pytest.raises(PolicyDenied, match="not allowlisted"):
        require_mail_access("personal", "INBOX", config=cfg)
    with pytest.raises(PolicyDenied, match="mailbox"):
        require_mail_access("work", "Spam", config=cfg)


def test_unconfigured_denies() -> None:
    cfg = load_config_from_toml("")
    with pytest.raises(PolicyDenied, match="not configured"):
        require_mail_access("work", "INBOX", config=cfg)


def test_empty_mailboxes_rejected() -> None:
    bad = """
[[accounts]]
id = "work"
host = "imap.example.com"
username = "me@example.com"
password_env = "BRIDLE_TEST_MAIL_PASS"
allowed_mailboxes = []
"""
    with pytest.raises(ValueError, match="allowed_mailboxes"):
        load_config_from_toml(bad)


def test_sender_globs() -> None:
    cfg = load_config_from_toml(SAMPLE)
    acct = cfg.account("work")
    assert sender_allowed(acct, "Alice <alice@example.com>")
    assert sender_allowed(acct, "boss@corp.test")
    assert not sender_allowed(acct, "Eve <eve@evil.test>")
    assert extract_email_address("Name <a@b.c>") == "a@b.c"


def test_require_mail_access_checks_sender() -> None:
    cfg = load_config_from_toml(SAMPLE)
    require_mail_access(
        "work", "INBOX", from_header="Alice <alice@example.com>", config=cfg
    )
    with pytest.raises(PolicyDenied, match="sender"):
        require_mail_access(
            "work", "INBOX", from_header="Eve <eve@evil.test>", config=cfg
        )


def test_resolve_password(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = load_config_from_toml(SAMPLE)
    acct = cfg.account("work")
    monkeypatch.delenv("BRIDLE_TEST_MAIL_PASS", raising=False)
    with pytest.raises(MailError, match="unset"):
        resolve_password(acct)
    monkeypatch.setenv("BRIDLE_TEST_MAIL_PASS", "s3cret")
    assert resolve_password(acct) == "s3cret"
