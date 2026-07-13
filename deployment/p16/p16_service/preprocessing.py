from __future__ import annotations

import re

APOSTROPHE_RE = re.compile(r"['’‘ʼʻ`´]")
TOKEN_RE = re.compile(r"[a-z][a-z']*")
STOPWORDS = {
    "va", "bu", "bir", "bilan", "da", "ni", "ga", "dan", "ham", "uchun",
    "bo'lgan", "bo'lib", "bo'ldi", "o'z", "ular", "u", "men", "biz", "siz",
    "edi", "ekan", "deb", "lekin", "ammo", "yoki", "agar", "chunki", "hali",
    "ko'p", "oz", "shunday", "shu", "esa", "endi", "bor", "yo'q", "kerak",
    "mumkin", "bo'lsa", "bo'lishi",
}
SUFFIXES = sorted(
    {
        "larning", "lardan", "larimiz", "laringiz", "laridir", "larni", "larga",
        "larim", "laring", "lari", "imizdan", "ingizdan", "ning", "niki", "nchi",
        "lilik", "ligi", "roqqa", "roq", "ishda", "ishi", "ish", "chi", "lik",
        "lar", "ni", "da", "dan", "ga",
    },
    key=len,
    reverse=True,
)


def preprocess(text: str) -> list[str]:
    """Mirror the m01 preprocessing stored with the LSTM training artifact."""
    normalized = APOSTROPHE_RE.sub("'", text).lower()
    result: list[str] = []
    for token in TOKEN_RE.findall(normalized):
        if len(token) < 2 or token in STOPWORDS:
            continue
        result.append(_stem(token))
    return result


def _stem(token: str) -> str:
    for suffix in SUFFIXES:
        if token.endswith(suffix) and len(token) - len(suffix) >= 3:
            return token[: -len(suffix)]
    return token
