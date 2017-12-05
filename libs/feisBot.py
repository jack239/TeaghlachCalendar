# -*- coding: utf-8 -*-
from botUtils import createMarkup
from feis import getSchoolCompetions, schoolsList, schoolCitys, getParticioiants, getDancerCompetions, getName
from feis import cityStat, schoolStat, danceStat
def getSchoolButton():
    keys = []
    for id, sc in enumerate(schoolsList):
        keys.append(((sc, 'feiss {}'.format(id)), ))
    return createMarkup(keys)

def getSchoolCityButton(schoolID):
    keys = []
    for id, sc in enumerate(schoolCitys[schoolsList[schoolID]]):
        keys.append(((sc, u'feiss {} {}'.format(schoolID, id)), ))
    keys.append(((u'Все', u'feiss {} {}'.format(schoolID, -1)), ))
    keys.append(((u'По ученикам', u'feisp {}'.format(schoolID)), ))
    return createMarkup(keys)


def getParticipiantButton(schoolID):
    keys = []
    for id, p in enumerate(getParticioiants(schoolID)):
        keys.append(((p, 'feisp {} {}'.format(schoolID, id)), ))
    return createMarkup(keys)

def feisCallback(bot, chat_id, data):
    if data[0] == 'feiss':
        if len(data) == 1:
            markup = getSchoolButton()
            bot.sendMessage(chat_id, 'Выберите школу', reply_markup=markup)
        elif len(data) == 2:
            markup = getSchoolCityButton(int(data[1]))
            bot.sendMessage(chat_id, 'Выберите город', reply_markup=markup)
        elif len(data) == 3:
            school = schoolsList[int(data[1])]
            if data[2] == '-1':
                city = None
                bot.sendMessage(chat_id, u'Расписание для {}\n'.format(school))
            else:
                city = schoolCitys[school][int(data[2])]
                bot.sendMessage(chat_id, u'Расписание для {} {}\n'.format(school, city))
            res = []
            for r in getSchoolCompetions(school, city):
                if 'Competition' in r and res:
                    bot.sendMessage(chat_id, u'\n'.join(res))
                    res = []
                res.append(r)
            bot.sendMessage(chat_id, u'\n'.join(res))
    if data[0] == 'feisp':
        if len(data) == 2:
            markup = getParticipiantButton(int(data[1]))
            bot.sendMessage(chat_id, 'Выбирите ученика', reply_markup=markup)
        if len(data) == 3:
            name = getName(int(data[1]), int(data[2]))
            bot.sendMessage(chat_id, u'Расписание для {}\n'.format(name))
            res = getDancerCompetions(name)
            bot.sendMessage(chat_id, u'\n'.join(res))
    if data[0] == 'feisStat':
        if len(data) == 1:
            keys = [(('Статистика по городам', 'feisStat city'),),
                    (('Статистика по школам', 'feisStat school'),),
                   (('Статистика по танцам', 'feisStat dance'),),]
            markup = createMarkup(keys)
            bot.sendMessage(chat_id, 'Что вы хотите узнать', reply_markup=markup)

        if len(data) == 2:
            if data[1] == 'city':
                stat = cityStat
            elif data[1] == 'school':
                stat = schoolStat
            elif data[1] == 'dance':
                stat = danceStat
            else:
                bot.sendMessage(chat_id, u'А ее пока нет')
                return
            res = [u'{} {}'.format(*s) for s in stat]
            bot.sendMessage(chat_id, u'\n'.join(res))
