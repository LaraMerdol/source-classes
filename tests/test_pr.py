import unittest
from datetime import datetime, timezone
from dateutil import parser
import json
import os
from sourceclass import GithubPr

class TestSimple(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join("data", "0_github-pr__2023-12-17.json")
        with open(file_path, encoding="utf-8") as f:
            self.lines = f.readlines()
            self.artifacts = []
            for line in self.lines:
                try:
                    data = json.loads(line, strict=False)
                    # Ensure that the loaded JSON has the "data" key
                    if "data" in data and isinstance(data["data"], dict):
                        self.artifacts.append(data["data"])
                    else:
                        print(f"Invalid JSON structure: {data}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        self.pr = GithubPr(self.artifacts[0])

    def test_1(self):
        test_pr = {
            "prId": self.pr.getUniqueId(),
            "prTitle": self.pr.getTitle(),
            "author": self.pr.getOpener(),
            "reviewers": self.pr.getReviewers(),
            "createdAt": self.pr.getDateCreated(),
            "prUrl": self.pr.getUrl(),
            "issueIds": self.pr.getReferencedIssues("ANY-23"),
            "numberOfCommits": self.pr.getNumberOfCommits(),
            "numberOfChangeFiles": self.pr.getNumberOfChangeFiles(),
            "changeLineOfCode": self.pr.getChangeLineOfCode(),
            "merger": self.pr.getMerger(),
            "mergeStatus": self.pr.isMerged(),
            "headBranch": self.pr.getHeadBranchName(),
            "closeDate": self.pr.getDateClosed()
        }

        control_pr = {
            "prId": 6,
            "prTitle": "Fix FOAF namespace",
            "author": "Stephane Corlosquet",
            "reviewers": [],
            "createdAt": parser.parse('2014-05-11T12:15:14Z').replace(tzinfo=timezone.utc),
            "prUrl": "https://github.com/apache/any23/pull/6",
            "issueIds": [],
            "numberOfCommits": 1,
            "numberOfChangeFiles": 7,
            "changeLineOfCode": 20,
            "merger": "asfgit",
            "mergeStatus": True,
            "headBranch": "foaf-ns-fix",
            "closeDate": parser.parse('2014-05-12T01:37:18Z').replace(tzinfo=timezone.utc),
        }

        for key in control_pr:
            with self.subTest(key=key):
                self.assertEqual(test_pr[key], control_pr[key])

if __name__ == '__main__':
    unittest.main()