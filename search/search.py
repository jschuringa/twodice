import operator

def startSearch(userCulture, userSkills, compCultureDict, compJobDict):
    matchDict = cultureMatch(userCulture, compCultureDict)
    matchDict = skillMatch(matchDict, userSkills, compJobDict)
    return matchDict

def cultureMatch(userCulture, compCultureDict):
    cultureMatchDict = {}
    for key in compCultureDict:
        cultureScore = 0
        value=compCultureDict[key]
        cultureScore = cultureMatchSingle(userCulture, value)
        cultureMatchDict[key] = cultureScore

    sortedList = sorted(cultureMatchDict.items(), key=operator.itemgetter(1))
    return dict(sortedList)

    
def skillMatch(matchDict, userSkills, compJobDict):
    jobMatchList = {}
    for key in matchDict:
        value = matchDict[key]
        for comp in compJobDict:
            dic = compJobDict[comp]
            if key == comp:
                for job in dic:
                    skills = dic[job]
                    match = 0
                    for i in userSkills:
                        for j in skills:
                            if i == j:
                                match += 1
                    jobMatchList[job] = [value, match]
                break
    return jobMatchList

def cultureMatchSingle(userCulture, studCulture):
    cultureScore = 0
    for i in range(0, len(userCulture)):
        for j in range(0, len(studCulture)):
            if userCulture[i] == studCulture[j]:
                cultureScore += abs(i - j)
    cultureScore = 100 - cultureScore * 2
    return cultureScore

def skillMatchSingle(userSkills, studSkills):
    match = 0
    for i in userSkills:
        for j in studSkills:
            if i == j:
                match += 1
    return match
    

