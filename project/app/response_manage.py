import psycopg2

class key_manage:

    def __init__(self):
        self.conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")

    def key_insert(self, u_key, reque):  # 기존에 있던것은 depth=2로 업데이트 -> 유저가 응답한 반응은 새로 넣는다
        cur = self.conn.cursor()
        del_str = "delete from user_key where depth=2 and key='" + u_key + "';"
        insert_str = "insert into user_key values ('" + u_key + "', '" + reque + "', 1);"
        update_str = "update user_key set depth='2' where key='" + u_key + "';"
        try:  # 기존에 값이 있던 경우
            cur.execute(del_str)
            cur.execute(update_str)
            cur.execute(insert_str)
            self.conn.commit()

        except:  # 첫 사용시 값이 없는 경우 등
            cur.execute(insert_str)
            self.conn.commit()

        return 0

    def pre_value(self, u_key):  # 사용자가 바로 이전에 응답한 값을 반환
        cur = self.conn.cursor()
        sql_str = "select request from user_key where key='" + u_key + "' and depth=1;"
        try:  # 기존에 값이 있던 경우
            cur.execute(sql_str)
            result = cur.fetchall()
            return result[0][0]

        except:  # 첫 사용시 값이 없는 경우
            return '0'

    def pre_pre_value(self, u_key):  # 사용자가 두 단계 이전에 응답한 값을 반환
        cur = self.conn.cursor()
        sql_str = "select request from user_key where key='" + u_key + "' and depth=2;"
        try:  # 기존에 값이 있던 경우
            cur.execute(sql_str)
            result = cur.fetchall()
            return result[0][0]

        except:  # 첫 사용시 값이 없는 경우
            return '0'