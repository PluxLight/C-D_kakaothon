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
            "buttons": ["교내식당", "학교 주변식당", "별점 주기",  "오늘의 날씨", "자취/하숙 정보"]
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

    # print("전"+pre_input_text)
    # print("전 전"+pre_pre_input_text)
    # print("현재" + content_name)
    # print(user_name) #오류 발생시 확인용 print문

    #input_text = button.button_check(content_name)

    throw_message = button.message_make(content_name, pre_input_text, pre_pre_input_text, user_name)

    return throw_message.return_message()


#사진 전송을 로컬의 이미지를 업로드 하는 기능은 제공하지 않고 있음
#사진 전송 기능 사용하려면 별도로 웹에 올려둬야함
#플러스친구 홈페이지에 올리면 되지않나 고민중
