def read_binary(path) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")


def write_binary(path, data: bytes):
    with open(path, "wb") as f:
            f.write(data)
