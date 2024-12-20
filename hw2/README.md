# Задание №2: Разработать инструмент командной строки для визуализации графа зависимостей

## 1. Общее описание
Этот проект реализует инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Зависимости определяются для git-репозитория. Для описания графа зависимостей используется 
представление Mermaid. Визуализатор выводит результат в виде сообщения об
успешном выполнении и сохраняет граф в файле формата png.
---
Конфигурационный файл имеет формат json и содержит:
+ Путь к программе для визуализации графов.
+ Путь к анализируемому репозиторию.
+ Путь к файлу с изображением графа зависимостей.


Все функции визуализатора зависимостей покрыты тестами

### Архитектура
`hw2`
+ `config`
  + config.xml
+ `result` 
  + output.png
+ `src`
  + dependencies_visualizer.py
+ `tests`
  + tests.py


---

---

## 2. Описание всех функций и настроек

#### `read_config(config_path)`
```Python
    def read_config(config_path):
        tree = ET.parse(config_path)
        root = tree.getroot()
        config = {
            "mermaid_path": root.find('visualizer_path').text,
            "repo_path": root.find('repo_path').text,
            "output_path": root.find('output_path').text
        }
        return config
```
- **Описание**: Функция считывает конфигурационный XML-файл, чтобы извлечь пути, необходимые для создания диаграммы Mermaid.
- **Параметры**:
  - `config_path`: Путь до xml-файла

---

#### `get_commit_dependencies(repo_path)`
```Python
    def get_commit_dependencies(repo_path):
        command = 'git log --pretty=format:"%h %p" --reverse'
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
    
        commits = {}
    
        for line in result.stdout.splitlines():
            parts = line.split()
            commit_id = parts[0]
            if len(parts)!=1:
                parents = parts[1:]
                commits[commit_id] = parents
            else:
                commits[commit_id]=[]
        return commits
```
- **Описание**: Выполняет комманду и получает хэш коммита и его родителей и возвращает словарь с установленными зависимостями
- **Параметры**:
  - `repo_path`: Путь до репозитория
  

---

#### `generate_mermaid_code(commit_dependencies)`
```Python
    def generate_mermaid_code(commit_dependencies):
        mermaid_code = 'graph TD\n'
        for commit, parents in commit_dependencies.items():
            for parent in parents:
                mermaid_code+=f"    {parent} --> {commit}\n"
        return mermaid_code
```
- **Описание**: Генерирует код необходимый для графа
- **Параметры**:
  - `commit_dependencies`: Зависимости коммитов

---

#### `generate_graph(mermaid_code, mermaid_path, output_path):`
```Python
    def generate_graph(mermaid_code, mermaid_path, output_path):
      with open('graph.mmd', 'w') as f:
          f.write(mermaid_code)
  
      os.system(f"{mermaid_path} -i graph.mmd -o {output_path}")
  
      os.remove('graph.mmd')
```
- **Описание**: Генерирует граф и сохраняет в png по указанному пути
- **Параметры**:
  - `mermaid_code`: Mermaid код 
  - `output_path`: Путь до изображения
  - `mermaid_path`: Путь до программы визуализатора

---



#### `main():`
```Python
   def main():
        os.system("pip install -r requirements.txt")
        
        config = read_config(Path("config/config.xml"))

        # Получаем зависимости
        commit_dependencies = get_commit_dependencies(config["repo_path"])
    
        # Генерируем граф Mermaid
        mermaid_code = generate_mermaid_code(commit_dependencies)
        output_path = Path(config["output_path"])
        # Генерируем изображение
        generate_graph(mermaid_code, config["mermaid_path"], output_path)
    
        print(f"Граф зависимостей успешно сгенерирован и сохранен в {config['output_path']}")

```
- **Описание**: Основная функция. Осуществляет вызовы остальных функций и оперирует полученными данными.


---

---

## 3. Описание команд для сборки проекта
Для работы с проектом необходимо иметь установленный Python 3.12

### Запуск проекта
Сначала необходимо перейти в рабочую директорию ```hw2```.
```bash
cd hw2
```

#### Установка зависимостей
В данном проекте используются сторонние библиотеки python, поэтому перед выполнением основных функций происходит установка.

#### Настройки для работы программы
В файле ```./config/config.xml``` находиться файл с настройками проекта.
В нем можно поменять:
1. ```package_name``` - путь до локального репозитория
2. ```graph_output_path``` - путь к файлу с расширением .png, в котором будет хранить рисунок полученного графа
3. ```visualizer_path``` - путь до программы визуализатора


Далее выполняем команду для запуска программы
```bash
python 'src/dependency_visualizer.py'
```

---

---

## 4. Пример использования в виде скриншотов
### Удачное завершение
![example_of_use](https://github.com/senya1101/config/blob/images/hw2/img/2024-11-20%2000_44_45-config%20%E2%80%93%20dependency_visualizer.py.png?raw=true )
### Граф зависимостей этого репозитория
![example_of_use](https://github.com/senya1101/config/blob/images/hw2/img/output1.png?raw=true )
### Пример графа зависимостей другого репозитория(с merge-коммитами)
![example_of_use](https://github.com/senya1101/config/blob/images/hw2/img/output.png?raw=true )

## 5. Результаты прогона тестов
![test](https://github.com/senya1101/config/blob/images/hw2/img/2024-11-20%2000_17_52-config%20%E2%80%93%20dependency_visualizer.py.png?raw=true )
