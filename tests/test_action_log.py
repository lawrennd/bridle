from bridle import action_log


def test_redact_secrets_and_content_keys() -> None:
    logged = action_log._redact(
        {
            "password": "secret",
            "body": "should not log",
            "subject": "ok",
            "nested": {"authorization": "Bearer x", "from": "a@b.c"},
        }
    )
    assert logged["password"] == "***"
    assert logged["body"] == "***"
    assert logged["subject"] == "ok"
    assert logged["nested"]["authorization"] == "***"
    assert logged["nested"]["from"] == "a@b.c"


def test_truncate_long_strings() -> None:
    long = "x" * 1000
    logged = action_log._redact({"subject": long})
    assert logged["subject"].endswith("…[truncated]")
    assert len(logged["subject"]) < 600
