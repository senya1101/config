import subprocess
import os
import xml.etree.ElementTree as ET
from pathlib import Path


def read_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        "mermaid_path": root.find('visualizer_path').text,
        "repo_path": root.find('repo_path').text,
        "output_path": root.find('output_path').text
    }
    return config

def get_commit_dependencies(repo_path):
    # Получаем все коммиты с их родительскими коммитами
    command = ["git", "log", "--oneline", "--parents", "--reverse", "--no-merges"]
    result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)

    commits = {}

    for line in result.stdout.splitlines():
        parts = line.split()
        commit_id = parts[0]
        if parts[1]=="Initial":
            commits[commit_id]=""# " ".join(str(commit_name) for commit_name in parts[1:])
        else:
            parent = parts[1]  #Родительский коммит(только один родитель тк слияния исключены)
            commits[commit_id] = parent# +" " + " ".join(str(commit_name) for commit_name in parts[2:])

    return commits


def generate_mermaid_graph(commit_dependencies):
    mermaid_code = "graph TD\n"

    for commit, parent in commit_dependencies.items():
            mermaid_code += f"  {parent} --> {commit}\n"
    return mermaid_code


def generate_graph_with_mermaid(mermaid_code, mermaid_path, output_path):
    # Создаем временный файл для хранения кода Mermaid
    with open("graph.mmd", "w") as f:
        f.write(mermaid_code)
    # Запускаем mermaid-cli для генерации PNG
    command = ['npx', mermaid_path, "graph.mmd", "-o", os.path.dirname(output_path), "-t", "png"]
    subprocess.run(command)




def main(config_path):
    config = read_config(config_path)

    # Получаем зависимости
    commit_dependencies = get_commit_dependencies(config["repo_path"])

    # Генерируем граф Mermaid
    mermaid_code = generate_mermaid_graph(commit_dependencies)
    output_path = Path(config["output_path"])
    # Генерируем изображение
    generate_graph_with_mermaid(mermaid_code, config["mermaid_path"], output_path)

    # Удаляем временный файл
    os.remove("graph.mmd")

    print(f"Граф зависимостей успешно сгенерирован и сохранен в {config['output_path']}")

if __name__ == "__main__":
    main(config_path=Path("config/config.xml"))

