import json
import sys


class Assembler:
    def __init__(self):
        # команды виртуальной машины(УВМ) и
        # их соответствующие значения
        # в формате шестнадцатеричных кодов(опкодах)
        self.instructions = {
            'LOAD_CONST': 0x9,
            'READ': 0x5,
            'WRITE': 0x4,
            'ROTATE_LEFT': 0xB
        }
        self.binary_code = []

    def assemble(self, input_file, output_file, log_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()
        logs = []
        for line in lines:
            parts = line.strip().split()
            if len(parts)==0 or line.startswith(';'):  # Игнорируем пустые строки и комментарии
                continue
            command = parts[0]
            if command in self.instructions:
                a = int(parts[1])# Значение A
                b = int(parts[2])# Значение B
                if (command=='LOAD_CONST' and not (0 <= b < (1 << 21))):
                    raise ValueError("Константа B должен быть в пределах от 0 до 2^23-1")
                elif (command in ['WRITE', 'ROTATE_LEFT'] and not (0 <= b < (1 << 23))):
                    raise ValueError("Смещение B должен быть в пределах от 0 до 2^23-1")
                elif (command=='READ' and not (0 <= b < (1 << 8))):
                    raise ValueError("Смещение B должен быть в пределах от 0 до 2^8-1")
                # Формируем бинарный код команды
                instruction = (b << 4) | a

                instruction = instruction.to_bytes(4, byteorder='little')
                logs.append({"command": line.rstrip(), "binary": str(instruction)})
                self.binary_code.append(instruction)
            else:
                print('Команда не найдена')
                return

        # Запись бинарного файла
        with open(output_file, 'wb') as f:
            for instruction in self.binary_code:
                f.write(instruction)

        # Запись лог-файла
        with open(log_file, 'w') as log_f:
            json.dump(logs, log_f, indent=4)


# Запуск ассемблера
if __name__ == "__main__":
    input_file = sys.argv[1]  # Путь к файлу с исходным кодом
    output_file = sys.argv[2]  # Путь к выходному бинарному файлу
    log_file = sys.argv[3]  # Путь к файлу лога
    assembler = Assembler()
    assembler.assemble(input_file, output_file, log_file)
