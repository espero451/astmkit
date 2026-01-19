import argparse
import sys

from astmkit.parser import read_lines, extract_record, enumerate_fields
from astmkit.encoder import build_astm_msg
from astmkit.io import read_binary, write_binary
from astmkit.binary import hexdump


def run_enumerate_fields(path: str, record_type: str):
    records = read_lines(path)
    record = extract_record(records, record_type.upper())

    if record is None:
        raise SystemExit(f"Error: record '{record_type}' not found")

    print(enumerate_fields(record))


def run_build(input_path: str, output_path: str):
    records = read_lines(input_path)
    data = build_astm_msg(records)
    write_binary(output_path, data)
    print(f"'{output_path}' successfully created")


def run_hexdump(path: str, width: int):
    data = read_binary(path)
    print(hexdump(data, width))


def main():
    # argparse
    parser = argparse.ArgumentParser("astmkit")

    parser.add_argument("-i", "--input", help="Input file path")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument(
        "-r", "--record",
        help="Record type to enumerate: H, P, O, R, C, M, L, Q"
    )
    parser.add_argument(
        "-x", "--hex", nargs="?", const=16, type=int,
        help="Show hex dump (optional bytes per line, default: 16)"
    )

    args = parser.parse_args()

    if args.hex is not None:
        if not args.input:
            raise SystemExit("Error: --hex requires --input")
        run_hexdump(args.input, args.hex)
        return

    if args.record:
        if not args.input:
            raise SystemExit("Error: --record requires --input")
        run_enumerate_fields(args.input, args.record)
        return

    if args.input and args.output:
        run_build(args.input, args.output)
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
