from astmkit.config import ENCODING_DEFAULT, STX, ETX, CR, LF


# 8-bit sum
def calc_checksum(payload: bytes) -> int:
    return sum(payload) & 0xFF


def build_astm_msg(records: list[str]) -> bytes:

    # Add CR to each record
    body = b"".join(
        record.encode(ENCODING_DEFAULT) + bytes([CR])
        for record in records
    )

    checksum = calc_checksum(body)

    # Add checksum and terminate with CRLF
    return (
        bytes([STX])
        + body
        + bytes([ETX])
        + f"{checksum:02X}".encode(ENCODING_DEFAULT)
        + bytes([CR, LF])
    )
