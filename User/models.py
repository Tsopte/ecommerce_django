from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image


regions = [ ("1","Centre"),("2","Littoral"),("3","Ouest"),
        ("4","Nord-Ouest"),("5","Sud-Ouest"),("6","Est"),
        ("7","Sud"),("8","Adamaoua"),("9","Extreme-Nord"),
        ("10","Nord")
]


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = (models.CASCADE))
    image = models.ImageField(upload_to="profile_pics",default = "default.jpg")

    #addresse
    region = models.CharField(choices = regions,max_length = 20)
    ville = models.CharField(max_length = 20)
    quartier = models.CharField(max_length = 20)

    #numéro whatsapp
    phone_regex = RegexValidator(regex=r'^\d{9}$', message="votre whatsapp doit avoir 9 chiffres")
    whatsapp = models.CharField(validators=[phone_regex],max_length = 9,blank = False)


    def save(self,*args,**kwargs):
        super().save(*args,**kwargs) #on appel la methode save de la classe parent pour sauvegarder le profile

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
