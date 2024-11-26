import json
import sys


class Interpreter:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size  # Эмуляция памяти
        self.accumulator = 0  # Регистр-аккумулятор

    def execute(self, binary_file, output_file, memory_range):
        byte_code = 0
        with open(binary_file, 'rb') as f:
            byte_code = int.from_bytes(f.read(), byteorder="little")

        while byte_code !=0:
            a = byte_code & ((1 << 4) -1 )
            byte_code >>= 4
            match a:
                case 9:#LOAD_CONSTANT
                    self.accumulator = byte_code & ((1 << 21)-1)
                case 5:#READ
                    offset = byte_code & ((1 << 8) -1)
                    self.accumulator = self.memory[self.accumulator+offset]
                case 4:#WRITE
                    address = byte_code & ((1 <<23)-1)
                    self.memory[address] = self.accumulator
                case 11:#ROTATE_LEFT
                    address = byte_code & ((1 << 23) - 1)
                    shift = self.memory[address]
                    self.accumulator = ((self.accumulator << shift) & ((1 << 21)-1)) | (self.accumulator >> (21 - shift))
                    #Сдвигаем число влево и обрезаем его до нужного количества бит, используя маску (1 << bits) - 1.
                    # Эта маска устанавливает все биты в 1 до bits.
                    #Комбинируем сдвинутое число с правым сдвигом исходного числа, который возвращает старшие биты в младшие позиции.
                case _:
                    raise ValueError("В бинарном файле содержатся невалидные данные: неверный байт-код")
            byte_code >>= 28



        # Записываем результаты в json
        result = {
            "memory_range": self.memory[memory_range[0]:memory_range[1]],
            "accumulator": self.accumulator
        }

        # Сохранение результата в выходной файл
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=4)



# Запуск интерпретатора
if __name__ == "__main__":
    binary_file = sys.argv[1]  # Путь к бинарному файлу
    output_file = sys.argv[2]  # Путь к выходному файлу
    memory_range = [int(sys.argv[3]), int(sys.argv[4])]  # Диапазон памяти для результата
    vm = Interpreter()
    vm.execute(binary_file, output_file, memory_range)
