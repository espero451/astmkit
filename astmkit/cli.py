import argparse
import sys

from astmkit.parser import read_lines, extract_record, enumerate_fields
from astmkit.encoder import build_astm_msg
from astmkit.io import read_binary, write_binary
from astmkit.hexdump import hexdump
from astmkit.inst import instrument_emulator


# --- CLI Helpers ------------------------------------------------------

# Normalize record type inputs like "H/O/R".
def _split_record_types(raw_values: list[str]) -> list[str]:
    record_types = []
    for value in raw_values:
        for part in value.split("/"):
            token = part.strip()
            if token:
                record_types.append(token.upper())
    return record_types


# --- CLI Commands -----------------------------------------------------

# Enumerate fields for one record type.
def run_enumerate_fields(path: str, record_type: str):
    records = read_lines(path)
    record = extract_record(records, record_type.upper())

    if record is None:
        raise SystemExit(f"Error: record '{record_type}' not found")

    print(enumerate_fields(record))


# Build and write an ASTM binary frame.
def run_build(input_path: str, output_path: str):
    records = read_lines(input_path)
    data = build_astm_msg(records)
    write_binary(output_path, data)
    print(f"'{output_path}' successfully created")


# Print a hex dump of a binary file.
def run_hexdump(path: str, width: int):
    data = read_binary(path)
    print(hexdump(data, width))


# Run the instrument emulator session.
def run_instrument_emulator(input_path: str, host: str, port: int) -> None:
    instrument_emulator(input_path, host, port)


# --- CLI Setup --------------------------------------------------------

def main():
    # Build subcommands for each CLI mode.
    parser = argparse.ArgumentParser("astmkit")
    subparsers = parser.add_subparsers(dest="command")

    parser_enum = subparsers.add_parser(
        "enum",
        help="Enumerate fields of a record"
    )
    parser_enum.add_argument("input", help="Input file path")
    parser_enum.add_argument(
        "record_types",
        nargs="+",
        help="Record type(s): H, P, O, R, C, M, L, Q (use '/' to split)"
    )

    parser_hex = subparsers.add_parser(
        "hex",
        help="Show hex dump of input file"
    )
    parser_hex.add_argument("input", help="Input file path")
    parser_hex.add_argument(
        "width",
        nargs="?",
        type=int,
        default=16,
        help="Bytes per line (default: 16)"
    )

    parser_frame = subparsers.add_parser(
        "frame",
        help="Build binary ASTM frame"
    )
    parser_frame.add_argument("input", help="Input file path")
    parser_frame.add_argument("output", help="Output file path")

    parser_inst = subparsers.add_parser(
        "inst",
        help="Run instrument emulator"
    )
    parser_inst.add_argument("input", help="Input file path")
    parser_inst.add_argument(
        "--host",
        default="127.0.0.1",
        help="Target host (default: 127.0.0.1)"
    )
    parser_inst.add_argument(
        "--port",
        required=True,
        type=int,
        help="Target port"
    )

    args = parser.parse_args()

    if args.command == "enum":
        # Run enumeration for each requested record type.
        record_types = _split_record_types(args.record_types)
        if not record_types:
            raise SystemExit("Error: record type list is empty")
        for record_type in record_types:
            run_enumerate_fields(args.input, record_type)
        return

    if args.command == "hex":
        run_hexdump(args.input, args.width)
        return

    if args.command == "frame":
        run_build(args.input, args.output)
        return

    if args.command == "inst":
        run_instrument_emulator(args.input, args.host, args.port)
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
