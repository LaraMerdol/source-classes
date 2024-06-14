import re
from datetime import datetime, timezone
from dateutil import parser
import time

class GitCommit:
        
    def __init__(self, data):
        self.data = data

    def getUniqueId(self):
        return self.data["commit"]
    
    def getAuthor(self):
        try:
            author = {
                "name":self.data["Author"].split("<")[0].strip(),
                "email":self.data["Author"].split("<")[1].strip().split(">")[0].strip() 
            }
            return author
        except (KeyError, TypeError):
            return None        
    
    def getCommitDate(self):
        try:
            return parser.parse(self.data["AuthorDate"] ).replace(tzinfo=timezone.utc)
        except (KeyError, TypeError):
            return None         
    
    def getModifiedFilePaths(self):
        files = []
        for file_instance in self.data.get("files", []):
            added = file_instance.get("added", None)
            created = False
            removed = file_instance.get("removed", None)
            deleted =False
            if added is not None and removed is not None and added != '-' and removed != '-':
                change_loc = added + removed
            else:
                change_loc = 0
            if file_instance.get("action") and file_instance.get("action") == "D":
                deleted = True
            if file_instance.get("action") and file_instance.get("action") == "A":
                created = True           
            file = {
                "name": file_instance.get("file", ""),
                "changeLOC": change_loc,
                "deleted": deleted,
                "created": created
            }
            files.append(file)
        return files
    
    def getRenamedFilePairs(self):
        pairs = []
        for file in self.data["files"]:
            if "newfile" in file:
                oldFile = file["file"]
                newFile = file["newfile"]
                pairs.append((oldFile, newFile))
        return pairs
    

    def getReferencedIssues(self, projectName):
        regex = f"({projectName}-\\d+)"
        compiled_regex = re.compile(regex)
        message = self.data.get("message", "")
        issues = compiled_regex.findall(message)
        return list(map(str.upper, set(issues)))