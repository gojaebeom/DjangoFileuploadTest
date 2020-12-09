from django.db import models


# Create your models here.
class ImageFile(models.Model):
    img = models.ImageField(upload_to="%Y%m%d")
    origin_name = models.CharField(max_length=100)
    let = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
