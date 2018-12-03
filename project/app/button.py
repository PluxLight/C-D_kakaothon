from app import crawcafeteria
from app import weather
from app import db_control
from django.http import JsonResponse
import datetime

class message_make:

    def __init__(self, cur_text, pre_text, pre_pre_text, user_key): #현재 입력한 버튼, 1단계 전 입력한 버튼, 2단계 전 입력한 버튼, 유저 키
        self.cur_text = cur_text
        self.pre_text = pre_text
        self.pre_pre_text = pre_pre_text
        self.user_key = user_key
        self.no_star = JsonResponse(
                    {
                        'message': {
                            'text': '현재는 별점 등록기간이 아닙니다\n처음으로 돌아갑니다'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["교내식당", "학교 주변식당", "별점 주기",  "오늘의 날씨"]
                        }
                    }
                )
        self.yes_star = JsonResponse(
                    {
                        'message': {
                            'text': '별점을 선택하세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆", "처음으로"]
                        }
                    }
                )
        self.basic_button = ["교내식당", "학교 주변식당", "별점 주기",  "오늘의 날씨"]

    def button_check(self):
        if self.cur_text == '채움관':
            if self.pre_text == '내일의 메뉴 확인':
                return db_control.cheaum_tomorrow()
            else:
                return db_control.cheaum()
        elif self.cur_text == '이룸관':
            if self.pre_text == '내일의 메뉴 확인':
                return db_control.erum_tomorrow()
            else:
                return db_control.erum()
            return db_control.erum()
        elif self.cur_text == '기숙사':
            if self.pre_text == '내일의 메뉴 확인':
                return db_control.domitori_tomorrow()
            else:
                return db_control.domitori()
        elif self.cur_text == '양식당':
            return db_control.restaurant()
        elif self.cur_text == '맘스터치(버거)':
            return db_control.moms('버거')
        elif self.cur_text == '맘스터치(치킨)':
            return db_control.moms('치킨')
        elif self.cur_text == '맘스터치(스낵)':
            return db_control.moms('스낵')
        elif self.cur_text == '오늘의 날씨':
            return weather.main_action()
        else:
            return '미구현'

    def return_message(self):

        if self.cur_text == '교내식당':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식당을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["채움관", "이룸관", "기숙사", "박물관", "내일의 메뉴 확인", "처음으로"]
                    }
                }
            )

        elif self.cur_text == '내일의 메뉴 확인':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식당을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["채움관", "이룸관", "기숙사", "처음으로"]
                    }
                }
            )
        elif self.cur_text == '별점 주기':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '별점은 중복 투표가 불가능하며\n식사시간 중에만 투표가 가능합니다\n식당을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["채움관&이룸관", "기숙사", "처음으로"]
                    }
                }
            )
        elif self.cur_text == '채움관&이룸관':
            day_of_week = datetime.datetime.today().weekday()
            breakfast_exist, lunch_exist, dinner_exist = db_control.meal_exist('채움관', day_of_week)

            if breakfast_exist == False and lunch_exist == False and dinner_exist == False:
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '식단이 존재하지 않습니다\n 처음으로 돌아갑니다'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )
            else:
                button_list = ['처음으로']
                if dinner_exist == True: # 식단이 존재하면 별점 버튼 추가
                    button_list.insert(0, '석식')
                if lunch_exist == True:
                    button_list.insert(0, '중식')
                if breakfast_exist == True:
                    button_list.insert(0, '조식')

                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '식단을 선택하세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": button_list
                        }
                    }
                )

        elif self.cur_text == '기숙사' and self.pre_text == '별점 주기':
            day_of_week = datetime.datetime.today().weekday()
            breakfast_exist, lunch_exist, dinner_exist = db_control.meal_exist('기숙사', day_of_week)

            if breakfast_exist == False and lunch_exist == False and dinner_exist == False:
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '식단이 존재하지 않습니다\n 처음으로 돌아갑니다'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )
            else:
                button_list = ['처음으로']
                if dinner_exist == True: # 식단이 존재하면 별점 버튼 추가
                    button_list.insert(0, '석식')
                if lunch_exist == True:
                    button_list.insert(0, '중식')
                if breakfast_exist == True:
                    button_list.insert(0, '조식')

                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '식단을 선택하세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": button_list
                        }
                    }
                )

        elif self.cur_text == '조식' or self.cur_text == '중식' or self.cur_text == '석식':

            now_time = datetime.datetime.now()

            chaeum_lunch_start = now_time.replace(hour=11, minute=50, second=0, microsecond=0)
            chaeum_lunch_end = now_time.replace(hour=13, minute=30, second=0, microsecond=0)

            chaeum_dinner_start = now_time.replace(hour=16, minute=50, second=0, microsecond=0)
            chaeum_dinner_end = now_time.replace(hour=18, minute=30, second=0, microsecond=0)

            domitory_morning_start = now_time.replace(hour=7, minute=30, second=0, microsecond=0)
            domitory_morning_end = now_time.replace(hour=9, minute=0, second=0, microsecond=0)

            domitory_lunch_start = now_time.replace(hour=12, minute=0, second=0, microsecond=0)
            domitory_lunch_end = now_time.replace(hour=13, minute=30, second=0, microsecond=0)

            domitory_dinner_start = now_time.replace(hour=18, minute=0, second=0, microsecond=0)
            domitory_dinner_end = now_time.replace(hour=19, minute=30, second=0, microsecond=0)

            #채움관 중식 별점 등록 가능여부 확인
            if self.cur_text == '중식' and self.pre_text == '채움관&이룸관' and (now_time >=chaeum_lunch_start and now_time <= chaeum_lunch_end):
                message_val = self.yes_star
            elif self.cur_text == '중식' and self.pre_text == '채움관&이룸관' and (now_time < chaeum_lunch_start or now_time > chaeum_lunch_end):
                message_val = self.no_star

            # 채움관 석식 별점 등록 가능여부 확인
            elif self.cur_text == '석식' and self.pre_text == '채움관&이룸관' and (now_time >=chaeum_dinner_start and now_time <= chaeum_dinner_end):
                message_val = self.yes_star
            elif self.cur_text == '석식' and self.pre_text == '채움관&이룸관' and (now_time < chaeum_dinner_start or now_time > chaeum_dinner_end):
                message_val = self.no_star

            # 기숙사 조식 별점 등록 가능여부 확인
            elif self.cur_text == '조식' and self.pre_text == '기숙사' and (now_time >=domitory_morning_start and now_time <= domitory_morning_end):
                message_val = self.yes_star
            elif self.cur_text == '조식' and self.pre_text == '기숙사' and (now_time < domitory_morning_start or now_time > domitory_morning_end):
                message_val = self.no_star

            # 기숙사 중식 별점 등록 가능여부 확인
            elif self.cur_text == '중식' and self.pre_text == '기숙사' and (now_time >=domitory_lunch_start and now_time <= domitory_lunch_end):
                message_val = self.yes_star
            elif self.cur_text == '중식' and self.pre_text == '기숙사' and (now_time < domitory_lunch_start or now_time > domitory_lunch_end):
                message_val = self.no_star

            #기숙사 석식 별점 등록 가능여부 확인
            elif self.cur_text == '석식' and self.pre_text == '기숙사' and (now_time >=domitory_dinner_start and now_time <= domitory_dinner_end):
                message_val = self.yes_star
            elif self.cur_text == '석식' and self.pre_text == '기숙사' and (now_time < domitory_dinner_start or now_time > domitory_dinner_end):
                message_val = self.no_star

            else:
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '오류가 발생했습니다\n처음으로 돌아갑니다'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )

        elif self.cur_text == '★★★★★' or self.cur_text == "★★★★☆" or self.cur_text == '★★★☆☆' or \
                self.cur_text == '★★☆☆☆' or self.cur_text == '★☆☆☆☆':
            if db_control.overlap_check(self.user_key, self.pre_text, self.pre_pre_text) == 0: #해당 항목에 투표를 한번도 안했을경우
                if self.cur_text == '★★★★★':
                    star = 5
                elif self.cur_text == '★★★★☆':
                    star = 4
                elif self.cur_text == '★★★☆☆':
                    star = 3
                elif self.cur_text == '★★☆☆☆':
                    star = 2
                elif self.cur_text == '★☆☆☆☆':
                    star = 1
                db_control.star_point(star, self.pre_text, self.pre_pre_text)
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '별점이 등록되었습니다'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )
            else:
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '별점의 중복 투표는 제한되어 있습니다'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )

        elif self.cur_text == '박물관':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식당을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["양식당", "맘스터치(버거)", "맘스터치(치킨)", "맘스터치(스낵)", "처음으로"]
                    }
                }
            )

        elif self.cur_text == '학교 주변식당':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '검색할 식당 이름을 입력하세요\n식당리스트를 보려면 리스트 를 입력하세요\n처음으로 돌아가려면 처음으로 를 입력하세요'
                    },
                    "keyboard": {
                        "type": "text"
                    }
                }
            )

        elif self.cur_text == '처음으로':
            message_val = JsonResponse(
            {
                'message': {
                    'text': '처음으로 돌아갑니다'
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": self.basic_button
                }
            }
        )
        else:
            if self.pre_text == '학교 주변식당':
                input_text = db_control.restaurant_list(self.cur_text)
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': input_text
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )
            else:
                input_text = self.button_check()
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': input_text
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": self.basic_button
                        }
                    }
                )

        return message_val