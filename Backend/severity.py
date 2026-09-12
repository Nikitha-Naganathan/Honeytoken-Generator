from pathlib import Path


# File types that are especially interesting
# when accessed by an attacker.
HIGH_SEVERITY_EXTENSIONS = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".env",
    ".sql",
}

HIGH_SEVERITY_NAMES = {
    "passwords.txt",
    "api_keys.txt",
    "database_credentials.txt",
    "passwords.xlsx",
    "credentials.txt",
    "aws_credentials.txt",
    "secrets.txt",
    "id_rsa",
}


def calculate_severity(filepath: str) -> str:

    filename = Path(filepath).name.lower()
    extension = Path(filepath).suffix.lower()

    # Very sensitive honeytokens
    if filename in HIGH_SEVERITY_NAMES:
        return "high"

    # Sensitive credential/key files
    if extension in HIGH_SEVERITY_EXTENSIONS:
        return "high"

    # Medium-risk files
    if extension in {".docx", ".xlsx", ".csv", ".pdf"}:
        return "medium"

    # Everything else
    return "low"