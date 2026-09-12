def calculate_severity(filepath: str) -> str:
    """
    Calculate severity based on the type of honeytoken accessed.
    """

    filepath = filepath.lower()

    # High-value credential and secret decoys
    high_priority = [
        "password",
        "credential",
        "aws",
        ".env",
        "secret",
        "api_key",
        "apikey",
        "git-credentials"
    ]

    # Medium-value sensitive-looking files
    medium_priority = [
        ".xlsx",
        ".csv",
        ".json",
        ".db",
        ".sqlite"
    ]

    for keyword in high_priority:
        if keyword in filepath:
            return "high"

    for keyword in medium_priority:
        if keyword in filepath:
            return "medium"

    return "low"