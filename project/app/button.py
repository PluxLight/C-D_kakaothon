from app import crawcafeteria
from app import weather
from app import db_control
from django.http import JsonResponse


class message_make:

    def __init__(self, cur_text, pre_text, pre_pre_text, user_key):
        self.cur_text = cur_text
        self.pre_text = pre_text
        self.pre_pre_text = pre_pre_text
        self.user_key = user_key

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
                        'text': '식당을 선택'
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
                        'text': '식당을 선택'
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
                        'text': '식단을 선택'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["조식", "중식", "석식", "처음으로"]
                    }
                }
            )
        elif self.cur_text == '기숙사' and self.pre_text == '별점 주기':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '식단을 선택'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["조식", "중식", "석식", "처음으로"]
                    }
                }
            )
        elif self.cur_text == '조식' or self.cur_text == '중식' or self.cur_text == '석식':
            message_val = JsonResponse(
                {
                    'message': {
                        'text': '별점을 선택'
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆", "처음으로"]
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
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
                        }
                    }
                )
            else:
                message_val = JsonResponse(
                    {
                        'message': {
                            'text': '별점의 중복 투표는 제한되어 있습니다.'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
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
                    "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
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
                    "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
                }
            }
        )

        return message_val





"""

    elif button == '사진 전송':
        return '사진 전송'
"""