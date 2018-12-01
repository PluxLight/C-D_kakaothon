import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from app import db_control

def domitori(): #기숙사 당일 정보
    day_of_week = dt.datetime.today().weekday()

    data = db_control.menu_print('기숙사', day_of_week)

    data = data + '\n조식 ' + str(db_control.trans_star('조식', '기숙사')) + ' ' + str(db_control.count_star('조식', '기숙사')) + '명이 참여\n중식 ' + \
           str(db_control.trans_star('중식', '기숙사')) + ' ' + str(db_control.count_star('중식', '기숙사')) + '명이 참여\n석식 ' + \
           str(db_control.trans_star('석식', '기숙사')) + ' ' + str(db_control.count_star('석식', '기숙사')) + '명이 참여\n'

    return data

def domitori_tomorrow(): #기숙사 익일 정보
    day_of_week = dt.datetime.today().weekday()
    day_of_week += 1

    data = db_control.menu_print('기숙사', day_of_week)

    return data

def cheaum():#채움관 당일 정보
    day_of_week = dt.datetime.today().weekday()

    data = db_control.menu_print('채움관', day_of_week)

    data = data + '\n중식 ' + str(db_control.trans_star('중식', '채움관&이룸관')) + ' ' + str(db_control.count_star('중식', '채움관&이룸관')) + '명이 참여\n석식 ' + \
           str(db_control.trans_star('석식', '채움관&이룸관')) + ' ' + str(db_control.count_star('석식', '채움관&이룸관')) + '명이 참여\n'

    return data

def cheaum_tomorrow(): #채움관 익일 정보
    day_of_week = dt.datetime.today().weekday()
    day_of_week += 1

    data = db_control.menu_print('채움관', day_of_week)

    return data

def erum():#이움관 당일 정보
    day_of_week = dt.datetime.today().weekday()

    data = db_control.menu_print('이룸관', day_of_week)

    data = data + '\n중식 ' + str(db_control.trans_star('중식', '채움관&이룸관')) + ' ' + str(db_control.count_star('중식', '채움관&이룸관')) + '명이 참여\n석식 ' + \
           str(db_control.trans_star('석식', '채움관&이룸관')) + ' ' + str(db_control.count_star('석식', '채움관&이룸관')) + '명이 참여\n'

    return data

def erum_tomorrow(): #이움관 익일 정보
    day_of_week = dt.datetime.today().weekday()
    day_of_week += 1

    data = db_control.menu_print('이룸관', day_of_week)

    return data


def restaurant(): #양식당 정보
    rest_data = "운영시간 10:00 ~ 19:00\n(주말, 공휴일 제외)\n\n김밥: 1500원\n참치김밥: 1500원\n우동: 2500원\n참치마요: 3500원\n등심돈가스: 3800원\n치킨까스: 3800원\n치즈돈가스: 4000원\n불닭덮밥: 3800원\n\
스팸덮밥: 3800원\n샐러드파스타: 3800원\n돼지불고기: 4000원\n소고기불고기: 4500원\n오리불고기: 5000원\n\n"

    return rest_data

def moms(moms_type): #맘스터치 정보
    moms_data = db_control.moms_db(moms_type)

    return moms_data