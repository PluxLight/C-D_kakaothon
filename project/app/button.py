from app import crawcafeteria
from app import weather

def button_check(button):
    if button == '채움관':
        return crawcafeteria.cheaum()
    elif button == '채움관(내일)':
        return crawcafeteria.cheaum_tomorrow()
    elif button == '이룸관':
        return crawcafeteria.erum()
    elif button == '이룸관(내일)':
        return crawcafeteria.erum_tomorrow()
    elif button == '기숙사':
        return crawcafeteria.domitori()
    elif button == '기숙사(내일)':
        return crawcafeteria.domitori_tomorrow()
    elif button == '양식당':
        return crawcafeteria.restaurant()
    elif button == '오늘의 날씨':
        return weather.main_action()
    elif button == '내일의 메뉴 확인':
        return '내일'
    elif button == '처음으로':
        return '처음으로'
    elif button == '별점 확인&주기':
        return '미구현'
    else:
        return '미구현'

def star_check(button):
    if button == '학식(중식)':
        return '채움이룸_중식'
    elif button == '학식(석식)':
        return '채움이룸_석식'
    elif button == '기숙사(조식)':
        return '기숙사_조식'
    elif button == '기숙사(중식)':
        return '기숙사_중식'
    elif button == '기숙사(석식)':
        return '기숙사_석식'
    elif button == '처음으로':
        return '처음으로'
    elif button == '별점 확인&주기':
        return '별점'
    else:
        return '미구현'