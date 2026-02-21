# ASTM Kit

**ASTM Kit** is a command-line tool for working with ASTM messages: enumerate fields, build binary frames, inspect hex dumps, and emulate instrument TCP sessions.

---

## Installation:

```
pipx install .
```

## Usage:

```
usage: astmkit <command> [args]

commands:
  enum   Enumerate fields of a record
  hex    Show hex dump of input file
  frame  Build binary ASTM frame
  inst   Run instrument emulator
```

## Modes Explanation

### Mode 1. Enumerate fields of a specific record.

Allows simple enumeration of segments within a record. You can select record types: H, P, O, R, C, M, L, Q (case-insensitive).

Command: ```astmkit enum input.astm P```

Multiple record types are supported:
```
astmkit enum input.astm H/O/R/C/M
astmkit enum input.astm H O R C M
```

Example:

Input record:
```
H|\^&|||CHEM3000|||||LIS||P|1
P|1||PAT0001||DOE^ALICE||19850512|F
O|1|SMP0001||^^^GLU^1|R|20260107103000||||N||||1
R|1|^^^GLU|5.4|mmol/L|3.9-5.8|N|||F
R|2|^^^CHOL|4.9|mmol/L|0-5.2|N|||F
L|1|N
```
CLI output:
```
P|1||PAT0001||DOE^ALICE||19850512|F
P1: P
P2: 1
P3: 
P4: PAT0001
P5: 
P6: DOE^ALICE
P7: 
P8: 19850512
P9: F
```

### Mode 2. Build ASTM frame for instrument or interface.

Converts a text-based ASTM message into a structured binary frame suitable for feeding to laboratory instruments or interfaces for testing and debugging purposes.

Command:
```astmkit frame input.astm output.astm```


### Mode 3. Hex dump of input files.

Displays the hexadecimal representation of a file, facilitating low-level inspection of message content for debugging and validation.

Command:
```
astmkit hex input.astm       # default 16 bytes per line
astmkit hex input.astm 32    # custom bytes per line
```
CLI output:
```
0000  48 7C 5C 5E 26 7C 7C 7C 43 48 45 4D 31 30 30 30   |H|\^&|||CHEM1000|
0010  7C 7C 7C 7C 7C 4C 49 53 7C 7C 50 7C 31 0A 50 7C   ||||||LIS||P|1.P||
0020  31 7C 7C 50 41 54 30 30 30 31 7C 7C 44 4F 45 5E   |1||PAT0001||DOE^|
0030  41 4C 49 43 45 7C 7C 31 39 38 35 30 35 31 32 7C   |ALICE||19850512||
0040  46 0A 4F 7C 31 7C 53 4D 50 30 30 30 31 7C 7C 5E   |F.O|1|SMP0001||^|
0050  5E 5E 47 4C 55 5E 31 7C 52 7C 32 30 32 36 30 31   |^^GLU^1|R|202601|
0060  30 37 31 30 33 30 30 30 7C 7C 7C 7C 4E 7C 7C 7C   |07103000||||N||||
0070  7C 31 0A 52 7C 31 7C 5E 5E 5E 47 4C 55 7C 35 2E   ||1.R|1|^^^GLU|5.|
0080  34 7C 6D 6D 6F 6C 2F 4C 7C 33 2E 39 2D 35 2E 38   |4|mmol/L|3.9-5.8|
0090  7C 4E 7C 7C 7C 46 0A 52 7C 32 7C 5E 5E 5E 43 48   ||N|||F.R|2|^^^CH|
00A0  4F 4C 7C 34 2E 39 7C 6D 6D 6F 6C 2F 4C 7C 30 2D   |OL|4.9|mmol/L|0-|
00B0  35 2E 32 7C 4E 7C 7C 7C 46 0A 4C 7C 31 7C 4E      |5.2|N|||F.L|1|N|
```

### Mode 4. Instrument emulator

Sends an ASTM frame over TCP to a target host and prints response frames.

Command:
```
astmkit inst input.astm --port 20100
astmkit inst input.astm --host 127.0.0.1 --port 20100
```

## Running Tests

The project uses pytest for unit testing. To run tests:

```
python3 -m pytest
```

##  TODO

- Add support for serial interfaces
