import re
from datetime import datetime, timezone
from dateutil import parser
import time

class GithubPr:

    def __init__(self, data):
        self.data = data

    def getUniqueId(self):
        return self.data["number"]
    
    def getTitle(self):
        return self.data["title"]   
    
    def getOpener(self):
        return self.data["user_data"]["name"] or  self.data["user"]["login"]   

    def getCommits(self):
        return self.data["commits_data"]   
    
    def getReviewers(self):
        reviewers = []
        for review in self.data["reviews_data"]:
            if review["state"] == "PENDING" or review["body"] == "":
                continue
            reviewers.append(review["user-data"]["name"]or review["user_data"]["login"] )

        for reviewComment in self.data["review_comments_data"]:
            if reviewComment["user_data"] is None:
                continue
            reviewers.append( reviewComment["user_data"]["name"] or reviewComment["user_data"]["login"] )
        #WARNING
        return sorted(list(set(reviewers)))

    def getDateCreated(self):
        date = self.data["created_at"]
        return parser.parse(date).replace(tzinfo=timezone.utc)
    
    def getDateClosed(self):
        if self.data["merged"]:
            return parser.parse(self.data["merged_at"] ).replace(tzinfo=timezone.utc)  
        elif self.data["state"] == "closed":
            return  parser.parse(self.data["closed_at"] ).replace(tzinfo=timezone.utc) 
        else:  
            return None

    def getUrl(self):
        return self.data["html_url"]
    
    def getProjectName(self):
        return self.data["head"]["ref"].split("-")[0]
    
    def getReferencedIssues(self):
        regex = f"({self.getProjectName()}-\\d+)"
        compiledRegex = re.compile(regex, re.IGNORECASE)
        title = self.getTitle()
        body =self.data["body"]
        headBranch = self.getHeadBranchName()
        issues = re.findall(compiledRegex, "\n".join([headBranch, title, body]))
        return list(map(str.upper, set(issues)))

    def getNumberOfCommits(self):
        return self.data["commits"]

    def getNumberOfChangeFiles(self):
        return self.data["changed_files"]
      
    def getChangeLineOfCode(self):
        return self.data["additions"] + self.data["deletions"]
    
    def isMerged(self):
        return self.data["merged"]
    
    def getMerger(self):
        if (not self.isMerged()):
            return None
        return self.data["merged_by_data"]["name"]or self.data["merged_by_data"]["login"]
    
    def getCommits(self, commits_json_data):
        commits_data = []
        for commit in commits_json_data:
            commits_data.append({
                "commit_sha": commit["sha"],
                "commit_author": commit["commit"]["author"]["name"],
                "commit_date": self.timestamp(commit["commit"]["author"]["date"]),
            })
        return commits_data
    def getHeadBranchName(self):
        return self.data["head"]["ref"]
    
    def timestamp(self, dt):
        if isinstance(dt, str):
            dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(dt, int):
            dt = datetime.utcfromtimestamp(dt / 1000.0)  

        utime = int(time.mktime(dt.timetuple()) * 1000)
        return utime