import xml.etree.ElementTree as ET
import sys
import numexpr as ne

class ConfigLanguageTranslator:
    def __init__(self):
        self.constants = {}


    def parse_input(self, xml_input):
        try:
            root = ET.fromstring(xml_input)
            for child in root:
                self.process_elem(child, 0)
        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
            return None


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

    def get_value(self, tmp:str):
        if tmp.isalpha() and isinstance(self.constants[tmp], int):
            return str(self.constants[tmp])
        else:
            return tmp


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

if __name__ == "__main__":
    main()
