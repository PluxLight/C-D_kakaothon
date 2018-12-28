from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from app import button
from app import response_manage


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
    user_name = received_json['user_key']

    r_m = response_manage.key_manage()

    pre_input_text = r_m.pre_value(user_name) #사용자가 한단계전에 입력한 값을 변수에 저장
    pre_pre_input_text = r_m.pre_pre_value(user_name) #사용자가 두단계전에 입력한 값을 변수에 저장
    r_m.key_insert(user_name, content_name) #사용자가 현재 입력한 값을 DB에 저장

    send_message = button.message_make(content_name, pre_input_text, pre_pre_input_text, user_name) #사용자에게 입력한 값을 판별하여 보낼 메세지를 준비

    return send_message.return_message()


#사진 전송을 로컬의 이미지를 업로드 하는 기능은 제공하지 않고 있음
#사진 전송 기능 사용하려면 별도로 웹에 올려둬야함
#플러스친구 홈페이지에 올리면 되지않나 고민중
