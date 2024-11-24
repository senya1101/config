import xml.etree.ElementTree as ET
import sys
import ast


class ConfigLanguageTranslator:
    def __init__(self):
        self.constants = {}


    def parse_input(self, xml_input):
        try:
            root = ET.fromstring(xml_input)
            for child in root:
                self.process_elem(child)
        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
            return None


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
        elif element.text.replace('\n','').replace(' ','').startswith('['):
            tmp = element.text.replace('\n','').replace(' ','')
            elements = []
            try:
                elements = ast.literal_eval(tmp)

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
