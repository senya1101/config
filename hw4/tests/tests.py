import unittest
import os
import json

from hw4.src.assembler import Assembler
from  hw4.src.interpreter import Interpreter

class TestAssembler(unittest.TestCase):

    def setUp(self):
        # Установим временные файлы для тестирования
        self.input_file = 'test_input.asm'
        self.output_file = 'test_output.bin'
        self.log_file = 'test_log.json'
        self.assembler = Assembler()

    def tearDown(self):
        # Удалим временные файлы после тестирования
        for filename in [self.input_file, self.output_file, self.log_file]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_load_const(self):
        with open(self.input_file, 'w') as f:
            f.write("LOAD_CONST 9 282\n")

        self.assembler.assemble(self.input_file, self.output_file, self.log_file)

        # Проверяем содержимое бинарного файла
        with open(self.output_file, 'rb') as f:
            data = f.read()

        # Ожидаем, что сгенерированный код будет равен по байтам
        expected_instruction = (282 << 4) | 9
        expected_bytes = expected_instruction.to_bytes(4, byteorder='little')
        self.assertEqual(data, expected_bytes)

        # Проверяем файл лога
        with open(self.log_file, 'r') as f:
            log_data = json.load(f)

        expected_log = [{"command": "LOAD_CONST 9 282", "binary": str(expected_bytes)}]
        self.assertEqual(log_data, expected_log)

    def test_write_command(self):
        with open(self.input_file, 'w') as f:
            f.write("WRITE 4 457\n")

        self.assembler.assemble(self.input_file, self.output_file, self.log_file)

        with open(self.output_file, 'rb') as f:
            data = f.read()

        # WRITE команда: 457 это B, 4 это A
        expected_instruction = (457 << 4) | 4
        expected_bytes = expected_instruction.to_bytes(4, byteorder='little')
        self.assertEqual(data, expected_bytes)

    def test_invalid_load_const(self):
        with open(self.input_file, 'w') as f:
            f.write("LOAD_CONST 9 8388608\n")  # 2^23 (недопустимо)

        with self.assertRaises(ValueError) as context:
            self.assembler.assemble(self.input_file, self.output_file, self.log_file)

        self.assertEqual(str(context.exception), "Константа B должен быть в пределах от 0 до 2^23-1")

    def test_invalid_read(self):
        with open(self.input_file, 'w') as f:
            f.write("READ 5 256\n")  # 256 не в диапазоне 0-255

        with self.assertRaises(ValueError) as context:
            self.assembler.assemble(self.input_file, self.output_file, self.log_file)

        self.assertEqual(str(context.exception), "Смещение B должен быть в пределах от 0 до 2^8-1")




class TestInterpreter(unittest.TestCase):

    def setUp(self):
        # Установим временные файлы для тестирования
        self.binary_file = 'test_program.bin'
        self.output_file = 'test_output.json'
        self.memory_size = 1024
        self.vm = Interpreter(memory_size=self.memory_size)

    def tearDown(self):
        # Удалим временные файлы после тестирования
        for filename in [self.binary_file, self.output_file]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_load_constant(self):
        # бинарный код для команды LOAD_CONST 9
        instruction = (282 << 4) | 9
        instruction_bytes = instruction.to_bytes(4, byteorder='little')

        with open(self.binary_file, 'wb') as f:
            f.write(instruction_bytes)

        self.vm.execute(self.binary_file, self.output_file, [0, 10])

        with open(self.output_file, 'r') as f:
            result = json.load(f)

        self.assertEqual(result['accumulator'], 282)
        self.assertEqual(result['memory_range'], [0] * 10)

    def test_write_command(self):
        # Подготовим команду WRITE 4
        load_instruction = (10 << 4) | 9
        write_instruction = (0 << 4) | 4  # Запись по адресу 0
        instructions = load_instruction | (write_instruction << 32)

        with open(self.binary_file, 'wb') as f:
            f.write(instructions.to_bytes(8, byteorder='little'))

        self.vm.execute(self.binary_file, self.output_file, [0, 10])

        # Проверка после выполнения
        self.assertEqual(self.vm.memory[0], 10)

    def test_read_command(self):
        # Подготовим команду LOAD_CONST и MOVE (READ)
        self.vm.memory[5] = 999  # Задаем значение в памяти
        load_instruction = (4 << 4) | 9  # LOAD_CONST 4
        read_instruction = (1 << 4) | 5  # READ - с [4 + 1]

        combined_instruction = load_instruction | (read_instruction << 32)

        with open(self.binary_file, 'wb') as f:
            f.write(combined_instruction.to_bytes(8, byteorder='little'))

        self.vm.execute(self.binary_file, self.output_file, [0, 10])

        with open(self.output_file, 'r') as f:
            result = json.load(f)

        self.assertEqual(result['accumulator'], 999)

    def test_left_rotate_command(self):
        self.vm.memory[0] = 4  # Задаем значение сдвига в памяти
        load_instruction = (2 << 4) | 9  # LOAD_CONST 4
        instruction = (0 << 4) | 11  # LEFT_ROTATE

        combined_instruction = load_instruction | (instruction << 32)

        with open(self.binary_file, 'wb') as f:
            f.write(combined_instruction.to_bytes(8, byteorder='little'))

        self.vm.execute(self.binary_file, self.output_file, [0, 10])

        self.assertEqual(self.vm.accumulator, 32)

    def test_invalid_command(self):
        # Записываем байт-код, который не соответствует ни одной команде
        invalid_instruction = (1 << 4) | 3 # Неизвестный инструктаж

        with open(self.binary_file, 'wb') as f:
            f.write(invalid_instruction.to_bytes(4, byteorder='little'))

        with self.assertRaises(ValueError) as context:
            self.vm.execute(self.binary_file, self.output_file, [0, 10])

        self.assertEqual(str(context.exception), "В бинарном файле содержатся невалидные данные: неверный байт-код")


if __name__ == '__main__':
    unittest.main()
