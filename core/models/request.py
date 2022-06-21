from django.db import models


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    reason = models.TextField()
    employee = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
