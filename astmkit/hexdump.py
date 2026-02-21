def hexdump(data: bytes, length: int = 16) -> str:

    lines = []

    for offset in range(0, len(data), length):
        chunk = data[offset:offset + length]

        hex_bytes = " ".join(f"{b:02X}" for b in chunk)
        ascii_bytes = "".join(
            chr(b) if 32 <= b <= 126 else "."
            for b in chunk
        )
        
        lines.append(f"{offset:04X}  {hex_bytes:<{length * 3}}  |{ascii_bytes}|")

    return "\n".join(lines)
