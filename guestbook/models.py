from django.db import models


# Create your models here.
class Guestbook(models.Model):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    content = models.CharField(max_length=480)
    regdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Guestbook({self.name}, {self.password}, {self.content}, {self.regdate})'

