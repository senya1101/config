import struct
import json
import sys


class Assembler:
    def __init__(self):
        self.instructions = {
            'LOAD_CONST': 0xA9,
            'READ_MEM': 0x15,
            'WRITE_MEM': 0x94,
            'ROTATE_LEFT': 0x7B
        }
        self.binary_code = []

    def assemble(self, input_file, output_file, log_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) == 0 or parts[0].startswith(';'):  # Игнорируем пустые строки и комментарии
                continue

            command = parts[0]
            if command in self.instructions:
                opcode = self.instructions[command]
                a = int(parts[1])  # Значение A
                b = int(parts[2])  # Значение B

                # Формируем бинарный код команды
                if command == 'LOAD_CONST':
                    instruction = struct.pack('>BHH', opcode, a, b)
                elif command in ['READ_MEM', 'WRITE_MEM', 'ROTATE_LEFT']:
                    instruction = struct.pack('>BHH', opcode, a, b)

                self.binary_code.append(instruction)

        # Запись бинарного файла
        with open(output_file, 'wb') as f:
            for instruction in self.binary_code:
                f.write(instruction)

        # Запись лог-файла
        log_data = [{"command": line.strip(), "binary": instruction.hex()} for line, instruction in
                    zip(lines, self.binary_code)]
        with open(log_file, 'w') as log_f:
            json.dump(log_data, log_f, indent=4)


# Запуск ассемблера
if __name__ == "__main__":
    input_file = sys.argv[1]  # Путь к файлу с исходным кодом
    output_file = sys.argv[2]  # Путь к выходному бинарному файлу
    log_file = sys.argv[3]  # Путь к файлу лога
    assembler = Assembler()
    assembler.assemble(input_file, output_file, log_file)
