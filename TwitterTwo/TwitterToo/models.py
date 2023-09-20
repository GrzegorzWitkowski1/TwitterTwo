from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True,
    )

    def __str__(self) -> str:
        return self.user.username