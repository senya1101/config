import struct
import json
import sys


class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size  # Эмуляция памяти
        self.accumulator = 0  # Регистр-аккумулятор

    def execute(self, binary_file, output_file, memory_range):
        with open(binary_file, 'rb') as f:
            while True:
                instruction = f.read(4)
                if len(instruction) == 0:
                    break  # Конец файла

                opcode, a, b = struct.unpack('>BHH', instruction)
                self.process_instruction(opcode, a, b)

        # Сохранение результата в выходной файл
        result_memory = self.memory[memory_range[0]:memory_range[1]]
        with open(output_file, 'w') as f:
            json.dump(result_memory, f)

    def process_instruction(self, opcode, a, b):
        if opcode == 0xA9:  # LOAD_CONST
            self.accumulator = b
        elif opcode == 0x15:  # READ_MEM
            self.accumulator = self.memory[self.accumulator + b]
        elif opcode == 0x94:  # WRITE_MEM
            self.memory[b] = self.accumulator
        elif opcode == 0x7B:  # ROTATE_LEFT
            value = self.memory[b]
            self.accumulator = ((self.accumulator << 1) | (value >> 15)) & 0xFFFF  # Циклический сдвиг
        else:
            raise ValueError("Неизвестная команда")


# Запуск интерпретатора
if __name__ == "__main__":
    binary_file = sys.argv[1]  # Путь к бинарному файлу
    output_file = sys.argv[2]  # Путь к выходному файлу
    memory_range = (int(sys.argv[3]), int(sys.argv[4]))  # Диапазон памяти для результата
    vm = VirtualMachine()
    vm.execute(binary_file, output_file, memory_range)
