class search:

    matchList = []

    def __init__(self, userList, compVals, compCutoff):
        self.userList = userList
        self.compVals = compVals
        self.compCutoff = compCutoff
        returnMatch()
    
    def returnMatch():
        for key, value in self.userList:
            if (checkvals(value) < self.compCutoff):
                matchList.append(key)
        
    def checkVals(userVals):
        



