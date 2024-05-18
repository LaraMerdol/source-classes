import re
from datetime import timezone
from dateutil import parser


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

    def getCoAuthor(self):
        result = []
        try:
            # Co-author information is found in the following format in git data
            # { ... "message": "...\n\n Co-authored-by: name <email>", ..}
            data = self.data["message"].split("Co-authored-by:")
            if len(data) > 1:
                co_authors = data[1:]
                for co_author in co_authors:
                    result.append({
                        "name": co_author.split("<")[0].strip(),
                        "email": co_author.split("<")[1].strip().split(">")[0].strip()
                    })
            return result
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
            removed = file_instance.get("removed", None)

            if added is not None and removed is not None and added != '-' and removed != '-':
                change_loc = added + removed
            else:
                change_loc = 0

            file = {
                "name": file_instance.get("file", ""),
                "changeLOC": change_loc
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
