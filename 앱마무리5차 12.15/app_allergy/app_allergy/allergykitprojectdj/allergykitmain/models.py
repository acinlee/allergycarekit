from django.db import models

# Create your models here.
class User(models.Model):
    al_ID = models.CharField(max_length=20, null=True, blank=False)
    al_PW = models.CharField(max_length=20, null=True, blank=False)
    al_Name = models.CharField(max_length=20, null=True, blank=False)
    al_Email = models.CharField(max_length=50, null=True, blank=False)
    al_Birth = models.CharField(max_length=50, null=True, blank=False)
    al_Height = models.CharField(max_length=50, null=True, blank=False)
    al_Weight = models.CharField(max_length=50, null=True, blank=False)
    al_Gender = models.CharField(max_length=1, null=True, blank=False) #0=man, 1=woman

class UsrAllergy(models.Model):
    User_Allergy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    Al_CreateDate = models.DateTimeField(null=True, blank=False)
    Al_Files = models.FileField(null=True, blank=True)
    fish_al = models.CharField(max_length=6, default=0)
    flour_al = models.CharField(max_length=6, default=0)
    milk_al = models.CharField(max_length=6, default=0)
    meat_al = models.CharField(max_length=6, default=0)
    fruit_al = models.CharField(max_length=6, default=0)
    cheese_al = models.CharField(max_length=6, default=0)
    alcohol_al = models.CharField(max_length=6, default=0)
    egg_al = models.CharField(max_length=6, default=0)
    chicken_al = models.CharField(max_length=6, default=0)
    vegetable_al = models.CharField(max_length=6, default=0)

    class Meta:
        get_latest_by = ['Al_CreateDate']