import os, io
from pathlib import Path

from django.conf import settings
from google.cloud import vision
from gtts import gTTS

BASE_DIR = Path(__file__).resolve().parent.parent

env_list = dict()

local_env = open(os.path.join(BASE_DIR, '.env'))

while True:
    line = local_env.readline()
    if not line:
        break
    line = line.replace('\n', '')
    start = line.find('=')
    key = line[:start]
    value = line[start+1:]
    env_list[key] = value

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_list['GOOGLE_API_KEY'] # 본인의 api 키 넣기

def detect_text(path):
    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL

    # google vision api 작동
    client = vision.ImageAnnotatorClient()

    # 이미지를 visionAPI가 읽을 수 있는 형태로 가공
    # 'rb' == 바이너리 읽기 모드
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # 이미지에서 text 뽑아내기
    response = client.text_detection(image=image)
    texts = response.text_annotations

    text_list = []
    for text in texts:
        text_list.append(text.description)

    tts_2 = gTTS(text=text_list[0], lang='en')
    tts_2.save(base_url + "text.mp3")


    return text_list
