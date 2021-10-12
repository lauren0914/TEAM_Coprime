from django.conf import settings
from gtts import gTTS
from django.shortcuts import render

# Create your views here.

def index(request):
    intro = "캔유텔미는 시각장애인을 위한 캔 음료 구분 서비스입니다.\
    지금 이미지를 업로드하고 예측결과를 받아보세요! 캔을 누르면 시작됩니다"

    tts_intro = gTTS(text=intro, lang='ko')
    tts_intro.save(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + "intro.mp3")

    tts_intro = settings.MEDIA_ROOT_URL + settings.MEDIA_URL + "intro.mp3"
    context = {'tts_intro': tts_intro}

    return render(request, 'main/index.html', context)