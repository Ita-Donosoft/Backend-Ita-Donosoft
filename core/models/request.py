from django.db import models


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    reason = models.TextField()
    employee = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Request, self).save(*args, **kwargs)
