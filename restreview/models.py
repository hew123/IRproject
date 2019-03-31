from django.db import models

# Create your models here.
class Restaurant(models.Model):
    #id = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    ave_rating = models.FloatField()
    #review = models.ManyToManyField('Review',blank=True)


class Review(models.Model):
    #id = models.IntegerField()
    comment = models.TextField()
