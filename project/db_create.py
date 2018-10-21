import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def domitori_create(): #이번주 기숙사 식단 DB생성
    url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm'

    day_db = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_db_h = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일']

    cafe_table = pd.read_html(url)[0]
    cafe_table = cafe_table.fillna('없음')

    now = dt.datetime.now()
    nowDate = str(now.strftime('%Y-%m-%d'))

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

        meal_str = nowDate + ' ' + day_db_h[i_f-3] + '\n<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
                   '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
                   '\n\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

        f = open("C:\project/Domitori_DB/" + str(day_db[i_f - 3]) + ".txt", 'w')
        f.write(meal_str)
        f.close()

        now = now + dt.timedelta(days=1)
        nowDate = str(now.strftime('%Y-%m-%d'))

    return 0

def nw_domitori_create(): #다음주 월요일 기숙사 식단 DB생성

    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=7)
    day_of_week = dt.datetime.today().weekday()
    tomorrow = tomorrow - dt.timedelta(days=day_of_week)
    toDate = str(tomorrow.strftime('%Y-%m-%d'))

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

    meal_str = toDate + ' 월요일' + '\n<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
           '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
           '\n\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

    f = open("C:\project/Domitori_DB/nextMon.txt", 'w')
    f.write(meal_str)
    f.close()

    return 0

def first_cheaum_create(): #이번주 채움관 식단 DB생성(생성 요일 무관하게 생성한 날 기준의 주간+다음주 월요일까지)

    day_db = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'nextMon']
    day_db_h = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일']

    day_of_week = dt.datetime.today().weekday()
    now = dt.datetime.now()
    standard_day = now - dt.timedelta(days=day_of_week)

    for i_f in range(0, 8):
        url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005000&strDate='
        now = standard_day
        exact_day = now + dt.timedelta(days=i_f)
        nowDate = str(exact_day.strftime('%Y-%m-%d'))
        url = url + nowDate

        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        check_chaeum = str(soup.find('table').find_all('th'))
        if '정보가 없습니다' in check_chaeum:
            text = nowDate + ' ' + day_db_h[i_f] + '\n운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'

            f = open("C:\project/Cheaum_DB/" + str(day_db[i_f]) + ".txt", 'w')
            f.write(text)
            f.close()
        else:
            table_data = soup.find('table').find_all('td')
            cafe_table = str(table_data).split('</td>')
            breakfast = cafe_table[0][17:-5]
            l = cafe_table[1][18:-5]
            d = cafe_table[2][18:-5]
            lun = l.split('<br/>')
            lunch = ''
            for i in lun:
                lunch = lunch + i + '\n'

            din = d.split('<br/>')
            dinner = ''
            for i in din:
                dinner = dinner + i + '\n'

            meal = nowDate + ' ' + day_db_h[i_f] + '\n<----------조식---------->\n' + breakfast + \
                   '\n\n<----------중식---------->\n식사시간 11:50~13:30\n' + lunch + \
                   '\n<----------석식---------->\n식사시간 16:50~18:30\n' + dinner

            meal = meal.replace('amp;', '', 5)

            f = open("C:\project/Cheaum_DB/" + str(day_db[i_f]) + ".txt", 'w')
            f.write(meal)
            f.close()



    return 0

def first_erum_create(): #이번주 이룸관 식단 DB생성(생성 요일 무관하게 생성한 날 기준의 주간+다음주 월요일까지)

    day_db = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'nextMon']
    day_db_h = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일']

    day_of_week = dt.datetime.today().weekday()
    now = dt.datetime.now()
    standard_day = now - dt.timedelta(days=day_of_week)

    for i_f in range(0, 8):
        url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005001&strDate='
        now = standard_day
        exact_day = now + dt.timedelta(days=i_f)
        nowDate = str(exact_day.strftime('%Y-%m-%d'))
        url = url + nowDate

        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        check_chaeum = str(soup.find('table').find_all('th'))
        if '정보가 없습니다' in check_chaeum:
            text = nowDate + ' ' + day_db_h[i_f] + '\n운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'

            f = open("C:\project/Erum_DB/" + str(day_db[i_f]) + ".txt", 'w')
            f.write(text)
            f.close()
        else:
            table_data = soup.find('table').find_all('td')
            cafe_table = str(table_data).split('</td>')
            breakfast = cafe_table[0][17:-5]
            l = cafe_table[1][18:-5]
            d = cafe_table[2][18:-5]
            lun = l.split('<br/>')
            lunch = ''
            for i in lun:
                lunch = lunch + i + '\n'

            din = d.split('<br/>')
            dinner = ''
            for i in din:
                dinner = dinner + i + '\n'

            meal = nowDate + ' ' + day_db_h[i_f] + '\n<----------조식---------->\n' + breakfast + \
                   '\n\n<----------중식---------->\n식사시간 11:50~13:30\n' + lunch + \
                   '\n<----------석식---------->\n식사시간 16:50~18:30\n' + dinner

            meal = meal.replace('amp;', '', 5)

            f = open("C:\project/Erum_DB/" + str(day_db[i_f]) + ".txt", 'w')
            f.write(meal)
            f.close()



    return 0


domitori_create()
nw_domitori_create()
first_cheaum_create()
first_erum_create()


#cheaum_create()

"""
def cheaum_create(): #이번주 채움관 식단 DB생성

    day_db = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'nextMon']

    for i_f in range(0, 8):
        url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005000&strDate='
        now = dt.datetime.now()
        tomorrow = now + dt.timedelta(days=i_f)
        nowDate = str(tomorrow.strftime('%Y-%m-%d'))
        url = url + nowDate

        day_of_week = dt.datetime.today().weekday()
        day_of_week = (day_of_week + i_f)%8

        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        check_chaeum = str(soup.find('table').find_all('th'))
        if '정보가 없습니다' in check_chaeum:
            text = '운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'

            f = open("C:\project/Cheaum_DB/" + str(day_db[day_of_week]) + ".txt", 'w')
            f.write(text)
            f.close()
        else:
            table_data = soup.find('table').find_all('td')
            cafe_table = str(table_data).split('</td>')
            breakfast = cafe_table[0][17:-5]
            l = cafe_table[1][18:-5]
            d = cafe_table[2][18:-5]
            lun = l.split('<br/>')
            lunch = ''
            for i in lun:
                lunch = lunch + i + '\n'

            din = d.split('<br/>')
            dinner = ''
            for i in din:
                dinner = dinner + i + '\n'

            meal = '<----------조식---------->\n' + breakfast + \
                   '\n\n<----------중식---------->\n식사시간 11:50~13:30\n' + lunch + \
                   '\n<----------석식---------->\n식사시간 16:50~18:30\n' + dinner

            meal = meal.replace('amp;', '', 5)

            f = open("C:\project/Cheaum_DB/" + str(day_db[day_of_week]) + ".txt", 'w')
            f.write(meal)
            f.close()



    return 0

"""