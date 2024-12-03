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

## Реализованный функционал
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
    def process_elem(self, element):
        if element.tag == 'comment':
            print(f"|# {element.text.strip()} #|")
        elif element.tag == 'array':
            if 'name' in  element.attrib and element.attrib['name'] not in self.constants:
                res = self.process_array(element)
                if res!=None:
                    print(f"<< {', '.join([str(x) for x in res])} >>")
            else:
                print("Массив с таким именем уже есть или имя не задано")

        elif element.tag == 'constant':
            if 'name' in element.attrib and element.attrib['name'] not in self.constants:
                value = self.process_const(element)
                if value!=None:
                    self.constants[element.attrib['name']]=value
                    print(f"set {element.attrib['name']} = {value}")
            else:
                print("Константа с таким именем уже есть или имя не задано")
```
- **Описание**: Обрабатывает xml элементы
- **Параметры**:
  - `element`: xml-элемент


---
---

#### `evaluate_expression(self, expression: str)`
```Python
    def evaluate_expression(self, expression: str):
        expression = expression[2:-1].split()
        values = []
        result = 0
        for i in expression:
            if i in "+/*-":
                if len(values)>1:
                    try:
                        result = eval(str(i).join(values[-2:]))
                    except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
                        print(f"Возникла ошибка: {e}")
                        return None


                    del values[-2:]
                    values.append(str(result))
            elif i.isdigit():
                values.append(str(i))
            elif i in self.constants:
                values.append(str(self.constants[i]))
            else:
                print("Ошибка в выражении")
                return None

        if len(values)!=1 or str(result)!=values[0]:
            print("Ошибка в выражении")
            return None
        return result
```
- **Описание**: Вычисляет значение константы
- **Параметры**:
  - `expression`: Строковое представление выражения

---

---

#### `def process_const(self, element)`
```Python
    def process_const(self, element):
        v = None
        if element.text.startswith('@'):
            v = self.evaluate_expression(element.text.strip())
        else:
            try:
                v = int(element.text)
            except ValueError:
                print("Константа содержит недопустимые символы")
        return v
```
- **Описание**: Получает значение константы или числа
- **Параметры**:
  - `element`: элемент xml - константа

---

---

#### `def get_value(self, tmp:str)`
```Python
        def process_array(self, element):
        res = []
        if element.text.startswith('@'):
            if element.attrib['name'] not in self.constants:
                tmp = element.text[2:-1].split()
                if tmp[1] == 'sort()' and tmp[0] in self.constants:
                    r = self.constants[tmp[0]]
                    if isinstance(r, list):
                        try:
                            r.sort()
                            if r != None:
                                res = r
                            else:
                                print("Такой массив не найден")
                                return None
                        except TypeError:
                            print(f"Значение {tmp[0]} невозможно отсортировать")
                            return None
                    else:
                        print(f"Значение {tmp[0]} невозможно отсортировать")
                        return None
                else:
                    print("Такой массив не найден")
                    return None
            else:
                print('Такое имя уже использовано')
        elif element.text.rstrip().startswith('['):
            elements = []
            try:
                elements = ast.literal_eval(element.text.rstrip())

            except(ValueError, SyntaxError) as e:
                elements=None
                print(f"Ошибка при преобразовании строки в массив: {e}")

            if elements!=None:
                res=elements
        else:
            for child in element:
                if child.tag == 'constant':
                    m = self.process_const(child)
                    if m != None:
                        res.append(m)
                    else:
                        print("Ошибка в элементе массива")
                        return None
                elif child.tag == 'array':
                    m = self.process_array(child)
                    if m != None:
                        res.append(m)
                    else:
                        print("Ошибка в элементе массива")
                        return None
        self.constants[element.attrib['name']] = res
        return res
```
- **Описание**: Обрабатывет массив
- **Параметры**:
  - `element`: xml элемент массив

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
## Сборка и запуск проекта
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
py src/xml_to_conf.py 
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
        [19216811, 19216812, 19216813]
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
## Пример использования в виде скриншотов
![test](https://github.com/senya1101/config/blob/images/hw3/img/ex2.py.png?raw=true )
![test](https://github.com/senya1101/config/blob/images/hw3/img/exam1.png?raw=true )
## Результаты тестирования
![test](https://github.com/senya1101/config/blob/images/hw3/img/tests3.png?raw=true )
