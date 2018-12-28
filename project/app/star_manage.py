import psycopg2
import threading

class star_control:

    def __init__(self, place):
        self.conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
        self.star_place = place

    def star_point(self, star, pre_text, pre_pre_text):  # 사용자가 보낸 별점을 db에 등록
        if pre_text == "조식" and pre_pre_text == "채움관&이룸관":
            position = 'cheaum_morning'
        elif pre_text == '중식' and pre_pre_text == '채움관&이룸관':
            position = 'cheaum_lunch'
        elif pre_text == '석식' and pre_pre_text == '채움관&이룸관':
            position = 'cheaum_dinner'
        elif pre_text == '조식' and pre_pre_text == '기숙사':
            position = 'domitori_morning'
        elif pre_text == '중식' and pre_pre_text == '기숙사':
            position = 'domitori_lunch'
        elif pre_text == '석식' and pre_pre_text == '기숙사':
            position = 'domitori_dinner'
        else:
            return 0

        cur = self.conn.cursor()
        update_str = "update star_point set point=point + " + str(
            star) + ", count=count + 1 where position='" + position + "';"

        cur.execute(update_str)
        self.conn.commit()

    def trans_star(self, sum, cnt):  # 정수형태의 별점을 특수문자 형태로 변환
        if cnt == 0:  # 값이 0인경우 값을 나누지않고 넘어간다
            pass
        else:  # 0이 아니면 별점을 사용자 수만큼 나누어 평균값을 구한다
            sum = sum / cnt

        if sum == 5 or sum > 4.0:
            star_str = '★★★★★'
            return star_str
        elif sum <= 4.0 and sum > 3.0:
            star_str = '★★★★☆'
            return star_str
        elif sum <= 3.0 and sum > 2.0:
            star_str = '★★★☆☆'
            return star_str
        elif sum <= 2.0 and sum > 1.0:
            star_str = '★★☆☆☆'
            return star_str
        elif sum <= 1.0 and sum > 0.0:
            star_str = '★☆☆☆☆'
            return star_str
        else:
            star_str = '☆☆☆☆☆'
            return star_str

    def star_cnt(self):  # 사용자가 식단정보 요청시 별점정보도 같이 보낼때 숫자형태를 특수문자 별로 변환  별점 주기에 참여한 사람들 숫자도 보내기

        if self.star_place == "채움관" or self.star_place == "이룸관":
            self.star_place = 'cheaum'
        elif self.star_place == '기숙사':
            self.star_place = 'domitori'
        else:
            self.star_place = 'none'

        cur = self.conn.cursor()
        sql_str = "select point, count from star_point where position like '%" + self.star_place + "%' order by position desc;"

        cur.execute(sql_str)
        result = cur.fetchall()

        self.breakfast_star = result[0][0]
        self.breakfast_cnt = result[0][1]
        self.lunch_star = result[1][0]
        self.lunch_cnt = result[1][1]
        self.dinner_star = result[2][0]
        self.dinner_cnt = result[2][1]

        self.breakfast_star = self.trans_star(self.breakfast_star, self.breakfast_cnt)
        self.lunch_star = self.trans_star(self.lunch_star, self.lunch_cnt)
        self.dinner_star = self.trans_star(self.dinner_star, self.dinner_cnt)

    def overlap_check(self, u_key, pre_text, pre_pre_text):  # 별점주기에 참여한 적이 있는지 확인하는 기능
        if pre_text == "조식" and pre_pre_text == "채움관&이룸관":
            position = 'cheaum_morning'
        elif pre_text == '중식' and pre_pre_text == '채움관&이룸관':
            position = 'cheaum_lunch'
        elif pre_text == '석식' and pre_pre_text == '채움관&이룸관':
            position = 'cheaum_dinner'
        elif pre_text == '조식' and pre_pre_text == '기숙사':
            position = 'domitori_morning'
        elif pre_text == '중식' and pre_pre_text == '기숙사':
            position = 'domitori_lunch'
        elif pre_text == '석식' and pre_pre_text == '기숙사':
            position = 'domitori_dinner'
        else:
            position = 'none'

        cur = self.conn.cursor()
        sql_str = "select overlap_check from star_overlap where userkey='" + u_key + "' and position='" + position + "';"

        cur.execute(sql_str)
        check_int = cur.fetchall()
        try:  # 별점을 해당 내용에 투표한 적이 있다면
            check_int = int(check_int[0][0])
        except:  # 별점을 해당 내용에 투표한 적이 없어서 데이터가 없는 경우
            check_int = 0

        if check_int == 0:  # 투표 당일날 해당 항목에 투표를 한 번도 안한경우
            # update_str = "update star_overlap set overlap_check=1 where userkey='" + u_key + "' and position='" + position +"';"
            update_str = "insert into star_overlap values ('" + u_key + "', '" + position + "', 1)"
            cur.execute(update_str)
            self.conn.commit()

            return 0
        else:  # 투표 당일날 해당 항목에 투표한 경우
            return 1