import unittest
from unittest.mock import patch, MagicMock


# Assuming your script is named `dependency_visualizer.py`
from hw2.src.dependency_visualizer import (
    read_config,
    get_commit_dependencies,
    generate_mermaid_code,
    generate_graph_with_mermaid,
)

class TestDependencyVisualizer(unittest.TestCase):

    @patch('xml.etree.ElementTree.parse')
    def test_read_config(self, mock_parse):
        # Arrange
        mock_tree = MagicMock()
        mock_root = MagicMock()
        mock_parse.return_value = mock_tree
        mock_tree.getroot.return_value = mock_root

        # Setting up the return values of XML parsing
        mock_root.find.side_effect = [
            MagicMock(text='path/to/mermaid'),
            MagicMock(text='path/to/repo'),
            MagicMock(text='path/to/output')
        ]

        # Act
        config = read_config('dummy_config_path')

        # Assert
        expected_config = {
            "mermaid_path": 'path/to/mermaid',
            "repo_path": 'path/to/repo',
            "output_path": 'path/to/output'
        }
        self.assertEqual(config, expected_config)

    @patch('subprocess.run')
    def test_get_commit_with_one_parent_dependencies(self, mock_run):
        # Arrange
        mock_run.return_value.stdout = "a2b3c4d\na1b2c3d a2b3c4d"
        repo_path = "dummy_path"
        expected_commits = {
            "a2b3c4d": [],
            "a1b2c3d": ["a2b3c4d"]
        }

        # Act
        dependencies = get_commit_dependencies(repo_path)

        # Assert
        self.assertEqual(dependencies, expected_commits)

    @patch('subprocess.run')
    def test_get_commit_with_parents_dependencies(self, mock_run):
        # Arrange
        mock_run.return_value.stdout = "a2b3c4d\na1b2c3d a2b3c4d a2b35yhd"
        repo_path = "dummy_path"
        expected_commits = {
            "a2b3c4d": [],
            "a1b2c3d": ["a2b3c4d", "a2b35yhd"]
        }

        # Act
        dependencies = get_commit_dependencies(repo_path)

        # Assert
        self.assertEqual(dependencies, expected_commits)

    def test_generate_mermaid_code(self):
        # Arrange
        commit_dependencies = {
            "a2b3c4d": [],
            "a1b2c3d": ["a2b3c4d"]
        }

        # Act
        mermaid_code = generate_mermaid_code(commit_dependencies)

        # Assert
        expected_mermaid_code = "a1b2c3d --> a2b3c4d"
        self.assertIn('---\ntitle: Dependencies graph\n---\ngraph \na2b3c4d["a2b3c4d"]\na1b2c3d["a1b2c3d"]\na2b3c4d ---> a1b2c3d', mermaid_code)



if __name__ == '__main__':
    unittest.main()
