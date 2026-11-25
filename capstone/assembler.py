import os
import sys

COMP_TABLE = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|A": "0010101",
    "A|D": "0010101",
    "D|M": "1010101",
    "M|D": "1010101",
}

DEST_TABLE = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "AMD": "111",
    "ADM": "111",
}

JUMP_TABLE = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def build_predefined_symbols():
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }
    for i in range(16):
        symbols[f"R{i}"] = i
    return symbols


def clean_lines(raw_lines):
    cleaned = []
    for line in raw_lines:
        stripped = line.split("//")[0].strip()
        if stripped:
            cleaned.append(stripped)
    return cleaned


def assemble(asm_path):
    with open(asm_path, "r", encoding="utf-8") as f:
        lines = clean_lines(f.readlines())

    symbols = build_predefined_symbols()
    labels = {}
    variables = {}
    instructions = []

    rom_address = 0
    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            symbols[label] = rom_address
            labels[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1

    next_ram = 16
    machine_code = []

    for line in instructions:
        if line.startswith("@"):
            symbol = line[1:].strip()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram
                    variables[symbol] = next_ram
                    next_ram += 1
                address = symbols[symbol]
            machine_code.append(f"0{address:015b}")
        else:
            dest = ""
            jump = ""
            comp_part = line

            if "=" in comp_part:
                dest, comp_part = comp_part.split("=", 1)
            if ";" in comp_part:
                comp_part, jump = comp_part.split(";", 1)

            c_bits = COMP_TABLE[comp_part.strip()]
            d_bits = DEST_TABLE[dest.strip()]
            j_bits = JUMP_TABLE[jump.strip()]
            machine_code.append(f"111{c_bits}{d_bits}{j_bits}")

    base_dir = os.path.dirname(os.path.abspath(asm_path))
    base_name = os.path.splitext(os.path.basename(asm_path))[0]
    hack_path = os.path.join(base_dir, f"{base_name}.hack")
    symbols_path = os.path.join(base_dir, "symbols.txt")

    with open(hack_path, "w", encoding="utf-8") as f:
        f.write("\n".join(machine_code) + ("\n" if machine_code else ""))

    with open(symbols_path, "w", encoding="utf-8") as f:
        f.write("LABELS\n")
        for name, addr in labels.items():
            f.write(f"{name} = {addr}\n")
        f.write("\nVARIABLES\n")
        for name, addr in variables.items():
            f.write(f"{name} = {addr}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    assemble(sys.argv[1])