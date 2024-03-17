from django.db import models


class HistTrack(models.Model):
    user_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    img_url = models.CharField(max_length=300)

    def __str__(self):
        return str(self.title)
