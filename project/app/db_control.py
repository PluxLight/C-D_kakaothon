import psycopg2

def key_insert(u_key, reque): # 기존에 있던것은 depth=2로 업데이트 -> 유저가 응답한 반응은 새 튜플에 넣고
    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

    cur = conn.cursor()
    del_str = "delete from user_key where depth=2 and key='" + u_key + "';"
    insert_str = "insert into user_key values ('" + u_key +"', '" + reque +"', 1);"
    update_str = "update user_key set depth='2' where key='" + u_key + "';"
    try: #기존에 값이 있던 경우
        cur.execute(del_str)
        conn.commit()
        cur.execute(update_str)
        conn.commit()
        cur.execute(insert_str)
        conn.commit()

    except: #첫 사용시 값이 없는 경우 등
        cur.execute(insert_str)
        conn.commit()

    cur.close()
    conn.close()

    return 0

def pre_value(u_key):
    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

    cur = conn.cursor()
    sql_str = "select request from user_key where key='" + u_key + "';"
    try: #기존에 값이 있던 경우
        cur.execute(sql_str)

        result = cur.fetchall()

        return result[1][0]

    except: #첫 사용시 값이 없는 경우
        return '0'

def pre_pre_value(u_key):
    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

    cur = conn.cursor()
    sql_str = "select request from user_key where key='" + u_key + "';"
    try: #기존에 값이 있던 경우
        cur.execute(sql_str)

        result = cur.fetchall()

        #print(result[0][0])
        #print(result[1][0])

        return result[0][0]

    except: #첫 사용시 값이 없는 경우
        return '0'

def star_point(star, pre_text, pre_pre_text): #사용자가 보낸 별점을 db에 등록
    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

    #print(pre_text, pre_pre_text)

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


    cur = conn.cursor()
    update_str = "update star_point set point=point + " + str(star) + ", count=count + 1 where position='" + position + "';"

    cur.execute(update_str)
    conn.commit()

    cur.close()
    conn.close()

    return 0

def trans_star(pre_text, pre_pre_text): #시간과 장소 / 사용자가 식단정보 요청시 별점정보도 같이 보낼때 숫자형태를 특수문자 별로 변환

    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

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

    cur = conn.cursor()
    sql_str = "select point from star_point where position='" + position + "';"
    sql_str_2 = "select count from star_point where position='" + position + "';"

    cur.execute(sql_str)
    result = cur.fetchall()

    cur.execute(sql_str_2)
    cnt = cur.fetchall()

    cur.close()
    conn.close()

    sum = float(result[0][0])

    cnt = float(cnt[0][0])

    if cnt == 0:
        pass
    else:
        sum = sum / cnt



    star_str = ''

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

def count_star(pre_text, pre_pre_text): #시간과 장소 / 사용자가 식단정보 요청시 별점 주기에 참여한 사람들 숫자도 보내기

    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

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

    cur = conn.cursor()
    sql_str = "select count from star_point where position='" + position + "';"

    cur.execute(sql_str)
    cnt = cur.fetchall()

    cur.close()
    conn.close()

    cnt = int(cnt[0][0])

    return cnt

def star_reset(): #윈도우 스케줄러에 등록해서 매 정각마다 별점과 참여한 사람 수를 초기화
    try:
        conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
    except:
        return 0

    cur = conn.cursor()
    update_str = "update star_point set point=0, count=0;"

    cur.execute(update_str)
    conn.commit()

    cur.close()
    conn.close()

    return 0

if __name__ == "__main__":
    star_reset()


def trash():

    """

        try:
            cur = conn.cursor()
            sql_str = "select point from star_point where position='" + position + "';"
            print(sql_str)

            cur.execute(sql_str)

            result = cur.fetchall()
            print(result)
        except:
            print(sql_str)



        try:
            sum = float(result[0][0])
        except:
            print(sql_str)
            print(result)


        sum = (sum + float(star)) / 2
        """