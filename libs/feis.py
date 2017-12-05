import xlrd, xlwt
from collections import Counter
rb = xlrd.open_workbook('stage_lists_december.xls', formatting_info=True)
rsheet = rb.sheet_by_index(0)
partIDS = [(0, 'id'), (1, 'name'), (2, 'age'), (3, 'school'), (4, 'city')]
compIDS = [(0, 'name'), (2, 'age'), (4,'dance')]

competitions = []
participants = {}
schools = {}
schoolsList = []
schoolCitys = {}
cityStat = None
schoolStat = None
danceStat = None
def creatParticipant(row):
    return {f: row[fid] for fid, f in partIDS}

def getDancer(row):
    global participants
    name = row[1]
    dancer = participants.get(name)
    if dancer is None:
        dancer = participants[name] = creatParticipant(row)
        dancer['comps'] = []
    return dancer
        
        

def creatCompetition(row):
    return {f: row[fid] for fid, f in compIDS}

def collectFeisInfo():
    global competitions
    competitions = []

    for rownum in xrange(rsheet.nrows):
        row = rsheet.row_values(rownum)
        if type(row[0]) == unicode and 'Competition' in row[0]:
            cid = len(competitions)
            comp = creatCompetition(row)
            isCeili = 'hand' in comp['dance']
            competitions.append(comp)
        elif type(row[0]) == float and not isCeili:
            dancer = getDancer(row)
            dancer['comps'].append(cid)
        elif type(row[0]) == float and isCeili:
            for name in row[2].split(','):
                dancer = participants.get(name.strip())
                if dancer:
                    dancer['comps'].append(cid)
            
    
    global schools, schoolCitys, schoolsList
    schools = {}
    schoolsList = []
    schoolCitys = {}

    for p in participants.itervalues():
        school = p['school']
        if school not in schools:
            schools[school] = []
            schoolCitys[school] = set()
        schools[school].append(p['name'])
        schoolCitys[school].add(p['city'])
    schoolsList = sorted(schools.keys())
    for sc in schoolCitys.iterkeys():
        schools[sc] =  sorted(schools[sc])
        schoolCitys[sc] = sorted(schoolCitys[sc])

    global cityStat, schoolStat, danceStat
    cityStat = Counter([p['city'] for p in participants.itervalues()]).items()
    cityStat.sort(key = lambda x: (-x[1], x[0]))
    schoolStat = Counter([p['school'] for p in participants.itervalues()]).items()
    schoolStat.sort(key = lambda x: (-x[1], x[0]))
    dances = [c1 for p1 in participants.itervalues() for c1 in p1['comps'] ]
    danceStat = Counter([competitions[d]['dance'] for d in dances]).items()
    danceStat.sort(key = lambda x: (-x[1], x[0]))
    
collectFeisInfo()


def getSchoolCompetions(school, city):
    preres = []
    for name in schools[school]:
        part = participants[name]
        if city and part['city'] != city:
            continue

        for c in part['comps']:
            preres.append((c, part['name']))
    preres.sort()
    res = []
    cid = None
    for c, name in preres:
        if c != cid:
            comp = competitions[c]
            if res:
                res.append('\n')
            res.append(' '.join((comp['name'], comp['dance'], comp['age'])))
            cid = c
        res.append(name)
    return res

def getDancerCompetions(name):
    for comp in [competitions[c] for c in participants[name]['comps']]:
        yield ' '.join((comp['name'], comp['dance']))

def getParticioiants(scoolID):
    return schools[schoolsList[scoolID]]

def getName(scoolID, pid):
    return schools[schoolsList[scoolID]][pid]
