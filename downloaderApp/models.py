from django.db import models


class DownloadedVideo(models.Model):
    video_url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title