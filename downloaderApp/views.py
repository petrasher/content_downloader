import os
import threading
import json
import schedule
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube

def delete_file(video_path):
    if os.path.exists(video_path):
        os.remove(video_path)
        print('deleted')

def schedule_job(video_path):
    schedule.every(10).minutes.do(delete_file, video_path)
    while True:
        schedule.run_pending()
        time.sleep(10)

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('video_url')
        try:
            yt = YouTube(video_url)
            yt_streams = yt.streams.get_highest_resolution()
            video_path = yt_streams.download()

            threading.Thread(target=schedule_job, args=(video_path,)).start()
            return HttpResponse(f'Видео успешно скачано: {video_path}')
        except Exception as e:
            return HttpResponse(f'Ошибка при скачивании видео: {e}')
    return render(request, 'download.html')






