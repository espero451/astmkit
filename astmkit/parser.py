from astmkit.config import ENCODING_DEFAULT


def read_lines(path: str) -> list[str]:
    """
    Read file and return list of non-empty stripped lines.
    """
    try:
        with open(path, encoding=ENCODING_DEFAULT) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")


def extract_record(records: list[str], record_type: str) -> str | None:
    """
    Extract the first record of a given type from a list of ASTM records.
    """
    for record in records:
        if record.startswith(record_type):
            return record
    return None


def enumerate_fields(record: str) -> str:
    """
    Enumerate fields of a single ASTM message record.
    """
    record_type = record[0]
    fields = record.split("|")
    
    lines = [record] # unsplited line for clarity
    
    for index, field in enumerate(fields, start=1):
        lines.append(f"{record_type}{index}: {field}")

    return "\n".join(lines)
