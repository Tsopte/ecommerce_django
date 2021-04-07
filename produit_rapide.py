import json
from Ecommerce.models import Produit

with open('data.json') as f:
    all_p = json.load(f)

for p in all_p:
   pro = Produit(title = p['title'],description = p['info'],image = p['img'],price=p['price'],categorieId=p['category'],promo=p['promo'])
   pro.save()