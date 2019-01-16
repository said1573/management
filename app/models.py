from django.db import models

# Create your models here.

class Member(models.Model):

    user_id = models.CharField(max_length=20, primary_key=True)
    user_pw = models.CharField(max_length=20)
    user_email = models.CharField(max_length=20)
    user_name = models.CharField(max_length=10)

    def __str__(self):
        return self.user_id

class Record(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    address = models.TextField()
    buildingname = models.TextField()
    own = models.TextField()
    num1 = models.TextField()
    num2 = models.TextField()
    num3 = models.TextField()
    num4 = models.TextField()
    num5 = models.TextField()
    num6 = models.TextField()
    num7 = models.TextField()
    num8 = models.TextField()
    num9 = models.TextField()
    num10 = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
