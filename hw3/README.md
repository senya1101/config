# Общее описание
### Задание
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений. 

Входной текст на языке xml принимается из стандартного ввода. Выходной
текст на учебном конфигурационном языке попадает в стандартный вывод.
### Синтаксис учебного конфигурационного языка
Многострочные комментарии:
```
|#
Это многострочный
комментарий
#|
```
Массивы:
```
<< значение, значение, значение, ... >>
```
Имена:
```
[a-z]+

```
Значения:
```
• Числа.
• Массивы.
```
Объявление констант на этапе трансляции:
```
set имя = значение
```
Вычисление констант на этапе трансляции:
```
@[имя 1 +]
```
Для константных вычислений определены операции и функции:
```
1. Сложение.
2. Вычитание.
3. Умножение.
4. Деление.
5. sort().
```

# Реализованный функционал
---

#### `parse_input(self, xml_input)`
```Python
    def parse_input(self, xml_input):
        try:
            root = ET.fromstring(xml_input)
            for child in root:
                self.process_elem(child, 0)
        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
            return None
```
- **Описание**: Принимает и парсит xml, в случае ошибки выдает сообщение. Вызывает обработку всех элементов
- **Параметры**:
  - `xml_input`: Полученный со стандартного ввода xml 

---
---

#### `process_elem(self, element, f)`
```Python
    def process_elem(self, element, f):
        if element.tag == 'comment':
            print(f"|# {element.text.strip()} #|")
        elif element.tag == 'array':
            res = []
            if element.text.startswith('@'):
                if element.attrib['name'] not in self.constants:
                    tmp = element.text[2:-1].split()
                    if tmp[1]=='sort()':
                        r = self.constants[tmp[0]]
                        if isinstance(r, list):
                            try:
                                r.sort()
                                if r!=None:
                                    res = r
                                else:
                                    print("Такой массив не найден")
                            except TypeError:
                                print(f"Значение {tmp[0]} невозможно отсортировать")
                        else:
                            print(f"Значение {tmp[0]} невозможно отсортировать")
                else:
                    print('Такое имя уже использовано')
            else:
                for child in element:
                    if child.tag!='constant':
                        m = self.process_elem(child, 1)
                        if m != None:
                            res.append(m)
                    elif child.tag=='constant':
                        try:
                            value = int(child.text)
                            res.append(value)
                        except ValueError:
                            print("Константа содержит недопустимые символы")
            if len(res)!=0:
                self.constants[element.attrib['name']] = res
            if f!=1 and len(res)!=0:
                print(f"<< {', '.join([str(x) for x in res])} >>")
            return res
        elif element.tag == 'constant':
            name = element.attrib.get('name')
            if name in self.constants:
                print(f"Константа с именем {name} уже существует")
            else:
                v=None
                if element.text.startswith('@'):
                    v = self.evaluate_expression(element.text.strip())
                else:
                    try:
                        v = int(element.text)
                    except ValueError:
                        print("Константа содержит недопустимые символы")
                if v!=None:
                    self.constants[name] = v
                    print(f"set {name} = {v}")
```
- **Описание**: Обрабатывает xml и выводит полученную информацию на учебном конфигурационном языке
- **Параметры**:
  - `element`: xml-элемент
  - `f`: флаг для правильного отображения массивов

---
---

#### `evaluate_expression(self, expression: str)`
```Python
    def evaluate_expression(self, expression: str):
        expression = expression[2:-1].split(maxsplit=3)
        if len(expression)==3:
            math_op = expression[2]
            if math_op in '+-*/' and len(math_op)==1:
                first_value = self.get_value(expression[0])
                second_value = self.get_value(expression[1])
                exp = first_value+math_op+second_value
                try:
                    result = ne.evaluate(exp).item()
                    return result
                except (SyntaxError, NameError, ZeroDivisionError, TypeError) as e:
                    print(f"Ошибка вычисления: {e}")
            else:
                print("Ошибка в выражении")
        else:
            print("Ошибка в выражении")
```
- **Описание**: Вычисляет значение константы
- **Параметры**:
  - `expression`: Строковое представление выражения

---

---

#### `def get_value(self, tmp:str)`
```Python
    def get_value(self, tmp:str):
        if tmp.isalpha() and isinstance(self.constants[tmp], int):
            return str(self.constants[tmp])
        else:
            return tmp
```
- **Описание**: Получает значение константы или числа
- **Параметры**:
  - `tmp`: Число или название константы

---

---

#### `main()`
```Python
    def main():
        translator = ConfigLanguageTranslator()
        xml_input = ""
        while True:
            inp = sys.stdin.readline()
            if inp.strip():
                xml_input+=inp
            else:
                break
        translator.parse_input(xml_input.rstrip())
```
- **Описание**: Основная функция, контролирует ввод и вызывает функции для дальнейшей обработки


---
# Сборка и запуск проекта
1. Загрузить репозиторий на компьютер
```
git clone https://github.com/senya1101/config
```
2. Перейдите в директорию 
```
cd hw3
```


3. Запустить config_converter.py
```
py xml_to_conf.py 
```
4. Ввод конфигурации в командную строку. Для завершения ввода нажать enter
# Примерs работы программы
### Настройка базы данных
**Входные данные:**
```
<configuration>
    <comment>Настройки
базы
данных</comment>
    <constant name="maxusers">100</constant>
    <constant name="inactiveusers">30</constant>
    <array name="dbs">
        <constant>4</constant>
        <constant>3</constant>
                <array name="useddbs">
                        <constant>9</constant>
                        <constant>4</constant>
                </array>
    </array>
    <constant name="activeusers">@[maxusers inactiveusers -]</constant>
    <comment>Сортировка баз данных</comment>
    <array name="sorteddb">@[ useddbs sort()]</array>
    <constant name="active">@[activeusers maxusers /]</constant>
</configuration>
```
**Выходные данные:**
```
|# Настройки
базы
данных #|
set maxusers = 100
set inactiveusers = 30
<< 4, 3, [9, 4] >>
set activeusers = 70
|# Сортировка баз данных #|
<< 4, 9 >>
set active = 0.7
```
### Конфигурация веб-сервера
**Входные данные:**
```
<configuration>
    <comment>Настройки
веб-сервера</comment>
    <constant name="maxconnections">150</constant>
    <constant name="timeout">30</constant>
    <array name="allowedips">
        <constant>19216811</constant>
        <constant>19216812</constant>
        <constant>19216813</constant>
    </array>
    <constant name="currentconnections">@[maxconnections 25 -]</constant>
    <comment>Сортировка разрешенных IP</comment>
    <array name="sortedips">@[allowedips sort()]</array>
    <constant name="serverload">@[currentconnections 10 +]</constant>
</configuration>

```
**Выходные данные:**
```
|# Настройки
веб-сервера #|
set maxconnections = 150
set timeout = 30
<< 19216811, 19216812, 19216813 >>
set currentconnections = 125
|# Сортировка разрешенных IP #|
<< 19216811, 19216812, 19216813 >>
set serverload = 135
```
# Результаты тестирования
