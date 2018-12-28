import psycopg2
import datetime as dt
import pandas as pd
import requests
from bs4 import BeautifulSoup

class db_manage:

    def __init__(self):
        self.conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")

    def meal_exist(self, position, day):  # 해당 식당의 식사가 존재하는지 여부 확인
        day_db_h = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일(다음주)']  # DB 텍스트에 넣을 요일 문자 리스트

        day = day_db_h[day]

        cur = self.conn.cursor()
        sql_str = "select breakfast, lunch, dinner from school_menu where place='%s' and day='%s';" % (position, day)
        cur.execute(sql_str)
        result = cur.fetchall()

        breakfast_exist = result[0][0]
        lunch_exist = result[0][1]
        dinner_exist = result[0][2]

        return breakfast_exist, lunch_exist, dinner_exist

    def star_reset(self):  # 윈도우 스케줄러에 등록해서 매 정각마다 별점과 참여한 사람 수를 초기화, 투표 참여자도 초기화
        cur = self.conn.cursor()
        update_str = "update star_point set point=0, count=0;"

        cur.execute(update_str)
        update_str = "delete from star_overlap;"

        cur.execute(update_str)
        self.conn.commit()

    def school_menu_delete(self):  # DB에 등록된 학생회관 식당, 기숙사 식당 정보를 삭제
        cur = self.conn.cursor()
        sql_str = "delete from school_menu;"
        cur.execute(sql_str)
        self.conn.commit()

    def db_upload(self, place, upload_data, dow, morning, lunch, dinner):  # DB에 학생회관 식당, 기숙사 식당 정보를 등록
        cur = self.conn.cursor()
        sql_str = "insert into school_menu values ('%s', '%s', '%s', %r, %r, %r);" % (
            place, upload_data, dow, morning, lunch, dinner)
        cur.execute(sql_str)
        self.conn.commit()

    def exist_check(self, morning, lunch, dinner):  # 조식, 중식, 석식 식단이 있는지 판단한다 / db에 업로드 할 때 사용 / 메뉴 길이로 식단 존재여부 판단
        if morning > 3:
            morning = True
        else:
            morning = False

        if lunch > 3:
            lunch = True
        else:
            lunch = False

        if dinner > 3:
            dinner = True
        else:
            dinner = False

        return morning, lunch, dinner

    def menu_sum(self, breakfast, lunch, dinner):  # DB에 식단정보 등록할때 문자열을 합치는 기능
        # print(breakfast, lunch, dinner)

        sum = ''
        for i in breakfast:
            sum += str(i) + '\n'
        breakfast = sum

        sum = ''
        for i in lunch:
            sum += str(i) + '\n'
            lunch = sum

        sum = ''
        for i in dinner:
            sum += str(i) + '\n'
            dinner = sum

        return breakfast, lunch, dinner

    def domitori_create(self):  # 이번주 기숙사 식단 DB생성
        url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm'

        day_db_h = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

        day_of_week = dt.datetime.today().weekday()  # 요일 반환 (0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일)
        now = dt.datetime.now()  # 현재 날짜 값
        standard_day = now - dt.timedelta(
            days=day_of_week)  # 함수가 실행된 시점에서 월요일의 날짜를 가져온다 #현재 날짜에서 현재 날짜의 값(weekday 반환 값)을 빼서 월요일의 날짜로 만듦

        cafe_table = pd.read_html(url)[0]
        cafe_table = cafe_table.fillna('없음')

        for i in range(0, 7):  # 일주일치 데이터 업로드
            exact_day = standard_day + dt.timedelta(days=i)
            nowDate = str(exact_day.strftime('%Y-%m-%d'))

            breakfast = cafe_table[1][i + 3]
            lunch = cafe_table[2][i + 3]
            dinner = cafe_table[3][i + 3]

            breakfast = breakfast.split(' ')
            lunch = lunch.split(' ')
            dinner = dinner.split(' ')

            em, el, ed = self.exist_check(len(breakfast), len(lunch), len(dinner))  # 리스트의 길이로 식단 존재 여부 판단 후 변수에 저장

            breakfast, lunch, dinner = self.menu_sum(breakfast, lunch, dinner)

            menu_text = nowDate + ' ' + day_db_h[i] + '\n<----------조식---------->\n식사시간 07:30~09:00\n' + breakfast + \
                        '\n<----------중식---------->\n식사시간 12:00~13:30\n' + lunch + \
                        '\n<----------석식---------->\n식사시간 18:00~19:30\n' + dinner

            self.db_upload('기숙사', menu_text, day_db_h[i], em, el, ed)

        # 다음주 월요일 정보 생성
        tomorrow = now + dt.timedelta(days=7)  # 오늘 기준으로 +7일
        day_of_week = dt.datetime.today().weekday()  # 오늘 날짜의 요일을 숫자로 변환 (0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일)
        tomorrow = tomorrow - dt.timedelta(days=day_of_week)  # 오늘 기준으로 다음주에서 오늘의 요일 값만큼 빼서 다음주 월요일이 도출
        toDate = str(tomorrow.strftime('%Y-%m-%d'))  # 도출된 값을 지정된 형식으로 문자열 포맷

        nowYearDate = str(tomorrow.strftime('%Y'))
        nowMonthDate = str(tomorrow.strftime('%m'))
        toDayDate = str(tomorrow.strftime('%d'))

        url = 'http://dorm.andong.ac.kr/2014/food_menu/food_menu.htm?year=' + nowYearDate + '&month=' + nowMonthDate + '&day=' + toDayDate

        cafe_table = pd.read_html(url)[0]
        cafe_table = cafe_table.fillna('없음')

        breakfast = cafe_table[1][3]
        lunch = cafe_table[2][3]
        dinner = cafe_table[3][3]

        breakfast = breakfast.split(' ')
        lunch = lunch.split(' ')
        dinner = dinner.split(' ')

        em, el, ed = self.exist_check(len(breakfast), len(lunch), len(dinner))

        breakfast, lunch, dinner = self.menu_sum(breakfast, lunch, dinner)

        menu_text = toDate + ' ' + '월요일' + '\n<----------조식---------->\n' + breakfast + \
                    '\n<----------중식---------->\n식사시간 11:50~13:30\n' + lunch + \
                    '\n<----------석식---------->\n식사시간 16:50~18:30\n' + dinner

        self.db_upload('기숙사', menu_text, '월요일(다음주)', em, el, ed)

    def cheaum_create(self):  # 이번주 채움관 식단 DB생성(생성 요일 무관하게 생성한 날 기준의 주간+다음주 월요일까지)

        day_db_sql = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일(다음주)']  # sql_str에 넣을 요일 문자 리스트
        day_db_menu = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일']  # menu_text에 넣을 요일 문자 리스트

        day_of_week = dt.datetime.today().weekday()  # 요일 반환 (0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일)
        now = dt.datetime.now()  # 현재 날짜 값
        standard_day = now - dt.timedelta(
            days=day_of_week)  # 함수가 실행된 시점에서 월요일의 날짜를 가져온다 #현재 날짜에서 현재 날짜의 값(weekday 반환 값)을 빼서 월요일의 날짜로 만듦

        for i in range(0, 8):
            cheaum_url = 'http://www.andong.ac.kr/main/module/foodMenu/view.do?manage_idx=21&memo5='  # 채움관 식단 정보가 있는 url(날짜 빠짐)
            exact_day = standard_day + dt.timedelta(days=i)
            nowDate = str(exact_day.strftime('%Y-%m-%d'))
            cheaum_url = cheaum_url + nowDate

            req = requests.get(cheaum_url)
            html = req.text
            soup = BeautifulSoup(html, 'lxml')

            soup = str(soup)

            if '정보가 없습니다' in soup:
                soup = BeautifulSoup(html, 'lxml')
                check_chaeum = soup.find_all('dt')
                menu_text = str(check_chaeum[0]).replace('<dt style="width:100%; text-align:center;">', "").replace(
                    "</dt>", "").split("<br/>")
                menu_text = nowDate + ' ' + day_db_menu[i] + '\n' + str(menu_text[0]) + '\n' + str(menu_text[1])
                self.db_upload('채움관', menu_text, day_db_sql[i], False, False, False)
            else:
                soup = BeautifulSoup(html, 'lxml')
                check_chaeum = soup.find_all('dd')

                breakfast = str(check_chaeum[0]).replace("<dd>", "").replace("</dd>", "").replace("amp;", "").split(
                    "<br/>")  # Web에서 &기호 읽어들일때 amp; 라는 문장이 추가되어 제거하는 과정 추가
                lunch = str(check_chaeum[1]).replace("<dd>", "").replace("</dd>", "").replace("amp;", "").split("<br/>")
                dinner = str(check_chaeum[2]).replace("<dd>", "").replace("</dd>", "").replace("amp;", "").split(
                    "<br/>")

                em, el, ed = self.exist_check(len(breakfast), len(lunch), len(dinner))  # 리스트의 길이로 식단 존재 여부 판단 후 변수에 저장

                breakfast, lunch, dinner = self.menu_sum(breakfast, lunch, dinner)

                menu_text = nowDate + ' ' + day_db_menu[i] + '\n<----------조식---------->\n' + breakfast + \
                            '<----------중식---------->\n식사시간 11:50~13:30\n' + lunch + \
                            '<----------석식---------->\n식사시간 16:50~18:30\n' + dinner

                self.db_upload('채움관', menu_text, day_db_sql[i], em, el, ed)

    def erum_create(self):  # 이번주 채움관 식단 DB생성(생성 요일 무관하게 생성한 날 기준의 주간+다음주 월요일까지)

        day_db_sql = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일(다음주)']  # sql_str에 넣을 요일 문자 리스트
        day_db_menu = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '월요일']  # menu_text에 넣을 요일 문자 리스트

        day_of_week = dt.datetime.today().weekday()  # 요일 반환 (0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일)
        now = dt.datetime.now()  # 현재 날짜 값
        standard_day = now - dt.timedelta(
            days=day_of_week)  # 함수가 실행된 시점에서 월요일의 날짜를 가져온다 #현재 날짜에서 현재 날짜의 값(weekday 반환 값)을 빼서 월요일의 날짜로 만듦

        for i in range(0, 8):
            erum_url = 'http://www.andong.ac.kr/main/module/foodMenu/view.do?manage_idx=73&memo5='  # 채움관 식단 정보가 있는 url(날짜 빠짐)
            exact_day = standard_day + dt.timedelta(days=i)
            nowDate = str(exact_day.strftime('%Y-%m-%d'))
            erum_url = erum_url + nowDate

            req = requests.get(erum_url)
            html = req.text
            soup = BeautifulSoup(html, 'lxml')

            soup = str(soup)

            if '정보가 없습니다' in soup:
                soup = BeautifulSoup(html, 'lxml')
                check_chaeum = soup.find_all('dt')
                menu_text = str(check_chaeum[0]).replace('<dt style="width:100%; text-align:center;">', "").replace(
                    "</dt>", "").split("<br/>")
                menu_text = nowDate + ' ' + day_db_menu[i] + '\n' + str(menu_text[0]) + '\n' + str(menu_text[1])
                self.db_upload('이룸관', menu_text, day_db_sql[i], False, False, False)
            else:
                soup = BeautifulSoup(html, 'lxml')
                check_chaeum = soup.find_all('dd')

                breakfast = str(check_chaeum[0]).replace("<dd>", "").replace("</dd>", "").replace("amp;", "").split(
                    "<br/>")  # Web에서 &기호 읽어들일때 amp; 라는 문장이 추가되어 제거하는 과정 추가
                lunch = str(check_chaeum[1]).replace("<dd>", "").replace("</dd>", "").replace("amp;", "").split("<br/>")
                dinner = str(check_chaeum[2]).replace("<dd>", "").replace("</dd>", "").replace("amp;", "").split(
                    "<br/>")

                em, el, ed = self.exist_check(len(breakfast), len(lunch), len(dinner))  # 리스트의 길이로 식단 존재 여부 판단 후 변수에 저장

                breakfast, lunch, dinner = self.menu_sum(breakfast, lunch, dinner)

                menu_text = nowDate + ' ' + day_db_menu[i] + '\n<----------조식---------->\n' + breakfast + \
                            '<----------중식---------->\n식사시간 11:50~13:30\n' + lunch + \
                            '<----------석식---------->\n식사시간 16:50~18:30\n' + dinner

                self.db_upload('이룸관', menu_text, day_db_sql[i], em, el, ed)


if __name__ == "__main__": #윈도우 스케줄러에 의해 실행되는 경우
    dc = db_manage()
    day_of_week = dt.datetime.today().weekday()
    if day_of_week == 0: #실행 당일이 월요일인 경우 (학생회관, 기숙사 식당 정보 업로드)
        dc.school_menu_delete()
        dc.domitori_create()
        dc.cheaum_create()
        dc.erum_create()
    dc.star_reset() #별점관련 정보 초기화