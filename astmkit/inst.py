import socket

from astmkit.config import ACK, ENQ, EOT, STX, CR, LF
from astmkit.encoder import build_astm_msg
from astmkit.parser import read_lines


# --- Emulator Helpers -------------------------------------------------

# Read a single byte from the socket.
def _recv_byte(sock: socket.socket) -> bytes:
    return sock.recv(1)


# Send ACK to confirm frame receipt.
def _send_ack(sock: socket.socket) -> None:
    sock.sendall(bytes([ACK]))


# --- Emulator Runner --------------------------------------------------

# Run a simple ASTM TCP session with the input file.
def instrument_emulator(input_path: str, host: str, port: int) -> None:
    records = read_lines(input_path)
    frame = build_astm_msg(records)

    with socket.create_connection((host, port)) as sock:
        sock.settimeout(2.0)

        # Start handshake and send the ASTM frame.
        sock.sendall(bytes([ENQ]))
        print("ENQ ->", _recv_byte(sock))

        sock.sendall(frame)
        print("FRAME ->", _recv_byte(sock))

        sock.sendall(bytes([EOT]))

        # Read response frames until timeout or EOT.
        data = b""
        while True:
            try:
                byte = _recv_byte(sock)
            except socket.timeout:
                break
            if not byte:
                break
            if byte == bytes([ENQ]):
                _send_ack(sock)
                continue
            if byte == bytes([STX]):
                chunk = b""
                while True:
                    c = _recv_byte(sock)
                    chunk += c
                    if chunk.endswith(bytes([CR, LF])):
                        break
                _send_ack(sock)
                data += byte + chunk
                continue
            if byte == bytes([EOT]):
                break

        print(data.decode("ascii", errors="ignore").replace("\r", "\\r"))
