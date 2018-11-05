from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from app import button
from app import crawcafeteria
from app import db_control


def keyboard(request):

    return  JsonResponse(
        {
            "type": "buttons",
            "buttons": ["채움관", "이룸관", "기숙사", "별점 주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
        }
    )

@csrf_exempt
def message(request):

    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    content_name = received_json['content']
    #content_name_jeon = received_json['content'][1]
    user_name = received_json['user_key']

    pre_input_text = db_control.pre_value(user_name)

    pre_pre_input_text = db_control.pre_pre_value(user_name)

    db_control.key_insert(user_name, content_name)

    #print(pre_input_text)
    #print(pre_pre_input_text)

    #input_text = button.button_check(content_name)

    throw_message = button.message_make(content_name, pre_input_text, pre_pre_input_text, user_name)

    return throw_message.return_message()


#사진 전송을 로컬의 이미지를 업로드 하는 기능은 제공하지 않고 있음
#사진 전송 기능 사용하려면 별도로 웹에 올려둬야함
#플러스친구 홈페이지에 올리면 되지않나 고민중


def trash():
    """
        elif input_text == '사진 전송':
            return JsonResponse(
                {
                    'message': {
                        'text': input_text,
                        'photo' : {
                            "url" : "http://i1.ruliweb.com/cmt/18/11/03/166d9718352368a8a.jpg", #"C:\project/est_grim.jpg",
                            "width": 720,
                            "height":630
                        }
                    },
                    "keyboard": {
                        "type": "buttons",
                        "buttons": ["채움관", "이룸관", "기숙사", "별점 확인&주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인","사진 전송"]
                    }
                }
            )
    """

    """
        if content_name == '별점 확인&주기' or "학식(중식)" or "학식(석식)" or "기숙사(조식)" or "기숙사(중식)" or "기숙사(석식)" or "처음으로":
            input_text = button.star_check(content_name)

            if input_text == "별점":
                return JsonResponse(
                    {
                        'message': {
                            'text': '평가할 식단을 선택하세요' #+ str(content_name_jeon)
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["학식(중식)", "학식(석식)", "기숙사(조식)", "기숙사(중식)", "기숙사(석식)", "처음으로"]
                        }
                    }
                )
            elif input_text == "채움이룸_중식":
                return JsonResponse(
                    {
                        'message': {
                            'text': '별점을 매겨주세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★", "처음으로"]
                        }
                    }
                )
            elif input_text == "채움이룸_석식":
                return JsonResponse(
                    {
                        'message': {
                            'text': '별점을 매겨주세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★", "처음으로"]
                        }
                    }
                )
            elif input_text == "기숙사_조식":
                return JsonResponse(
                    {
                        'message': {
                            'text': '별점을 매겨주세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★", "처음으로"]
                        }
                    }
                )
            elif input_text == "기숙사_중식":
                return JsonResponse(
                    {
                        'message': {
                            'text': '별점을 매겨주세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★", "처음으로"]
                        }
                    }
                )
            elif input_text == "기숙사_석식":
                return JsonResponse(
                    {
                        'message': {
                            'text': '별점을 매겨주세요'
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★", "처음으로"]
                        }
                    }
                )
            else:
                return JsonResponse(
                    {
                        'message': {
                            'text': input_text
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 확인&주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
                        }
                    }
                )
        elif content_name == '채움관' :
            input_text = button.button_check(content_name)

            if input_text == '내일':
                return JsonResponse(
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
            else:
                return JsonResponse(
                    {
                        'message': {
                            'text': input_text
                        },
                        "keyboard": {
                            "type": "buttons",
                            "buttons": ["채움관", "이룸관", "기숙사", "별점 확인&주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
                        }
                    }
                )
    
    a = JsonResponse(
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
    b = JsonResponse(
            {
                'message': {
                    'text': input_text + ' \n' + str(pre_input_text)
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ["채움관", "이룸관", "기숙사", "별점 확인&주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
                }
            }
        )
    if input_text == '내일':
        return a
    else:
        return b



    """