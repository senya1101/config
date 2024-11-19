# Эмулятор для оболочки языка OS

## 1. Общее описание

Этот проект представляет собой эмулятор оболочки языка ОС, реализованный на Python. Эмулятор поддерживает базовые команды командной строки, такие как `ls`, `cd`, `exit`, `tree`, `history` и `chown`. Виртуальная файловая система загружается из архива zip.

### Основные особенности:
- Эмуляция команд UNIX-подобной оболочки.
- Поддержка виртуальной файловой системы, загружаемой из архива zip.
- Логирование всех действий пользователя.
- Поддержка базовых команд для работы с файлами и директориями.

### Структура проекта
```css
hw1/
├── config/
│   └── virtual_fs.tar # Виртуальная файловая система
├── src/
│   └── shell_emulator.py # Основной файл с программой
└── tests/
    └── test_shell_emulator.py # Файл с тестами
```

## 2. Описание всех функций и настроек

### Класс `VirtualFileSystem`

#### `__init__(self, zip_file)`

```Python
 def __init__(self, username, fs_path, log_path):
        def __init__(self, zip_file):
        self.zip_file = zip_file
        self.root = Path("root")  # Виртуальный корень
        self.current_path = self.root
        self.history = []
        self.filesystemdata = {}
        self.filesystem=[]
        self._load_vfs()  # Загружаем виртуальную файловую систему
```

- **Описание**: Инициализирует виртуальную файловую систему.
- **Параметры**:
  - `zip_file`: Путь к ZIP-архиву виртуальной файловой системы.
  

#### `load_filesystem(self)`

```Python
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

```

- **Описание**: Загружает виртуальную файловую систему из архива zip.

#### `list_files(self)`

```Python
    def list_files(self):
        current_dir = str(self.current_path)
        if current_dir in self.filesystem:
            return self.filesystem[current_dir]
        else:
            print("Директория пуста или не существует.")
            return []
```

- **Описание**: Возвращает список файлов и папок в текущем каталоге.

#### `change_directory(self, new_dir)`

```Python
    def change_directory(self, new_dir):
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
```

- **Описание**: Изменяет текущую директорию или переходит на уровень выше.

- **Параметры**:
  - `new_dir`: Путь к новой директории.

#### `print_tree(self, path=None, level=0)`

```Python
        def print_tree(self, path=None, level=0):
        """Рекурсивный вывод дерева каталогов."""
        if path == None:
            path = self.current_path

        current_dir = str(path)

        if current_dir in self.filesystem:
            for file in self.filesystem[current_dir]:
                print(' ' * level + file)

                self.print_tree(Path(current_dir)/Path(file), level + 4)
```

- **Описание**: Команда tree рекурсивно обходит все вложенные директории и файлы для выбранной директории.

- **Параметры**:
  - `new_dir`: Путь к новой директории.

#### `show_history(self)`

```Python
 def show_history(self):
        return '\n'.join(self.history)
```

- **Описание**: Выводит историю команд.

#### `change_owner(self, filename, owner)`

```Python
    def change_owner(self, filename, owner):
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
```

- **Описание**: Эмулирует изменение владельца файла..
- **Параметры**:
  - `filename`: Имя файла.
  - `owner`: Имя нового владельца.

### Класс `ShellEmulator`

#### `__init__(self, vfs)`

```Python
    def __init__(self, vfs):
        self.vfs = vfs
        self.hostname = 'localhost'
```
- **Описание**: Инициализирует эмулятор оболочки.
- **Параметры**:
  - `vfs`: Виртуальная файловая система.

#### `run(self)`

```Python
    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.vfs.current_path} $ ").strip()
            self.vfs.history.append(command)
            if command == "exit":
                raise SystemExit
            elif command.startswith("ls"):
                self._handle_ls()
            elif command.startswith("cd"):
                self._handle_cd(command)
            elif command == "refresh":
                self._handle_refresh()
            elif command.startswith("tree"):
                self._handle_tree(command)
            elif command == "history":
                self._handle_history()
            elif command.startswith("chown"):
                self._handle_chown(command)
            else:
                print(f"Команда не найдена: {command}")
```

- **Описание**: Основной цикл эмулятора.

#### `_handle_ls(self)`

```Python
    def _handle_ls(self):
        files = self.vfs.list_files()
        for file in files:
             print(file)
```

- **Описание**: Обработчик команды ls.

#### `_handle_cd(self, command)`

```Python
        def _handle_cd(self, command):
          """Обработчик команды cd"""
          _, dir_name = command.split(maxsplit=1)
          try:
              self.vfs.change_directory(dir_name)
          except FileNotFoundError as e:
              print(e)
```

- **Описание**: Обработчик команды cd.



#### `_handle_tree(self, command=None)`

```Python
     def _handle_tree(self, command=None):
        """Обработчик команды tree"""
        if command=="tree":
            self.vfs.print_tree()
        else:
            _, path = command.split(maxsplit=1)
            self.vfs.print_tree(path)
```

- **Описание**: Обработчик команды tree.



#### `_handle_history(self)`

```Python
        def _handle_history(self):
        """Обработчик команды history"""
        for i, cmd in enumerate(self.vfs.history, 1):
            print(f"{i}: {cmd}")
```

- **Описание**: Обработчик команды history.



#### `_handle_chown(self, command)`

```Python
       def _handle_chown(self, command):
          """Обработчик команды chown"""
          _, file_name, user = command.split(maxsplit=2)
          try:
              self.vfs.change_owner(file_name, user)
          except FileNotFoundError as e:
              print(e)
```

- **Описание**: Обработчик команды chown.






## 3. Описание команд для сборки проекта

Для работы с проектом необходимо иметь установленный Python 3.12

### Клонирование репозитория:

```bash
git clone https://github.com/senya1101/config
cd config
```


### Запуск эмулятора:
```bash
python "src/shell_emulator.py"  "username"  "config/virt_fs.zip"
```
## 4. Пример использования:
![example_of_use](https://github.com/senya1101/config/blob/images/hw1/img/example_of_use.png?raw=true )

## 5. Результаты прогона тестов:

![tests](https://github.com/senya1101/config/blob/images/hw1/img/tests.png?raw=true )
