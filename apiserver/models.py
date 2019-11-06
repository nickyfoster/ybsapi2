from django.db import models

# TODO add db replication (see settings db routing)
class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    vk_id = models.IntegerField(verbose_name="User's VK id")

    class Meta:
        ordering = ('created',)


