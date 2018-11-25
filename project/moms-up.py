import pandas as pd
import psycopg2

conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")

cur = conn.cursor()

df = pd.read_excel("moms.xlsx", sheet_name='Sheet1')

#print(df['메뉴'])

menu_list = df['메뉴']

price_list = df['가격']

note_list = df['비고']

#print(menu_list[0])

df_len = int(menu_list.count())
print(df_len)


for i in range(df_len):
    sql_str = "insert into moms values ('%s', %d, '%s')" %(menu_list[i], price_list[i], note_list[i])
    #print(sql_str)
    cur.execute(sql_str)
    conn.commit()

# def moms_db():
#     try:
#         conn = psycopg2.connect("dbname=k_userkey user=postgres host=localhost password=474849")
#     except:
#         print("moms_db Error")
#         return 0
#
#     cur = conn.cursor()
#
#     cur.execute("select * from moms;")
#
#     results = cur.fetchall()
#
#     moms_data = ''
#
#     for result in results:
#         moms_data += '\n' + str(result[0]) + ' ' + str(result[1]) + ' ' +str(result[2])
#
#     print(moms_data)
#
# moms_db()
