from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from app import button
from app import crawcafeteria


def keyboard(request):

    return  JsonResponse(
        {
            "type": "buttons",
            "buttons": ["채움관", "이룸관", "기숙사", "별점 확인&주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
        }
    )

@csrf_exempt
def message(request):

    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    content_name = received_json['content']
    #content_name_jeon = received_json['content'][1]
    user_name = received_json['user_key']

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
                    'text': input_text # + ' ' + str(content_name) + '\n' + str(user_name)
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ["채움관", "이룸관", "기숙사", "별점 확인&주기", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
                }
            }
        )











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



"""