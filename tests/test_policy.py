import pytest

from bridle.policy import PolicyDenied, decide, require


def test_allowlisted_ping() -> None:
    d = decide("ping")
    assert d.allowed is True


def test_deny_unknown_tool() -> None:
    d = decide("rm_rf")
    assert d.allowed is False
    with pytest.raises(PolicyDenied):
        require("rm_rf")


def test_mail_tools_allowlisted() -> None:
    for tool in ("mail_account_list", "mail_header_list", "mail_header_view"):
        assert decide(tool).allowed is True
