from django.db import models


# Create your models here.
class ImageFile(models.Model):
    img = models.ImageField(upload_to="%Y%m%d")
    imgX = models.CharField(max_length=50)
    imgY = models.CharField(max_length=50)
