from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
# Create your models here.

class Categorie(models.Model):
    title = models.CharField(max_length = 50)

class Produit(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    image = models.ImageField(upload_to = 'products')
    price = models.DecimalField(max_digits = 7,decimal_places = 2)
    promo =  models.IntegerField()
    categorieId =  models.IntegerField()

    def get_absolute_url(self):
        return reverse("article_link",kwargs = {'pk' : self.pk}) 
        #return le chemin complet vers une route sera utiliser après les delete et les update par exemple

class ProduitPanier(models.Model):
    produit_in = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ajout = models.DateTimeField()

