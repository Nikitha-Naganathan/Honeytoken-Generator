from pathlib import Path


def generate_honeytokens():
    honeytoken_dir = Path("honeytokens")
    honeytoken_dir.mkdir(exist_ok=True)

    passwords = honeytoken_dir / "passwords.txt"
    passwords.write_text(
        "Employee Login Credentials\n"
        "Username: admin_demo\n"
        "Password: HoneyDemo123\n"
    )

    api_keys = honeytoken_dir / "api_keys.txt"
    api_keys.write_text(
        "API Credentials\n"
        "Service: DemoCloud\n"
        "API Key: HONEY-FAKE-123456\n"
    )

    database = honeytoken_dir / "database_credentials.txt"
    database.write_text(
        "Database Credentials\n"
        "Username: db_admin_demo\n"
        "Password: FakeDBPassword123\n"
    )

    return [passwords, api_keys, database]


if __name__ == "__main__":
    tokens = generate_honeytokens()

    print("[+] Honeytokens created:")

    for token in tokens:
        print(f"    {token}")