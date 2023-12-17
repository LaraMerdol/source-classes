import unittest
from datetime import datetime, timezone
from dateutil import parser
import json
import os
from sourceclass import JiraIssue

class TestJiraIssue(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join("data", "0_jira__2023-12-17.json")
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
        self.jira_issue = JiraIssue(self.artifacts[0])

    def test_getId(self):
        self.assertEqual(self.jira_issue.getId(), "ANY23-22")

    def test_getTitle(self):
        self.assertEqual(self.jira_issue.getTitle(), "Edit trunk/lib/install-deps.sh to point to correct repos for dependencies")

    def test_getReporter(self):
        self.assertEqual(self.jira_issue.getReporter(), "Lewis John McGibbney")

    def test_getAssignee(self):
        self.assertEqual(self.jira_issue.getAssignee(), "Lewis John McGibbney")

    def test_getCreatedDate(self):
        expected_date = parser.parse("2012-01-03T14:44:12.000+0000").replace(tzinfo=timezone.utc)
        self.assertEqual(self.jira_issue.getCreatedDate(), expected_date)

    def test_getUrl(self):
        expected_url = "https://issues.apache.org/jira/browse/ANY23-22"
        self.assertEqual(self.jira_issue.getUrl(), expected_url)

    def test_getGithubPullRequestIds(self):
        expected_pr_ids = []
        self.assertEqual(self.jira_issue.getGithubPullRequestIds("https://github.com/apache/any23"), expected_pr_ids)

    def test_getCommitIds(self):
        expected_commit_ids = []
        self.assertEqual(self.jira_issue.getCommitIds(), expected_commit_ids)

    def test_getIssueType(self):
        expected_issue_type = "Task"
        self.assertEqual(self.jira_issue.getIssueType(), expected_issue_type)

    def test_getPriority(self):
        expected_priority = "Major"
        self.assertEqual(self.jira_issue.getPriority(), expected_priority)

    def test_getResolutionDate(self):
        expected_resolution_date = parser.parse("2012-01-05T12:42:10.000+0000").replace(tzinfo=timezone.utc)
        self.assertEqual(self.jira_issue.getResolutionDate(), expected_resolution_date)

    def test_getAllEventsDates(self):
        expected_dates = [parser.parse("2012-01-03T14:44:12.000+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-03T14:45:47.140+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:41:39.015+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:42:10.649+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:42:18.150+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:42:10.649+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-03T14:45:47.081+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-03T14:45:47.081+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:42:10.644+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:42:10.644+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-06T07:32:53.639+0000").replace(tzinfo=timezone.utc),
                          parser.parse("2012-01-05T12:42:10.644+0000").replace(tzinfo=timezone.utc)]
        expected_sorted_dates = sorted(set(expected_dates))
        self.assertEqual(self.jira_issue.getAllEventsDates(), expected_sorted_dates)

    def test_getStatus(self):
        expected_status = "Closed"
        self.assertEqual(self.jira_issue.getStatus(), expected_status)

    def test_getAssigner(self):
        expected_assigner = "Lewis John McGibbney"
        self.assertEqual(self.jira_issue.getAssigner(), expected_assigner)

    def test_getReopenCount(self):
        expected_reopen_count = 0
        self.assertEqual(self.jira_issue.getReopenCount(), expected_reopen_count)

    def test_getAssigneeChange(self):
        expected_assignee_change = []
        self.assertEqual(self.jira_issue.getAssigneeChange(), expected_assignee_change)

    def test_getResolver(self):
        expected_resolver = "Lewis John McGibbney"
        self.assertEqual(self.jira_issue.getResolver(), expected_resolver)

    def test_getCloser(self):
        expected_closer = "Lewis John McGibbney"
        self.assertEqual(self.jira_issue.getCloser(), expected_closer)

    def test_getCloseDate(self):      
        expected_close_date = parser.parse("2012-01-05T12:42:18.150+0000").replace(tzinfo=timezone.utc)
        self.assertEqual(self.jira_issue.getCloseDate(), expected_close_date)

    def test_getFixedVersions(self):
        expected_fixed_versions = []
        self.assertEqual(self.jira_issue.getFixedVersions(), expected_fixed_versions)

    def test_getAffectedVersions(self):
        expected_affected_versions = []
        self.assertEqual(self.jira_issue.getAffectedVersions(), expected_affected_versions)

    def test_isDuplicate(self):
        self.assertFalse(self.jira_issue.isDuplicate())

    def test_getEnvironment(self):
        self.assertEqual(self.jira_issue.getEnvironment(), None)

    def test_getLinkedIssues(self):
        expected_linked_issues = []
        self.assertEqual(self.jira_issue.getLinkedIssues(), expected_linked_issues)

if __name__ == '__main__':
    unittest.main()