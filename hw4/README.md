# Общее описание
## Задание
Разработать ассемблер и интерпретатор для учебной виртуальной машины
(УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к
которой задается из командной строки. Результатом работы ассемблера является
бинарный файл в виде последовательности байт, путь к которому задается из
командной строки. Дополнительный ключ командной строки задает путь к файлулогу, в котором хранятся ассемблированные инструкции в духе списков
“ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.

Форматом для файла-лога и файла-результата является json.

Необходимо реализовать приведенные тесты для всех команд, а также
написать и отладить тестовую программу
# Команды ассемблера
## Загрузка константы
| A | B |
| :---: | :---: | 
| Биты 0-3 | Биты 4-24 |
| 9 | Константа |

Размер команды: 4 байт.

Операнд: поле B.

Результат: регистр-аккумулятор.

## Чтение значения из памяти
|    A     |     B     |
|:--------:|:---------:| 
| Биты 0-3 | Биты 4-11 | 
|    5     | Смещение  | 

Размер команды: 4 байт.

Операнд: значение в памяти по адресу, которым является сумма адреса (регистр-аккумулятор) и смещения (поле B).

Результат: регистр-аккумулятор.

## Запись значения в память
|    A     |     B     |
|:--------:|:---------:| 
| Биты 0-3 | Биты 4-26 |
|    4     |   Адрес   |

Размер команды: 4 байт.

Операнд:  регистр-аккумулятор.

Результат: Результат: значение в памяти по адресу, которым является поле B.

## Бинарная операция: побитовый циклический сдвиг влево
|    A     |     B     |
|:--------:|:---------:|
| Биты 0-3 | Биты 4-26 |
|    11    |   Адрес   |

Размер команды: 4 байт.

Первый операнд: регистр-аккумулятор. 
Второй операнд: значение в памяти по адресу, которым является поле B. 
Результат: регистр-аккумулятор.

# Сборка и запуск проекта
1. Загрузить репозиторий на компьютер
```
git clone https://github.com/senya1101/config
```
2. Прейдите в директорию репозитория
```
cd hw4
```
3. Запустить assembler.py с указанием исполняемой программы, бинарного файла вывода и лог-файла
```
py assembler.py <исполняемая_программа.asm> <бинарный_файл_вывода.bin> -l <лог-файл.xml>
```
4. Запустить interpreter.py с указанием бинарного файла данных, файла с результатами и диапазона памяти
```
py interpreter.py <бинарный_файл_данных.bin> <результат.xml> -lb <левая_граница_диапазона> -rb <правая граница диапазона>
```
# Примерs работы программы
### Задание для тестовой программы
Выполнить поэлементно операцию умножение над вектором длины 6 и числом 128. Результат записать в новый вектор. 
### Тестовая программа
```
LOAD_CONSTANT 36 0 2
LOAD_CONSTANT 36 1 3
LOAD_CONSTANT 36 2 4
LOAD_CONSTANT 36 3 5
LOAD_CONSTANT 36 4 6
LOAD_CONSTANT 36 5 7
LOAD_CONSTANT 36 10 128
MUL 32 20 0 10
MUL 32 21 1 10
MUL 32 22 2 10
MUL 32 23 3 10
MUL 32 24 4 10
MUL 32 25 5 10
```
### Данные, записанные в лог-файл
```
<?xml version="1.0" encoding="utf-8"?>
<log>
	<LOAD_CONSTANT A="36" B="0" C="2">248000000000</LOAD_CONSTANT>
	<LOAD_CONSTANT A="36" B="1" C="3">a4c000000000</LOAD_CONSTANT>
	<LOAD_CONSTANT A="36" B="2" C="4">240101000000</LOAD_CONSTANT>
	<LOAD_CONSTANT A="36" B="3" C="5">a44101000000</LOAD_CONSTANT>
	<LOAD_CONSTANT A="36" B="4" C="6">248201000000</LOAD_CONSTANT>
	<LOAD_CONSTANT A="36" B="5" C="7">a4c201000000</LOAD_CONSTANT>
	<LOAD_CONSTANT A="36" B="10" C="128">240520000000</LOAD_CONSTANT>
	<MUL A="32" B="20" C="0" D="10">200a40010000</MUL>
	<MUL A="32" B="21" C="1" D="10">a04a40010000</MUL>
	<MUL A="32" B="22" C="2" D="10">208b40010000</MUL>
	<MUL A="32" B="23" C="3" D="10">a0cb40010000</MUL>
	<MUL A="32" B="24" C="4" D="10">200c41010000</MUL>
	<MUL A="32" B="25" C="5" D="10">a04c41010000</MUL>
</log>
```
### Данные, записанные в файл-результат
```
<?xml version="1.0" encoding="utf-8"?>
<result>
	<register address="0">2</register>
	<register address="1">3</register>
	<register address="2">4</register>
	<register address="3">5</register>
	<register address="4">6</register>
	<register address="5">7</register>
	<register address="10">128</register>
	<register address="20">256</register>
	<register address="21">384</register>
	<register address="22">512</register>
	<register address="23">640</register>
	<register address="24">768</register>
	<register address="25">896</register>
</result>
```
# Результаты тестирования
## Ассемблер
### Тест загрузки константы
```
def test_load_const(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("LOAD_CONSTANT 36 32 12")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "241003000000")
```
### Тест чтения из памяти
```
def test_read_memory(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("READ_MEMORY 58 26 198")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "3a8d31000000")
```
### Тест записи в память
```
def test_write_memory(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("WRITE_MEMORY 25 48 919")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "19d8e5000000")
```
### Тест бинарной операции умножения
```
def test_multiply(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("MUL 32 68 90 15")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "20a2f6010000")
```
### Тест ошибки аргумента команды
```
def test_value_error(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("LOAD_CONSTANT 10 10 10")

        assembler = Assembler(filename, binary_file, log_file)
        with self.assertRaisesRegex(ValueError, "Параметр А должен быть равен 36"):
            assembler.assemble()

        os.remove(filename)
```
### Тест ошибки определения команды
```
def test_syntax_error(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("MOV 50")

        assembler = Assembler(filename, binary_file, log_file)
        with self.assertRaisesRegex(SyntaxError, "Неизвестная команда"):
            assembler.assemble()

        os.remove(filename)
```
## Интерпретатор
### Тест загрузки константы
```
def test_load_const(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x24\x10\x03\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[32], 12)
```
### Тест чтения из памяти
```
def test_read_memory(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x3a\x8d\x31\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[26], 0)
```
### Тест записи в память
```
def test_write_memory(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x19\xd8\xe5\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[919], 0)
```
### Тест бинарной операции умножения
```
def test_multiply(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x20\xa2\xf6\x01\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[68], 0)
```
### Тест ошибки определения команды/аргумента
```
def test_value_error(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x01\x00\x00\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        with self.assertRaisesRegex(ValueError, "В бинарном файле содержатся невалидные данные: неверный байт-код"):
            interpreter.interpret()

        os.remove(filename)

        self.assertEqual(interpreter.registers[919], 0)
```
## Результаты тестирования
![image](https://github.com/user-attachments/assets/12f47803-d419-4a91-bfa9-e5fdb387e9c1)