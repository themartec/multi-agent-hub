import datetime
import os
import re
import time

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel
from app.schemas.models import OpenAIModelName
from app.schemas.settings import EnglishStyle
from youtube_transcript_api.proxies import WebshareProxyConfig

load_dotenv()


class Translate(BaseModel):
    """Translate the given text to the required language."""
    translated_text: str


def translate(raw_text: str, en_type: EnglishStyle = EnglishStyle.AMERICAN):
    llm_model = ChatOpenAI(model=OpenAIModelName.GPT_41, max_tokens=5000, temperature=0)
    translator = llm_model.with_structured_output(Translate, method="json_mode")
    output = translator.invoke(f"""You're a experienced translator. Translate the given {raw_text} to {en_type.value} 
    language. Don't forget to use popular idiom, slang or colloquialism to make the language more natural. Make sure to return a JSON 
    blob with key 'translated_text'""")
    return output.translated_text


def _mapping_youtube(link: str):
    if 'youtu.be' in link:
        video_id = link.split('/')[-1]
        print(f"video_id: {video_id}")
    else:
        video_id = link.split('=')[1]
    return video_id


def youtube_transcribe(video_link: str):
    proxy_config = WebshareProxyConfig(
        proxy_username="qnhgnxgc",
        proxy_password="wqgywmp2er8d",
    )

    before_time = datetime.datetime.now()
    ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
    video_id = _mapping_youtube(video_link)
    transcript_list = ytt_api.list(video_id)
    transcript = transcript_list.find_transcript(['ja', 'en', 'zh-Hans'])
    final_output = None
    counter = 0
    while final_output is None and counter < 3:
        counter += 1
        try:
            if video_id is not None:
                if 'en' in transcript.language_code:
                    fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
                    text_lines = [entry.text for entry in fetched_transcript]
                    final_output = " ".join(text_lines)
                else:
                    translated_transcript = transcript.translate('en')
                    final_output = translated_transcript.fetch(video_id)
                    text_lines = [entry.text for entry in final_output]
                    final_output = " ".join(text_lines)

                after_time = datetime.datetime.now()
                delta_time = (after_time - before_time).total_seconds()
                print(f"[Debug] Youtube Scrape time: {delta_time}")
                return final_output
            else:
                return "Please check the video link if it is valid Youtube link."
        except:
            print(f"[Debug] Youtube Scrape Retry: {counter}")
            final_output = None
            time.sleep(10)


#
# def download_audio_from_url(raw_url: str):
#     response = requests.get(raw_url, stream=True)
#     response.raise_for_status()  # Raise an error if the download fails
#     with open("test_video_demo.mp4", 'wb') as f:
#         for chunk in response.iter_content(chunk_size=8192):
#             f.write(chunk)


# @tool
# def get_transcribe_from_youtube(raw_url: str):
#     """Use this to crawl the content when user input the URL"""
#     if 'youtube' in raw_url:
#         return youtube_transcribe(raw_url)
#     else:
#         return None
#     # print(f"raw_url: {raw_url}")
#     # # download_audio_from_url(raw_url)
#     # time.sleep(1)
#     # client = OpenAI()
#     # url = "test_video_demo.mp4"
#     # audio_file = open(url, "rb")
#     # init_time = datetime.datetime.now()
#     # transcription = client.audio.transcriptions.create(
#     #     model="whisper-1",
#     #     file=audio_file,
#     #     response_format="text"
#     # )
#     # cur_time = datetime.datetime.now()
#     # delta_time = cur_time - init_time
#     # print(f"delta_time: {delta_time.total_seconds()} seconds")
#     #
#     # return transcription

def _format_youtube_description(description: str):
    if description is None:
        return None
    output_format = description.replace("\n", " ")
    output_format = re.sub(r".+Description", "", output_format)
    output_format = re.sub(r"\.\.more.+", "", f"Description: {output_format}")
    output_format = re.sub(r"Transcript.+", "", f"{output_format}")
    output_format = re.sub(r"\[https.+?\)", "", f"{output_format}")
    before_time = datetime.datetime.now()
    output_format = translate(output_format, EnglishStyle.AMERICAN)
    after_time = datetime.datetime.now()
    delta_time = (after_time - before_time).total_seconds()
    print(f"[Debug] translate time: {delta_time}")
    return output_format


def _scrape_by_jina(raw_url: str):
    url = f"https://r.jina.ai/{raw_url}"
    headers = {
        "Authorization": f'Bearer {os.getenv("JINA_API_KEY")}'
    }
    response = requests.get(url, headers=headers)
    return response.text


@tool
def get_content_from_url(raw_url: str):
    """Use this to crawl the content when user input the URL"""
    if 'youtube' in raw_url or 'youtu.be' in raw_url:
        youtube_trans = youtube_transcribe(raw_url)
        output_format = _format_youtube_description(_scrape_by_jina(raw_url))
        return f"**Video Transcript**:\n{youtube_trans}\n**Video Description**: {output_format}"
    else:
        return _scrape_by_jina(raw_url)
