import re
from datetime import timezone
from dateutil import parser


class JiraIssue:

    def __init__(self, data):
        self.data = data
    
    def getId(self):
        try:
            return self.data["key"]
        except (KeyError, TypeError):
            return None       
    
    def getTitle(self):
        try:
            return self.data["fields"]["summary"]
        except (KeyError, TypeError):
            return None
    
    def getReporter(self):
        try:
            return self.data["fields"]["reporter"]["displayName"] or self.data["fields"]["reporter"]["name"]
        except (KeyError, TypeError):
            return None        
    
    def getAssignee(self):
        try:
            return self.data["fields"]["assignee"]["displayName"] or self.data["fields"]["assignee"]["name"]
        except (KeyError, TypeError):
            return None               
    
    def getCreatedDate(self):
        return parser.parse(self.data["fields"]["created"] ).replace(tzinfo=timezone.utc) 
    
    def getUrl(self):
        try:
            return (
                "/".join(self.data["self"].split("/")[:-5])
                + "/browse/"
                + self.getId()
            )
        except (KeyError, TypeError):
            return None                 

    def getGithubPullRequestIds(self, url):
        try:
            regex = rf"(?:{re.escape(url)}/pull/(\d+)|GitHub Pull Request #(\d+))"
            compiled_regex = re.compile(regex, re.IGNORECASE)
            comments = [comment["body"] for comment in self.data.get("comments_data", []) if comment and comment["body"] is not None]
            history_items = [item["toString"] for history in self.data["changelog"]["histories"] for item in history["items"] if item["toString"] is not None]
            on_changelog = re.findall(compiled_regex, "\n".join(history_items))
            on_comments = re.findall(compiled_regex, "\n".join(comments))
            result = set(on_changelog).union(on_comments)
            non_empty_matches = [item for result_tuple in result for item in result_tuple if item and item.strip() != ""]
            return non_empty_matches
        except (KeyError, TypeError):
            return None 
            
    def  getCommitIds(self):
        try:        
            regex = rf"\bcommit\s+([0-9a-fA-F]{40})\b"
            compiled_regex = re.compile(regex, re.IGNORECASE)
            comments = [comment["body"] for comment in self.data.get("comments_data", []) if comment and comment.get("body")]
            on_comments = re.findall(compiled_regex, "\n".join(comments))
            non_empty_matches = [item for result_tuple in on_comments for item in result_tuple if item and item.strip() != ""]
            return non_empty_matches
        except (KeyError, TypeError):
            return None 
            
    def getIssueType(self):
        try:
            return self.data["fields"]["issuetype"]["name"]
        except (KeyError, TypeError):
            return None
    
    def getPriority(self):
        try:
            return self.data["fields"]["priority"]["name"]
        except (KeyError, TypeError):
            return None
       
    def getResolutionDate(self):
        try:
            if self.data["fields"]["resolutiondate"]:
                return parser.parse(self.data["fields"]["resolutiondate"] ).replace(tzinfo=timezone.utc) 
            return None
        except (KeyError, TypeError):
            return None
               
    def getAllEventsDates(self):
        histories = [history["created"] for history in self.data["changelog"]["histories"]]
        comments_created = [comment["created"] for comment in self.data["comments_data"]]
        comment_updated = [comment["updated"] for comment in self.data["comments_data"]]
        all_dates = histories + comments_created + comment_updated 
        date_objects = [parser.parse(date_str).replace(tzinfo=timezone.utc) for date_str in all_dates]
        date_objects.append(self.getCreatedDate())
        unique_sorted_dates = sorted(set(date_objects))
        return unique_sorted_dates        
    
    def getStatus(self):
        try:
            return self.data["fields"]["status"]["name"]
        except (KeyError, TypeError):
            return None        
    
    def getAssigner(self):
        try:
            histories = self.data["changelog"]["histories"]
            for history in reversed(histories):
                for item in history["items"]:
                    if item["field"] == "assignee" and  history["author"]:
                        return history["author"]["displayName"] or history["author"]["name"]
            return None
        except (KeyError, TypeError):
            return None   
        
    def getCommentsData(self):
        try:
            return self.data["comments_data"] if "comments_data" in self.data else None
        except (KeyError, TypeError):
            return None           

    def getReopenCount(self):
        reopenCount = 0
        reopenPeriods = []
        for index, history in  enumerate(self.data["changelog"]["histories"]):
            for item in history["items"]:
                if ((item["toString"]== "Reopened" and item["fromString"]=="Closed") 
                or (item["toString"]== "Resolved" and item["fromString"]=="Reopened")
                or (item["toString"]== "Closed" and item["fromString"]=="Reopened")):
                    reopenPeriods.append( history)
        for index, period in enumerate(reopenPeriods):  
            if index + 1 < len(reopenPeriods):
                first = parser.parse(period["created"] ).replace(tzinfo=timezone.utc)  
                second = parser.parse(reopenPeriods[index+1]["created"] ).replace(tzinfo=timezone.utc)   
                timeDifference = (second - first).total_seconds() / 60
                if abs(timeDifference) > 2: #Longer than 2 minutes
                    reopenCount +=1
            else:
               reopenCount +=1             
        return reopenCount
 
    def getAssigneeChange(self):
        assigneeChanges = []
        for history in self.data["changelog"]["histories"]:
            for item in history["items"]:
                if item["field"] == "assignee":
                    item["created"] = history["created"]
                    assigneeChanges.append(item)
        sortedAssigneeList = sorted(assigneeChanges, key=lambda d: d["created"])
        assigneeList = []
        index = 0  
        while index  < len(sortedAssigneeList):
            assigneeChange = sortedAssigneeList[index]
            if assigneeChange["toString"] is None  and index +1 < len(sortedAssigneeList):
                change = sortedAssigneeList[index + 1]
                change["fromString"] = assigneeChange["fromString"]
                assigneeList.append(change)
                index +=2 
            elif assigneeChange["toString"] is not  None and assigneeChange["fromString"] is not  None:
                assigneeList.append(sortedAssigneeList[index])
                index +=1
            else:
                index +=1
        returnList = []
        for index, assignee in enumerate(assigneeList):
            if index + 1 < len(assigneeList):           
                firstTime = parser.parse(assignee["created"] ).replace(tzinfo=timezone.utc) 
                secondTime =parser.parse(assigneeList[index + 1]["created"] ).replace(tzinfo=timezone.utc)  
                timeDifference = secondTime - firstTime
                timeDifferenceInMinutes = timeDifference.total_seconds() / 60
                if abs(timeDifferenceInMinutes) > 2:
                    returnList.append({
                        "from":assignee["fromString"],
                        "to":assignee["toString"],
                        "date":assignee["created"]
                    })      
        return returnList
    
    def getResolver(self):
        for history in  self.data["changelog"]["histories"]:
            for item in history["items"]:
                if item["field"] == "resolution" and item["toString"] and history["author"]:
                    return history["author"]["displayName"] or history["author"]["name"]
                if item["field"] == "status" and item["toString"].lower() == "resolved" and history["author"]:
                    return history["author"]["displayName"] or history["author"]["name"]
        return None   
         
    def getCloser(self):
        history = self.data["changelog"]["histories"]
        if len(history)>0:
            lastItem = history[-1]
            for item in  lastItem["items"]:
                if item["field"] == "status" and item["toString"]=="Closed" and lastItem["author"]:
                    return lastItem["author"]["displayName"] or lastItem["author"]["name"]
        return None
    
    def getCloseDate(self):
        history = self.data["changelog"]["histories"]
        if len(history)>0:
            lastItem = history[-1]
            for item in  lastItem["items"]:
                if item["field"] == "status" and item["toString"]=="Closed":
                    return  parser.parse(lastItem["created"] ).replace(tzinfo=timezone.utc)
        return None   
    
    def getFixedVersions(self):
        try:
            fixVersions = self.data["fields"]["fixVersions"]
            return [version["name"] for version in fixVersions]
        except (KeyError, TypeError):
            return None


    
    def getAffectedVersions(self):
        try:
            versions = self.data["fields"]["versions"]
            return [version["name"] for version in versions]
        except (KeyError, TypeError):
            return None

    
    def isDuplicate(self):
        histories = self.data["changelog"]["histories"]
        for history in histories:
            for item in history["items"]:
                if (item["field"] == "resolution"and item["toString"] == "Duplicate"):
                        return  True
        return False        

    def getEnvironment(self):
        try:
            return self.data["fields"]["environment"]
        except (KeyError, TypeError):
            return None
    
    def getLinkedIssues(self):
        try:
            return self.data["fields"]["issuelinks"]
        except (KeyError, TypeError):
            return None        
        