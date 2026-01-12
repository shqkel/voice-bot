import base64
from dotenv import load_dotenv
from openai import OpenAI
import os 

load_dotenv() # 현재경로의 .env파일을 읽어서 환경변수로 등록
# print(os.environ['OPENAI_API_KEY'])
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
# client = OpenAI(api_key=OPENAI_API_KEY)
client = OpenAI()

def stt(audio):
    # 파일로 저장
    output_filepath = 'input.mp3'
    audio.export(output_filepath, format='mp3')

    # stt변환
    with open(output_filepath, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f
        )
    # 음원파일 삭제
    os.remove(output_filepath)

    return transcription.text


def ask_gpt(messages, model):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=1,
        max_completion_tokens=4096
    ).choices[0].message.content

def tts(response: str):
    # tts변환
    filename = 'output.mp3'
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='alloy',
        input=response
    ) as resp:
        resp.stream_to_file(filename)

    # 음원이진파일을 base64문자열로 변환
    with open(filename, 'rb') as f:
        data = f.read()
        b64_encoded = base64.b64encode(data).decode() # 이진데이터 -> b64인코딩(이진) -> 문자열디코딩

    # 음원파일 삭제
    os.remove(filename)

    return b64_encoded