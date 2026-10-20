"""Mail allowlist configuration (accounts, mailboxes, sender globs)."""

from __future__ import annotations

import fnmatch
import os
import re
import tomllib
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from bridle.policy import PolicyDenied


class MailError(RuntimeError):
    """Raised for mail configuration or credential failures."""


_EMAIL_IN_ANGLE = re.compile(r"<([^>]+)>")
_DEFAULT_MAX_LIST = 50
_MAX_LIST_CAP = 200


@dataclass(frozen=True)
class MailAccount:
    id: str
    host: str
    username: str
    password_env: str
    port: int = 993
    use_ssl: bool = True
    allowed_mailboxes: tuple[str, ...] = ()
    allowed_from: tuple[str, ...] = ()
    max_list: int = _DEFAULT_MAX_LIST


@dataclass(frozen=True)
class MailConfig:
    accounts: dict[str, MailAccount] = field(default_factory=dict)

    def account(self, account_id: str) -> MailAccount:
        if account_id not in self.accounts:
            raise PolicyDenied(
                f"mail account {account_id!r} is not allowlisted "
                "(or mail is not configured)"
            )
        return self.accounts[account_id]


def default_config_path() -> Path:
    configured = os.environ.get("BRIDLE_MAIL_CONFIG", "").strip()
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".bridle" / "mail.toml"


def _as_str_list(value: Any, *, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
        raise ValueError(f"{field_name} must be a list of strings")
    return tuple(x.strip() for x in value if x.strip())


def _parse_account(raw: dict[str, Any]) -> MailAccount:
    account_id = str(raw.get("id", "")).strip()
    if not account_id:
        raise ValueError("each [[accounts]] entry needs a non-empty id")
    host = str(raw.get("host", "")).strip()
    username = str(raw.get("username", "")).strip()
    password_env = str(raw.get("password_env", "")).strip()
    if not host or not username or not password_env:
        raise ValueError(
            f"account {account_id!r} needs host, username, and password_env"
        )
    port = int(raw.get("port", 993))
    use_ssl = bool(raw.get("use_ssl", True))
    mailboxes = _as_str_list(raw.get("allowed_mailboxes"), field_name="allowed_mailboxes")
    if not mailboxes:
        raise ValueError(
            f"account {account_id!r} needs a non-empty allowed_mailboxes list"
        )
    allowed_from = _as_str_list(raw.get("allowed_from"), field_name="allowed_from")
    max_list = int(raw.get("max_list", _DEFAULT_MAX_LIST))
    if max_list < 1:
        raise ValueError(f"account {account_id!r} max_list must be >= 1")
    max_list = min(max_list, _MAX_LIST_CAP)
    return MailAccount(
        id=account_id,
        host=host,
        username=username,
        password_env=password_env,
        port=port,
        use_ssl=use_ssl,
        allowed_mailboxes=mailboxes,
        allowed_from=allowed_from,
        max_list=max_list,
    )


def load_config_from_toml(text: str) -> MailConfig:
    data = tomllib.loads(text)
    raw_accounts = data.get("accounts", [])
    if raw_accounts is None:
        raw_accounts = []
    if not isinstance(raw_accounts, list):
        raise ValueError("accounts must be a list of tables")
    accounts: dict[str, MailAccount] = {}
    for item in raw_accounts:
        if not isinstance(item, dict):
            raise ValueError("each account must be a table")
        account = _parse_account(item)
        if account.id in accounts:
            raise ValueError(f"duplicate mail account id {account.id!r}")
        accounts[account.id] = account
    return MailConfig(accounts=accounts)


def load_config(path: Path | None = None) -> MailConfig:
    """Load mail config from disk. Missing file → empty config (deny all)."""
    target = path or default_config_path()
    if not target.is_file():
        return MailConfig()
    return load_config_from_toml(target.read_text(encoding="utf-8"))


@lru_cache(maxsize=4)
def _cached_load(path_str: str, mtime_ns: int) -> MailConfig:
    return load_config(Path(path_str))


def get_config() -> MailConfig:
    """Load config with a light mtime cache (tests can clear via clear_config_cache)."""
    path = default_config_path()
    if not path.is_file():
        return MailConfig()
    stat = path.stat()
    return _cached_load(str(path.resolve()), stat.st_mtime_ns)


def clear_config_cache() -> None:
    _cached_load.cache_clear()


def extract_email_address(from_header: str | None) -> str | None:
    """Return a bare address from a From-style header, lowercased."""
    if not from_header or not from_header.strip():
        return None
    text = from_header.strip()
    angled = _EMAIL_IN_ANGLE.search(text)
    if angled:
        return angled.group(1).strip().lower()
    # Bare address
    if "@" in text and " " not in text:
        return text.lower()
    return text.lower()


def sender_allowed(account: MailAccount, from_header: str | None) -> bool:
    """True if sender passes allowed_from globs (empty list = any sender)."""
    if not account.allowed_from:
        return True
    address = extract_email_address(from_header)
    if address is None:
        return False
    return any(fnmatch.fnmatchcase(address, pat.lower()) for pat in account.allowed_from)


def require_mail_access(
    account_id: str,
    mailbox: str,
    *,
    from_header: str | None = None,
    config: MailConfig | None = None,
) -> MailAccount:
    """Deny unless account, mailbox, and optional sender are allowlisted."""
    cfg = config if config is not None else get_config()
    if not cfg.accounts:
        raise PolicyDenied(
            "mail is not configured "
            f"(create {default_config_path()} or set BRIDLE_MAIL_CONFIG)"
        )
    account = cfg.account(account_id)
    if mailbox not in account.allowed_mailboxes:
        raise PolicyDenied(
            f"mailbox {mailbox!r} is not allowlisted for account {account_id!r}"
        )
    if from_header is not None and not sender_allowed(account, from_header):
        raise PolicyDenied(
            f"sender not allowlisted for account {account_id!r}"
        )
    return account


def resolve_password(account: MailAccount) -> str:
    value = os.environ.get(account.password_env, "")
    if not value:
        raise MailError(
            f"mail password env {account.password_env!r} is unset for "
            f"account {account.id!r}"
        )
    return value
