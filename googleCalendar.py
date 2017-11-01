# -*- coding: utf-8 -*-
import icalendar
import calendar
import urllib2
from datetime import datetime, timedelta
from dateutil.rrule import rruleset, rrulestr
from django.utils import timezone
cal = None

#import locale
#locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

#WeekDays = {
#    1: u'Понедельник',
#    2: u'Вторник',
#    3: u'Среда',
#    4: u'Четверг',
#    5: u'Пятница',
#    6: u'Суббота',
#    7: u'Воскресенье',
#}

def parse_recurrences(component, start, end):#recur_rule, start, exclusions):
    recur_rule = component.get('rrule').to_ical().decode('utf-8')
    startc = component.get('dtstart').dt
    exclusions = component.get('exdate')
    """ Find all reoccuring events """
    rules = rruleset()
    first_rule = rrulestr(recur_rule, dtstart=startc)
    rules.rrule(first_rule)
    if not isinstance(exclusions, list):
        exclusions = [exclusions]
    for xdate in exclusions:
        try:
            rules.exdate(xdate.dts[0].dt)
        except AttributeError:
            pass
    dates = []
    for rule in rules.between(start, end):
        dates.append(rule)
    return dates

def getCal():
    global cal
    if cal is None:
        fp = urllib2.urlopen('https://calendar.google.com/calendar/ical/teaghlach.spb%40gmail.com/public/basic.ics')
        cal = icalendar.Calendar().from_ical(fp.read())
    return cal

def getShedule(start, end):
    cal = getCal()
    shedule = []
    for component in cal.walk('VEVENT'):
        if component.get('rrule'):
            days = parse_recurrences(component, start, end)
            for day in  days:
                shedule.append((day, component))
    shedule.sort()
    prevDay = None
    sheduleRes = []

    for time, component in shedule:
        day = time.date()
        if day != prevDay:
            sheduleRes.append(unicode(time.strftime(u'%A %d %B %Y')))
            prevDay = day
        sheduleRes.append(time.strftime(u'%H:%M') + u' -- ' + component.get('SUMMARY'))
    return sheduleRes



def getWeeklyShedule(week = False, offset = 0, day = None):
    if day:
        start = datetime(day[0], day[1], day[2], tzinfo = timezone.utc)
    else:
        now = datetime.now()
        start = datetime(now.year, now.month, now.day, tzinfo = timezone.utc)
    period = 1
    if week:
        offset -= start.isoweekday() - 1
        period = 7
    if offset:
        start += timedelta(days = offset)
    end = start + timedelta(days = period)
    return getShedule(start, end)

def create_calendar(year,month):
    #First row - Month and Year
    calName = u'{} {}'.format(calendar.month_name[month], year)
    keys = [[('<', "calendar {}".format(year * 12 + month - 2)),
             (calName, ),
             ('>', "calendar {}".format(year * 12 + month)),
             ]]
    #Second row - Week Days
    week_days=[(l, ) for l in u"ПВСЧПСВ"]
    keys.append(week_days)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append((" ",))
            else:
                callback = u'getSheduleDay {} {} {}'.format(year, month, day)
                row.append((str(day), callback))
        keys.append(row)
    
    
    
    keys.append([('На сегодня', u'getSheduleToday'),
                 ('На завтра', u'getSheduleTommoroe')])
    keys.append([('На эту неделю', u'getSheduleWeekly'),
                 ('На следующую неделю', u'getSheduleNextWeekly')])
    return keys