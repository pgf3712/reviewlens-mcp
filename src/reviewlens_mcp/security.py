import re

from .models import InjectionSignal

_INJECTION_PATTERNS = {
    "ignore_previous": re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    "role_override": re.compile(r"(?:system|assistant)\s*(?:message|prompt)?\s*:", re.I),
    "secret_request": re.compile(
        r"(?:reveal|print|exfiltrate).{0,30}(?:token|secret|password)", re.I
    ),
    "tool_command": re.compile(r"(?:call|use|execute)\s+(?:the\s+)?(?:tool|command)", re.I),
}

_SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(token|password|secret)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
]


def redact_secrets(value: str) -> str:
    for pattern in _SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    return value


def scan_untrusted_content(location: str, value: str) -> list[InjectionSignal]:
    return [
        InjectionSignal(
            location=location,
            pattern=name,
            explanation="Instruction-like text found in untrusted repository content; it was not executed.",
        )
        for name, pattern in _INJECTION_PATTERNS.items()
        if pattern.search(value)
    ]
