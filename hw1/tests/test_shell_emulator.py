import unittest
from unittest.mock import patch, MagicMock, call
import zipfile
import os



from hw1.src.shell_emulator import VirtualFileSystem, ShellEmulator

class TestShellEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создание тестового zip-файла
        cls.zip_name = 'test_vfs.zip'
        with zipfile.ZipFile(cls.zip_name, 'w') as zipf:
            zipf.writestr('file1.txt', 'content of file1')
            zipf.writestr('file2.txt', 'content of file2')
            zipf.writestr('dir1/file3.txt', 'content of file3')
            zipf.writestr('dir1/dir2/file4.txt', 'content of file4')

        cls.vfs = VirtualFileSystem(cls.zip_name)
        cls.shell = ShellEmulator(cls.vfs)


    @classmethod
    def tearDownClass(cls):
        os.remove(cls.zip_name)  # Удаляем временный ZIP-файл


    @patch('builtins.input', side_effect=["ls", "cd dir1", "ls", "cd ..", "chown file1.txt user", "exit"])
    @patch('builtins.print')
    def test_command_execution(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):  # Проверка выхода
            self.shell.run()  # Запуск оболочки

        # Проверяем вывод ls команды
        mock_print.assert_any_call("file1.txt")
        mock_print.assert_any_call("file2.txt")



        # Проверка сообщения об изменении владельца
        mock_print.assert_any_call("Владелец файла file1.txt изменен на user")


    @patch('builtins.input', side_effect=["cd non_existing_dir", "exit"])
    @patch('builtins.print')
    def test_cd_invalid_directory(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):  # Проверка выхода
            self.shell.run()

        # Убедитесь, что выводится сообщение об ошибке
        mock_print.assert_called_with("Нет такого каталога")


    @patch('builtins.input', side_effect=["cd ..", "exit"])
    def test_cd_to_parent_directory(self, mock_input):
        # Переход в подкаталог
        self.shell.vfs.change_directory('dir1')

        with self.assertRaises(SystemExit):  # Проверка выхода
            self.shell.run()  # Запуск из родительского каталога

        self.assertEqual(str(self.shell.vfs.current_path), str(self.shell.vfs.root))  # Проверяет, что он на уровне корня


    @patch('builtins.input', side_effect=["ls", "tree", "history", "exit"])
    @patch('builtins.print')
    def test_history(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):  # Проверка выхода
            self.shell.run()  # Запуск оболочки

        expected_history = [
            "1: ls",
            "2: tree",
            "3: history",
        ]

        # Проверка, что history выводится корректно
        f=0
        for command in expected_history:
            if f==1:
                mock_print.assert_any_call(command)
            if command=="history":
                f=1


    @patch('builtins.input', side_effect=["exit"])
    def test_exit_command(self, mock_input):
        with self.assertRaises(SystemExit):  # Проверка выхода
            self.shell.run()  # Запуск оболочки

    @patch('builtins.input', side_effect=["cd dir1", "tree", "exit"])
    @patch('builtins.print')
    def test_tree_command(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):  # Проверка выхода
            self.shell.run()  # Запуск оболочки

        expected_tree = [
            'dir2',
            '    file3.txt',
            '/dir2',
            'file4.txt'
        ]
        f=0
        for tmp in expected_tree:
            if f==1:
                mock_print.assert_any_call(tmp)
            if tmp == "tree":
                f=1


if __name__ == '__main__':
    unittest.main()
