import unittest
from datetime import datetime, timezone
from dateutil import parser
import json
import os
from sourceclass import GithubPr

class TestGithubPr(unittest.TestCase):
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

    def test_prId(self):
        test_prId = self.pr.getUniqueId()
        control_prId = 6
        self.assertEqual(test_prId, control_prId)

    def test_prTitle(self):
        test_prTitle = self.pr.getTitle()
        control_prTitle = "Fix FOAF namespace"
        self.assertEqual(test_prTitle, control_prTitle)

    def test_author(self):
        test_author = self.pr.getOpener()
        control_author = "Stephane Corlosquet"
        self.assertEqual(test_author, control_author)

    def test_reviewers(self):
        test_reviewers = self.pr.getReviewers()
        control_reviewers = []
        self.assertEqual(test_reviewers, control_reviewers)

    def test_createdAt(self):
        test_createdAt = self.pr.getDateCreated()
        control_createdAt = parser.parse('2014-05-11T12:15:14Z').replace(tzinfo=timezone.utc)
        self.assertEqual(test_createdAt, control_createdAt)

    def test_prUrl(self):
        test_prUrl = self.pr.getUrl()
        control_prUrl = "https://github.com/apache/any23/pull/6"
        self.assertEqual(test_prUrl, control_prUrl)

    def test_issueIds(self):
        test_issueIds = self.pr.getReferencedIssues("ANY-23")
        control_issueIds = []
        self.assertEqual(test_issueIds, control_issueIds)

    def test_numberOfCommits(self):
        test_numberOfCommits = self.pr.getNumberOfCommits()
        control_numberOfCommits = 1
        self.assertEqual(test_numberOfCommits, control_numberOfCommits)

    def test_numberOfChangeFiles(self):
        test_numberOfChangeFiles = self.pr.getNumberOfChangeFiles()
        control_numberOfChangeFiles = 7
        self.assertEqual(test_numberOfChangeFiles, control_numberOfChangeFiles)

    def test_changeLineOfCode(self):
        test_changeLineOfCode = self.pr.getChangeLineOfCode()
        control_changeLineOfCode = 20
        self.assertEqual(test_changeLineOfCode, control_changeLineOfCode)

    def test_merger(self):
        test_merger = self.pr.getMerger()
        control_merger = "asfgit"
        self.assertEqual(test_merger, control_merger)

    def test_mergeStatus(self):
        test_mergeStatus = self.pr.isMerged()
        control_mergeStatus = True
        self.assertEqual(test_mergeStatus, control_mergeStatus)

    def test_headBranch(self):
        test_headBranch = self.pr.getHeadBranchName()
        control_headBranch = "foaf-ns-fix"
        self.assertEqual(test_headBranch, control_headBranch)

    def test_closeDate(self):
        test_closeDate = self.pr.getDateClosed()
        control_closeDate = parser.parse('2014-05-12T01:37:18Z').replace(tzinfo=timezone.utc)
        self.assertEqual(test_closeDate, control_closeDate)

if __name__ == '__main__':
    unittest.main()