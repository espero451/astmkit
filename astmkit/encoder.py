from astmkit.constants import STX, ETX, CR, LF
from astmkit.binary import calc_checksum
from astmkit.config import ENCODING_DEFAULT


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
