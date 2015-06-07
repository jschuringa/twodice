import operator

def startSearch(userCulture, userSkills, compCultureDict, compJobDict):
    matchDict = cultureMatch(userCulture, compCultureDict)
    matchDict = skillMatch(matchDict, userSkills, compJobDict)
    return matchDict

def cultureMatch(userCulture, compCultureDict):
    cultureMatchDict = {}
    cultureScore = 0
    for key, value in compCultureDict:
        cultureScore = 0
        for i in range(0, len(userCulture)):
            for j in range(0, len(value)):
                if userCulture[i] == value[j]:
                    cultureScore += abs(i - j)
        cultureMatchDict[key] = cultureScore

    sortedList = sorted(cultureMatchDict.items(), key=operator.itemgetter(1))
    return dict(sortedList)

    
def skillMatch(matchDict, userSkills, compJobDict):
    jobMatchList = []
    for key, value in matchDict:
        for comp, dict in compJobDict:
            if key == comp:
                for job, skills in dict:
                    for i in userSkills:
                        for j in skills:
                            if i == j:
                                jobMatchList.append(job)
            break
    return jobMatchList




