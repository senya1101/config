import subprocess
import os
import xml.etree.ElementTree as ET
from langchain_core.runnables.graph_mermaid import draw_mermaid_png
from python_mermaid.diagram import MermaidDiagram, Node, Link
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
    print(commits)
    return commits


def generate_mermaid_code(commit_dependencies):
    links: list[Link]=[]
    nodes: list[Node]=[]
    for commit, parents in commit_dependencies.items():
        nodes.append(Node(commit))
        if len(parents)!=0:
            for parent in parents:
                links.append(Link(Node(parent), Node(commit)))

    mermaid_code = MermaidDiagram(title="Dependencies graph", nodes=nodes, links=links)
    return str(mermaid_code)


def generate_graph_with_mermaid(mermaid_code, mermaid_path, output_path):
    draw_mermaid_png(mermaid_syntax=mermaid_code, output_file_path=output_path)




def main():
    config = read_config(Path("config/config.xml"))

    # Получаем зависимости
    commit_dependencies = get_commit_dependencies(config["repo_path"])

    # Генерируем граф Mermaid
    mermaid_code = generate_mermaid_code(commit_dependencies)
    output_path = Path(config["output_path"])
    # Генерируем изображение
    generate_graph_with_mermaid(mermaid_code, config["mermaid_path"], output_path)


    print(f"Граф зависимостей успешно сгенерирован и сохранен в {config['output_path']}")

if __name__ == "__main__":
    main()

