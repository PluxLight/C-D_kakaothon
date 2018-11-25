from app import crawcafeteria
from app import weather
from app import db_control
from django.http import JsonResponse
import datetime


class message_make:

    def __init__(self, cur_text, pre_text, pre_pre_text, user_key):
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
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "박물관", "오늘의 날씨", "내일의 메뉴 확인"]
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

    def button_check(self):
        if self.cur_text == '채움관':
            return crawcafeteria.cheaum()
        elif self.cur_text == '채움관(내일)':
            return crawcafeteria.cheaum_tomorrow()
        elif self.cur_text == '이룸관':
            return crawcafeteria.erum()
        elif self.cur_text == '이룸관(내일)':
            return crawcafeteria.erum_tomorrow()
        elif self.cur_text == '기숙사':
            return crawcafeteria.domitori()
        elif self.cur_text == '기숙사(내일)':
            return crawcafeteria.domitori_tomorrow()
        elif self.cur_text == '양식당':
            return crawcafeteria.restaurant()
        elif self.cur_text == '맘스터치(버거)':
            return crawcafeteria.moms('버거')
        elif self.cur_text == '맘스터치(치킨)':
            return crawcafeteria.moms('치킨')
        elif self.cur_text == '맘스터치(스낵)':
            return crawcafeteria.moms('스낵')
        elif self.cur_text == '오늘의 날씨':
            return weather.main_action()
        elif self.cur_text == '내일의 메뉴 확인':
            return '내일'
        else:
            return '미구현'

    def return_message(self):

        input_text = self.button_check()

        if self.cur_text == '내일의 메뉴 확인':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식당을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["채움관(내일)", "이룸관(내일)", "기숙사(내일)", "처음으로"]
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
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식단을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["중식", "석식", "처음으로"]
                    }
                }
            )
        elif self.cur_text == '기숙사' and self.pre_text == '별점 주기':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식단을 선택하세요'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["조식", "중식", "석식", "처음으로"]
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
                message_val = JsonResponse(
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
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "박물관", "오늘의 날씨", "내일의 메뉴 확인"]
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
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "박물관", "오늘의 날씨", "내일의 메뉴 확인"]
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
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "박물관", "오늘의 날씨", "내일의 메뉴 확인"]
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

        elif self.cur_text == '처음으로':
            message_val = JsonResponse(
            {
                'message': {
                    'text': '처음으로 돌아갑니다'
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "박물관", "오늘의 날씨", "내일의 메뉴 확인"]
                }
            }
        )
        else:
            message_val = JsonResponse(
            {
                'message': {
                    'text': input_text
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "박물관", "오늘의 날씨", "내일의 메뉴 확인"]
                }
            }
        )

        return message_val





"""

    elif button == '사진 전송':
        return '사진 전송'
"""