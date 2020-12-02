from datetime import datetime
from django.db import models


# Create your models here.

class Executions(models.Model):
    date_execution = models.DateTimeField(default=datetime.now, blank=True)
    state = models.CharField(max_length=150, null=True)
    country = models.CharField(max_length=150)
    end_date = models.CharField(max_length=8, null=True)
    start_date = models.CharField(max_length=8)

    class Meta:
        db_table = 'executions_history'
