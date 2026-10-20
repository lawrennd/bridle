"""Allowlisted IMAP adapter — headers / metadata only (REQ-0003 / CIP-0003)."""

from __future__ import annotations

import email
import fnmatch
import imaplib
import re
from email.header import decode_header, make_header
from email.message import Message
from typing import Any, Callable

from bridle.mail_config import (
    MailAccount,
    MailConfig,
    MailError,
    extract_email_address,
    get_config,
    require_mail_access,
    resolve_password,
    sender_allowed,
)
from bridle.policy import PolicyDenied, require

_MAX_HEADER_CHARS = 2048
_ID_SEP = "\x1f"

# Injected in tests.
_IMAP_FACTORY: Callable[..., imaplib.IMAP4] | None = None


def _decode_header_value(raw: str | None) -> str | None:
    if raw is None:
        return None
    try:
        decoded = str(make_header(decode_header(raw)))
    except Exception:
        decoded = raw
    if len(decoded) > _MAX_HEADER_CHARS:
        return decoded[:_MAX_HEADER_CHARS] + "…[truncated]"
    return decoded


def _headers_from_message(msg: Message) -> dict[str, str | None]:
    return {
        "from": _decode_header_value(msg.get("From")),
        "to": _decode_header_value(msg.get("To")),
        "cc": _decode_header_value(msg.get("Cc")),
        "bcc": _decode_header_value(msg.get("Bcc")),
        "subject": _decode_header_value(msg.get("Subject")),
        "date": _decode_header_value(msg.get("Date")),
        "message_id": _decode_header_value(msg.get("Message-ID")),
    }


def encode_message_id(account_id: str, mailbox: str, uid: str) -> str:
    if _ID_SEP in account_id or _ID_SEP in mailbox or _ID_SEP in uid:
        raise MailError("account, mailbox, and uid must not contain unit separator")
    return f"{account_id}{_ID_SEP}{mailbox}{_ID_SEP}{uid}"


def decode_message_id(message_id: str) -> tuple[str, str, str]:
    parts = message_id.split(_ID_SEP)
    if len(parts) != 3 or not all(parts):
        raise MailError("message_id must be an opaque id from mail_header_list")
    return parts[0], parts[1], parts[2]


def _connect(account: MailAccount) -> imaplib.IMAP4:
    password = resolve_password(account)
    factory = _IMAP_FACTORY
    try:
        if factory is not None:
            client = factory(account.host, account.port)
        elif account.use_ssl:
            client = imaplib.IMAP4_SSL(account.host, account.port)
        else:
            client = imaplib.IMAP4(account.host, account.port)
        client.login(account.username, password)
    except MailError:
        raise
    except Exception as exc:
        raise MailError(f"IMAP connect/login failed for {account.id!r}: {exc}") from exc
    return client


def _examine(client: imaplib.IMAP4, mailbox: str) -> None:
    typ, _ = client.select(mailbox, readonly=True)
    if typ != "OK":
        raise MailError(f"cannot EXAMINE mailbox {mailbox!r}")


def _uid_list(client: imaplib.IMAP4, limit: int) -> list[str]:
    typ, data = client.uid("SEARCH", None, "ALL")
    if typ != "OK" or not data or data[0] is None:
        return []
    uids = data[0].decode("ascii", errors="replace").split()
    if not uids:
        return []
    return uids[-limit:]


_UID_FETCH_RE = re.compile(rb"UID\s+(\d+)", re.IGNORECASE)


def _parse_uid_and_header(
    fetch_item: Any,
) -> tuple[str, dict[str, str | None]] | None:
    """Parse one IMAP UID FETCH response item into (uid, headers)."""
    if not isinstance(fetch_item, tuple) or len(fetch_item) < 2:
        return None
    meta, payload = fetch_item[0], fetch_item[1]
    if not isinstance(payload, (bytes, bytearray)):
        return None
    meta_b = meta if isinstance(meta, (bytes, bytearray)) else str(meta).encode()
    match = _UID_FETCH_RE.search(meta_b)
    if not match:
        return None
    uid = match.group(1).decode("ascii")
    msg = email.message_from_bytes(bytes(payload))
    return uid, _headers_from_message(msg)


def _fetch_headers(
    client: imaplib.IMAP4,
    uids: list[str],
) -> list[tuple[str, dict[str, str | None]]]:
    if not uids:
        return []
    typ, data = client.uid("FETCH", ",".join(uids), "(BODY.PEEK[HEADER] UID)")
    if typ != "OK" or not data:
        raise MailError("IMAP UID FETCH headers failed")
    out: list[tuple[str, dict[str, str | None]]] = []
    for item in data:
        parsed = _parse_uid_and_header(item)
        if parsed is not None:
            out.append(parsed)
    out.reverse()
    return out


def mail_account_list(*, config: MailConfig | None = None) -> dict[str, Any]:
    """Return allowlisted account ids only (no host/user secrets)."""
    require("mail_account_list")
    cfg = config if config is not None else get_config()
    if not cfg.accounts:
        return {
            "ok": True,
            "accounts": [],
            "note": "mail is not configured",
        }
    return {
        "ok": True,
        "accounts": [
            {
                "id": a.id,
                "mailboxes": list(a.allowed_mailboxes),
                "max_list": a.max_list,
            }
            for a in cfg.accounts.values()
        ],
    }


def mail_header_list(
    account: str,
    mailbox: str = "INBOX",
    limit: int | None = None,
    from_glob: str | None = None,
    *,
    config: MailConfig | None = None,
) -> dict[str, Any]:
    """List recent message headers for an allowlisted account/mailbox."""
    require("mail_header_list", account=account, mailbox=mailbox, limit=limit)
    acct = require_mail_access(account, mailbox, config=config)
    effective_limit = acct.max_list if limit is None else min(int(limit), acct.max_list)
    if effective_limit < 1:
        raise MailError("limit must be >= 1")

    client = _connect(acct)
    try:
        _examine(client, mailbox)
        uids = _uid_list(client, effective_limit)
        fetched = _fetch_headers(client, uids)
    finally:
        try:
            client.logout()
        except Exception:
            pass

    messages: list[dict[str, Any]] = []
    for uid, headers in fetched:
        if not sender_allowed(acct, headers.get("from")):
            continue
        if from_glob:
            addr = extract_email_address(headers.get("from"))
            if addr is None or not fnmatch.fnmatchcase(addr, from_glob.lower()):
                continue
        messages.append(
            {
                "id": encode_message_id(account, mailbox, uid),
                "account": account,
                "mailbox": mailbox,
                "uid": uid,
                **headers,
            }
        )

    return {"ok": True, "messages": messages, "count": len(messages)}


def mail_header_view(
    account: str,
    message_id: str,
    *,
    config: MailConfig | None = None,
) -> dict[str, Any]:
    """Fetch headers for one message by opaque id from mail_header_list."""
    require("mail_header_view", account=account, message_id=message_id)
    acct_id, mailbox, uid = decode_message_id(message_id)
    if acct_id != account:
        raise MailError("message_id account does not match account argument")
    acct = require_mail_access(account, mailbox, config=config)

    client = _connect(acct)
    try:
        _examine(client, mailbox)
        fetched = _fetch_headers(client, [uid])
    finally:
        try:
            client.logout()
        except Exception:
            pass

    if not fetched:
        raise MailError(f"message not found for id {message_id!r}")
    uid_got, headers = fetched[0]
    if not sender_allowed(acct, headers.get("from")):
        raise PolicyDenied(f"sender not allowlisted for account {account!r}")

    return {
        "ok": True,
        "message": {
            "id": encode_message_id(account, mailbox, uid_got),
            "account": account,
            "mailbox": mailbox,
            "uid": uid_got,
            **headers,
        },
    }
