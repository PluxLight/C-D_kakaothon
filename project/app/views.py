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
            "buttons": ["채움관", "이룸관", "기숙사", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
        }
    )

@csrf_exempt
def message(request):

    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    content_name = received_json['content']

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
                "buttons": ["채움관", "이룸관", "기숙사", "양식당", "오늘의 날씨", "내일의 메뉴 확인"]
            }
        }
    )
