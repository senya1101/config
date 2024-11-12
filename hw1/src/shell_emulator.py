import os
import zipfile
import argparse
import sys
import shutil
from pathlib import Path
from re import split
from pathlib import PurePosixPath


class VirtualFileSystem:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.root = Path("/root")
        self.current_path = self.root
        self.history = []
        self.filesystem = self._load_vfs()

    def _load_vfs(self):
        """Загружает виртуальную файловую систему из zip-архива"""
        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.root)

    def list_files(self):
        """Возвращает список файлов и папок в текущем каталоге"""
        return [entry for entry in self.current_path.iterdir()]

    def change_directory(self, new_dir):
        """Изменяет текущую директорию или переходит на уровень выше"""

        # Если new_dir это "..", то переходим на уровень выше
        if new_dir == "..":
            parent_dir = self.current_path.parent
            if parent_dir.exists() and parent_dir.is_dir():
                self.current_path = parent_dir
            else:
                raise FileNotFoundError("Не удается перейти на уровень выше, директория не существует.")
        else:
            # Иначе, переходим в новую директорию
            target = self.current_path / new_dir
            if target.exists() and target.is_dir():
                self.current_path = target
            else:
                raise FileNotFoundError(f"Нет такого каталога: {new_dir}")



class Shell:
    def __init__(self, vfs):
        self.vfs = vfs
        self.hostname = 'localhost'

    def run(self):
        """Основной цикл эмулятора"""
        while True:
            command = input(f"{self.hostname}:{self.vfs.current_path} $ ").strip()
            self.vfs.history.append(command)
            if command == "exit":
                break
            elif command.startswith("ls"):
                self._handle_ls()
            elif command.startswith("cd"):
                self._handle_cd(command)
            else:
                print(f"Команда не найдена: {command}")

    def _handle_ls(self):
        """Обработчик команды ls"""
        files = self.vfs.list_files()
        for file in files:
            print(file.name)

    def _handle_cd(self, command):
        """Обработчик команды cd"""

        _, dir_name = command.split(maxsplit=1)
        try:
            self.vfs.change_directory(dir_name)
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
    shell = Shell(vfs)
    shell.hostname = args.hostname
    shell.run()

if __name__ == "__main__":
    main()
