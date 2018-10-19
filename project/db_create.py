import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def domitori_create(): #이번주 기숙사 식단 DB생성
    url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm'

    day_db = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    cafe_table = pd.read_html(url)[0]
    cafe_table = cafe_table.fillna('없음')


    for i_f in range(3, 10):
        breakfast = cafe_table[1][i_f]
        lunch = cafe_table[2][i_f]
        dinner = cafe_table[3][i_f]

        if breakfast == '없음':
            breakfast = '아침 없음'
        else:
            breakfast = breakfast.split(' ')
            sum = ''
            for i_t in breakfast:
                sum = sum + i_t + '\n'
                breakfast = sum

        if lunch == '없음':
            lunch = '점심 없음'
        else:
            lunch = lunch.split(' ')
            sum = ''
            for i_t in lunch:
                sum = sum + i_t + '\n'
                lunch = sum

        if dinner == '없음':
            dinner = '저녁 없음'
        else:
            dinner = dinner.split(' ')
            sum = ''
            for i_t in dinner:
                sum = sum + i_t + '\n'
                dinner = sum

        meal_str = '<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
                   '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
                   '\n\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

        f = open("C:\project/Domitori_DB/" + str(day_db[i_f - 3]) + ".txt", 'w')
        f.write(meal_str)
        f.close()

    return 0

def nw_domitori_create(): #다음주 월요일 기숙사 식단 DB생성

    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=7)

    nowYearDate = str(now.strftime('%Y'))
    nowMonthDate = str(now.strftime('%m'))
    toDayDate = str(tomorrow.strftime('%d'))

    url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm?year=' + nowYearDate + '&month=' + nowMonthDate + '&day=' + toDayDate

    cafe_table = pd.read_html(url)[0]
    cafe_table = cafe_table.fillna('없음')
    breakfast = cafe_table[1][3]
    lunch = cafe_table[2][3]
    dinner = cafe_table[3][3]

    if breakfast == '없음':
        breakfast = '아침 없음'
    else:
        breakfast = breakfast.split(' ')
        sum = ''
        for i in breakfast:
            sum = sum + i + '\n'
        breakfast = sum

    if lunch == '없음':
        lunch = '점심 없음'
    else:
        lunch = lunch.split(' ')
        sum = ''
        for i in lunch:
            sum = sum + i + '\n'
        lunch = sum

    if dinner == '없음':
        dinner = '저녁 없음'
    else:
        dinner = dinner.split(' ')
        sum = ''
        for i in dinner:
            sum = sum + i + '\n'
        dinner = sum

    meal_str = '<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
           '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
           '\n\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

    f = open("C:\project/Domitori_DB/nextMon.txt", 'w')
    f.write(meal_str)
    f.close()

    return 0



domitori_create()
nw_domitori_create()