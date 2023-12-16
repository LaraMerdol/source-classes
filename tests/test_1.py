import unittest
import json
import os
from sourceclasses import GitCommit
from sourceclasses import GithubPr
from sourceclasses import JiraIssue

class TestSimple(unittest.TestCase):
    def setUp(self):
        # Set up common resources here
        file_path = os.path.join("data", "0_github-pr__2023-12-14 20.32.46.json")
        with open(file_path, encoding="utf-8") as f:
            self.lines = f.readlines()
            self.artifacts = [json.loads(line, strict=False)["data"] for line in self.lines]

    def tearDown(self):
        # Clean up resources if needed
        pass

    def test_module_path(self):
        number = GithubPr(self.artifacts[0]).getUniqueId()
        self.assertEqual(number, 6)

if __name__ == '__main__':
    unittest.main()
