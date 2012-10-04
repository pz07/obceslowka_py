'''
Created on 24-09-2012

@author: pawel
'''

from django import template
import datetime

def answer_value_is_empty(value):
    if value:
        if value[0] and len(value[0]) > 0:
            return False
        
    return True

def date_before_today(value):
    return days_from_now(value) <= 0

def days_from_now(value):
    now = datetime.datetime.now()
    
    today_midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)
    value_midnight = datetime.datetime(value.year, value.month, value.day)
    
    delta = value_midnight - today_midnight
    return delta.days +1
     
register = template.Library()
register.filter('answer_value_is_empty', answer_value_is_empty)
register.filter('date_before_today', date_before_today)
register.filter('days_from_now', days_from_now)

