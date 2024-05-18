import unittest
from datetime import timezone
from dateutil import parser
import json
import os
from sourceclass import GitCommit


class TestGitCommit(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join("data", "0_git__2023-12-17.json")
        with open(file_path, encoding="utf-8") as f:
            self.lines = f.readlines()
            self.artifacts = []
            for line in self.lines:
                try:
                    data = json.loads(line, strict=False)
                    if "data" in data and isinstance(data["data"], dict):
                        self.artifacts.append(data["data"])
                    else:
                        print(f"Invalid JSON structure: {data}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        self.git_commit = GitCommit(self.artifacts[0])    


    def test_getUniqueId(self):
        self.assertEqual(self.git_commit.getUniqueId(), "322d9d5c6bb92888f8fe98cba1db635bace799bc")

    def test_getAuthor(self):
        expected_author = {"name": "Michele Mostarda", "email": "dev-null@apache.org"}
        self.assertEqual(self.git_commit.getAuthor(), expected_author)

    def test_getCommitDate(self):
        expected_date = parser.parse("Thu Dec 18 17:56:05 2008 +0000").replace(tzinfo=timezone.utc)
        self.assertEqual(self.git_commit.getCommitDate(), expected_date)

    def test_getModifiedFilePaths(self):
        expected_files = []
        self.assertEqual(self.git_commit.getModifiedFilePaths(), expected_files)

    def test_getRenamedFilePairs(self):
        expected_pairs = []
        self.assertEqual(self.git_commit.getRenamedFilePairs(), expected_pairs)

    def test_getReferencedIssues(self):
        expected_issues = []
        self.assertEqual(self.git_commit.getReferencedIssues("ANY-23"), expected_issues)

if __name__ == '__main__':
    unittest.main()