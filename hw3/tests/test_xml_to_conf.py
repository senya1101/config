import unittest
import sys
import io


from hw3.src.xml_to_conf import ConfigLanguageTranslator

class TestConfigLanguageTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = ConfigLanguageTranslator()
        self.output = io.StringIO()
        sys.stdout = self.output  # Перенаправляем stdout на строковый буфер

    def tearDown(self):
        sys.stdout = sys.__stdout__  # Возвращаем stdout в исходное состояние

    def test_parse_valid_xml(self):
        xml_input = '''
        <config>
            <comment>Это комментарий</comment>
            <constant name="a">10</constant>
            <array name="my_array">
                <constant>1</constant>
                <constant>2</constant>
            </array>
        </config>
        '''
        self.translator.parse_input(xml_input)
        expected_output = "set a = 10\n<< 1, 2 >>\n"
        self.assertIn(expected_output.strip(), self.output.getvalue().strip())

    def test_duplicate_constant(self):
        xml_input = '''
        <config>
            <constant name="a">10</constant>
            <constant name="a">20</constant>
        </config>
        '''
        self.translator.parse_input(xml_input)
        self.assertIn("Константа с именем a уже существует", self.output.getvalue())

    def test_sort_array(self):
        xml_input = '''
        <config>
            <array name="my_array">
                <constant>3</constant>
                <constant>2</constant>
                <constant>1</constant>
            </array>
            <array name="my_sorted_array">@[my_array sort()]</array>
        </config>
        '''
        self.translator.parse_input(xml_input)
        self.assertIn("<< 3, 2, 1 >>\n<< 1, 2, 3 >>", self.output.getvalue().strip())

    def test_invalid_constant_value(self):
        xml_input = '''
        <config>
            <constant name="b">xyz</constant>
        </config>
        '''
        self.translator.parse_input(xml_input)
        self.assertIn("Константа содержит недопустимые символы", self.output.getvalue())

    def test_math_expression_evaluation(self):
        xml_input = '''
        <config>
            <constant name="x">5</constant>
            <constant name="y">10</constant>
            <constant name="result">@[x y +]</constant>
        </config>
        '''
        self.translator.parse_input(xml_input)
        expected_output = "set result = 15"
        self.assertIn(expected_output, self.output.getvalue())

    def test_zero_division(self):
        xml_input = '''
        <config>
            <constant name="x">5</constant>
            <constant name="y">0</constant>
            <constant name="result">@[x y /]</constant>
        </config>
        '''
        self.translator.parse_input(xml_input)
        self.assertIn("Ошибка вычисления", self.output.getvalue())

    def test_array(self):
        xml_input = '''
        <config>
            <array name="my_array">
            <comment>
                Разработать инструмент командной строки для учебного конфигурационного
                языка, синтаксис которого приведен далее. 
            </comment>
                    <array name="my_array1">
                        <constant>3</constant>
                        <constant>2</constant>
                        <constant>1</constant>
                    </array>
                <constant>3</constant>
                <constant>2</constant>
                <constant>1</constant>
            </array>
        </config>
        '''
        self.translator.parse_input(xml_input)
        self.assertIn("|# Разработать инструмент командной строки для учебного конфигурационного\n                языка, синтаксис которого приведен далее. #|\n<< [3, 2, 1], 3, 2, 1 >>", self.output.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
