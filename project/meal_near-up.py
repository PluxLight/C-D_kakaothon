import pandas as pd
import psycopg2

conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")

cur = conn.cursor()

sql_str = "delete from restaurant;"
cur.execute(sql_str) #일단 삭제부터

df = pd.read_excel("meal_near.xlsx", sheet_name='Sheet2')

restaurant_name = df['가게이름']
menu_list = df['메뉴 이름']
price_list = df['가격']
tel_list = df['전화번호']
delivery_list = df['배달가능']

df_len = int(menu_list.count())

for i in range(df_len):
    sql_str = "insert into restaurant values ('%s', '%s', '%s', '%s', '%s')" %(restaurant_name[i], menu_list[i], price_list[i], tel_list[i], delivery_list[i])
    cur.execute(sql_str)

conn.commit()