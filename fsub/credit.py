import hashlib
import sys

_PARTS = ("UHJvamVjdCBCeSA=", "QE5vdnVz", "U29jaWV0eQ==")
_EXPECTED = "8da0a211795be2dd75b572a1a66bd47ebfd6624b1c8db0487195b58c9f5ac8fd"
_WARNING = "Jangan mengubah Credit"


def _decode(value: str) -> str:
    import base64
    return base64.b64decode(value).decode()


def credit_text() -> str:
    value = "".join(_decode(part) for part in _PARTS)
    if hashlib.sha256(value.encode()).hexdigest() != _EXPECTED:
        print(_WARNING, file=sys.stderr)
        raise RuntimeError(_WARNING)
    return value


def ensure_credit_integrity() -> None:
    credit_text()


def with_credit(message: str) -> str:
    return f"{message}\n\n{credit_text()}"
