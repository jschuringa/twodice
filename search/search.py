


def startSearch(userVals, userSkills, jobSkills, compVals, compCutoff):
    cultureMatchList = getMatchOnCulture(userList, compVals, compCutoff)
    fullMatchList = getMatchOnSkills(cultureMatchList, userList)
    
def getMatchOnCulture(userLIst, compVals, compCutoff):
    matchList = []
    for key, value in self.userList:
        if (checkvals(value) < self.compCutoff):
            matchList.append(key)
    return matchList  

def checkVals(userVals):
        



