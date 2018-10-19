import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def cheaum():
    url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005000&strDate='

    now = dt.datetime.now()
    nowDate = str(now.strftime('%Y-%m-%d'))
    tomorrow = now + dt.timedelta(days=1)
    toDate = str(tomorrow.strftime('%Y-%m-%d'))
    url = url + nowDate

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    check_chaeum = str(soup.find('table').find_all('th'))
    if '정보가 없습니다' in check_chaeum:
        text = '운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'
        return text
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

        return meal

def cheaum_tomorrow():
    url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005000&strDate='

    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=1)
    toDate = str(tomorrow.strftime('%Y-%m-%d'))
    url = url + toDate

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    check_chaeum = str(soup.find('table').find_all('th'))
    if '정보가 없습니다' in check_chaeum:
        text = '운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'
        return text
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

        return meal

"""
def domitori():
    url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm'

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')

    now = dt.datetime.now()
    nowDate = str(now.strftime('%a'))
    day = {'Mon': 3, 'Tue': 4, 'Wed': 5, 'Thu': 6, 'Fri': 7, 'Sat': 8, 'Sun': 9, }
    index_day = day.get(nowDate)

    cafe_table = pd.read_html(url)[0]
    cafe_table = cafe_table.fillna('없음')
    breakfast = cafe_table[1][index_day]
    lunch = cafe_table[2][index_day]
    dinner = cafe_table[3][index_day]

    if breakfast =='없음':
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

    meal = '<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
           '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
           '\n\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

    meal = meal.replace('amp;', '', 5)

    return meal
"""
#이전방식
"""

def domitori_tomorrow():
    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=1)
    nowDate = str(now.strftime('%a'))
    toDate = str(tomorrow.strftime('%a'))

    if nowDate == 'Sun': #오늘이 일요일이면 다음주 데이터를 받아와야함
        nowYearDate = str(now.strftime('%Y'))
        nowMonthDate = str(now.strftime('%m'))
        toDayDate = str(tomorrow.strftime('%d'))

        url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm?year='+nowYearDate+'&month='+nowMonthDate+'&day='+toDayDate

        day = {'Mon': 3, 'Tue': 4, 'Wed': 5, 'Thu': 6, 'Fri': 7, 'Sat': 8, 'Sun': 9, }
        index_day = day.get(toDate)

        cafe_table = pd.read_html(url)[0]
        cafe_table = cafe_table.fillna('없음')
        breakfast = cafe_table[1][index_day]
        lunch = cafe_table[2][index_day]
        dinner = cafe_table[3][index_day]

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

        meal = '<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
               '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
               '\n\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

        meal = meal.replace('amp;', '', 5)

        return meal

    else:
        url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm'

        day = {'Mon': 3, 'Tue': 4, 'Wed': 5, 'Thu': 6, 'Fri': 7, 'Sat': 8, 'Sun': 9, }
        index_day = day.get(toDate)

        cafe_table = pd.read_html(url)[0]
        cafe_table = cafe_table.fillna('없음')
        breakfast = cafe_table[1][index_day]
        lunch = cafe_table[2][index_day]
        dinner = cafe_table[3][index_day]

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

        meal = '<----------조식---------->\n식사시간 07:30~09:00\n@방학중 08:00 ~ 09:00\n' + breakfast + \
               '\n\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
               '\n\n<----------석식---------->\n식사시간 18:00~19:30\n@방학중 18:00 ~ 19:00\n' + dinner

        meal = meal.replace('amp;', '', 5)

        return meal

"""
#이전방식

def domitori(): #당일 정보
    now = dt.datetime.now()
    nowDate = str(now.strftime('%a'))

    f = open("C:\project/Domitori_DB/" + nowDate + ".txt", 'r')
    data = f.read()
    f.close()

    return data

def domitori_tomorrow():
    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=1)
    nowDate = str(now.strftime('%a'))
    toDate = str(tomorrow.strftime('%a'))

    if nowDate == 'Sun': #오늘이 일요일인 경우
        f = open("C:\project/Domitori_DB/nextMon.txt", 'r')
        data = f.read()
        f.close()

        return data
    else: #이외의 날짜인 경우
        f = open("C:\project/Domitori_DB/" + toDate + ".txt", 'r')
        data = f.read()
        f.close()

        return data



def erum():
    url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005001&strDate='

    now = dt.datetime.now()
    nowDate = str(now.strftime('%Y-%m-%d'))
    tomorrow = now + dt.timedelta(days=1)
    toDate = str(tomorrow.strftime('%Y-%m-%d'))
    url = url + nowDate

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    check_ahrum = str(soup.find('table'))

    if '정보가 없습니다' in check_ahrum:
        text = '운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'
        return text
    elif '방학 중' in check_ahrum:
        text = '방학 중\n채움관만 운영'
        return text
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
               '\n\n<----------중식---------->\n' + lunch + \
               '\n<----------석식---------->\n' + dinner

        meal = meal.replace('amp;', '', 5)

        return meal

def erum_tomorrow():
    url = 'http://www.andong.ac.kr/index.sko?menuCd=AA06003005001&strDate='

    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=1)
    toDate = str(tomorrow.strftime('%Y-%m-%d'))
    url = url + toDate

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    check_ahrum = str(soup.find('table'))

    if '정보가 없습니다' in check_ahrum:
        text = '운영하지 않는 날입니다\n토, 일, 공휴일은 운영 안함'
        return text
    elif '방학 중' in check_ahrum:
        text = '방학 중\n채움관만 운영'
        return text
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
               '\n\n<----------중식---------->\n' + lunch + \
               '\n<----------석식---------->\n' + dinner

        meal = meal.replace('amp;', '', 5)

        return meal

def restaurant():
    rest_data = "운영시간 10:00 ~ 19:00\n(주말, 공휴일 제외)\n\n김밥: 1500원\n참치김밥: 1500원\n우동: 2500원\n참치마요: 3500원\n등심돈가스: 3800원\n치킨까스: 3800원\n치즈돈가스: 4000원\n불닭덮밥: 3800원\n\
스팸덮밥: 3800원\n샐러드파스타: 3800원\n돼지불고기: 4000원\n소고기불고기: 4500원\n오리불고기: 5000원\n\n"

    return rest_data