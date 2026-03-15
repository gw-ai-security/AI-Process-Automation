"""Phase 1 security scaffolding.

Security controls such as auth, request signing, or secrets rotation are explicitly
out of scope for Phase 1. This module exists to give later phases a clear home.
"""


def get_security_posture() -> dict[str, str]:
    """Return a simple statement of current security scope."""
    return {
        "phase": "1",
        "status": "placeholder",
        "note": "Authentication and authorization are intentionally deferred.",
    }
