import zipfile
import argparse
import os
from pathlib import Path
from collections import defaultdict


class VirtualFileSystem:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.root = Path("root")  # Виртуальный корень
        self.current_path = self.root
        self.history = []
        self.filesystemdata = {}
        self.filesystem=[]
        self._load_vfs()  # Загружаем виртуальную файловую систему

    def _load_vfs(self):
        """Загружает виртуальную файловую систему из zip-архива в память."""
        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            self.filesystem = defaultdict(list)
            for file_info in zip_ref.infolist():
                file_path = Path(file_info.filename)
                dir_path = Path(file_path.parent)
                if(dir_path==Path(".")):
                    self.filesystem[str(self.root)].append(file_path.name)
                else:
                    self.filesystem[str(self.root/dir_path)].append(file_path.name)

                if not file_info.is_dir():
                    self.filesystemdata[file_info.filename] = zip_ref.read(file_info).decode('utf-8')


    def list_files(self):
        current_dir = str(self.current_path)
        if current_dir in self.filesystem:
            return self.filesystem[current_dir]
        else:
            print("Директория пуста или не существует.")
            return []
        """Возвращает список файлов и папок в текущем каталоге."""



    def change_directory(self, new_dir):
        """Изменяет текущую директорию или переходит на уровень выше."""
        if new_dir == "..":
            # Переход на уровень выше
            if self.current_path != self.root:
                self.current_path = self.current_path.parent
                print(f"Перешли в директорию: {self.current_path}")
            else:
                print("Нет такого каталога")
        else:
            # Переход в указанную директорию
            new_path = self.current_path / new_dir
            if str(new_path) in self.filesystem:
                self.current_path = new_path
                print(f"Перешли в директорию: {self.current_path}")
            else:
                print("Нет такого каталога")


    def print_tree(self, path=None, level=0):
        """Рекурсивный вывод дерева каталогов."""
        if path == None:
            path = self.current_path

        current_dir = str(path)

        if current_dir in self.filesystem:
            for file in self.filesystem[current_dir]:
                print(' ' * level + file)

                self.print_tree(Path(current_dir)/Path(file), level + 4)

    def make_tree(self, path=None, level=0):
        dir = self.current_path/Path(path)

        if str(dir) in self.filesystem:
            self.print_tree(self.current_path/Path(path))
        else:
            print('Директория не найдена')




    def show_history(self):
        """Выводит историю команд."""
        return '\n'.join(self.history)

    def change_owner(self, path, owner):
        """Эмулирует изменение владельца файла."""
        # Поскольку мы не можем изменять владельцев в zip-файле, просто симулируем это
        dir = self.current_path / Path(path)
        filename = str(dir.parts[-1])
        dirr = str('\\'.join(dir.parts[:-1]))
        if str(dir) in self.filesystem or filename in self.filesystem[dirr]:
            self.print_tree(self.current_path / Path(path))
            print(f"Владелец {path} изменен на {owner}")
        else:
            print("Нет такого каталога/файла")



class ShellEmulator:
    def __init__(self, vfs):
        self.vfs = vfs
        self.hostname = 'localhost'

    def run(self):
        """Основной цикл эмулятора командной оболочки"""
        self.vfs.history=[]
        while True:
            command = input(f"{self.hostname}:{self.vfs.current_path} $ ").strip()
            self.vfs.history.append(command)
            if command == "exit":
                raise SystemExit
            elif command.startswith("ls"):
                self._handle_ls()
            elif command.startswith("cd"):
                self._handle_cd(command)
            elif command.startswith("tree"):
                self._handle_tree(command)
            elif command == "history":
                self._handle_history()
            elif command.startswith("chown"):
                self._handle_chown(command)
            else:
                print(f"Команда не найдена: {command}")

    def _handle_ls(self):
        """Обработчик команды ls"""
        files = self.vfs.list_files()
        for file in files:
             print(file)

    def _handle_cd(self, command):
        """Обработчик команды cd"""
        _, dir_name = command.split(maxsplit=1)
        try:
            self.vfs.change_directory(dir_name)
        except FileNotFoundError as e:
            print(e)



    def _handle_tree(self, command=None):
        """Обработчик команды tree"""
        if command=="tree":
            self.vfs.print_tree()
        else:
            _, path = command.split(maxsplit=1)
            self.vfs.make_tree(path)

    def _handle_history(self):
        """Обработчик команды history"""
        for i, cmd in enumerate(self.vfs.history, 1):
            print(f"{i}: {cmd}")

    def _handle_chown(self, command):
        """Обработчик команды chown"""
        _, file_name, user = command.split(maxsplit=2)
        try:
            self.vfs.change_owner(file_name, user)
        except FileNotFoundError as e:
            print(e)


def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Эмулятор командной оболочки")
    parser.add_argument('hostname', help="Имя компьютера для отображения в приглашении")
    parser.add_argument('vfs_zip', help="Путь к ZIP-архиву виртуальной файловой системы")
    return parser.parse_args()


def main():
    args = parse_args()
    vfs = VirtualFileSystem(args.vfs_zip)
    shell = ShellEmulator(vfs)
    shell.hostname = args.hostname
    shell.run()


if __name__ == "__main__":
    main()
