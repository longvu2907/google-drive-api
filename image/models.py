from unicodedata import category
from django.db import models

# Create your models here.
class Image(models.Model):
    id = models.CharField(
        max_length=100, 
        primary_key=True
    )

    name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=100
    )

    category_id = models.CharField(
        max_length=100
    )

    image_url = models.URLField()

    created_at = models.DateTimeField()