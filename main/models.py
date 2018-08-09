from django.db import models
from django.contrib.postgres.fields import ArrayField


class Algo(models.Model):
    algo_name = models.CharField(max_length=255, default='', blank=True)
    positions = ArrayField(models.IntegerField(blank=True), blank=True, default=list)
    daily_pnl = ArrayField(models.FloatField(blank=True), blank=True, default=list)
    avg_pnl = models.FloatField(blank=True)
