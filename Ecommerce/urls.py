
from django.urls import path
from .views import (home,
    ProduitDetailView,
    ProduitUpdateView,
    ProduitDeleteView,
    add_to_cart,
    remove_to_cart,
    mypanier,
    add_quantite,
    remove_quantite)

urlpatterns = [
    path('',home,name = 'Ecommerce-home'),
    path('articles/<int:pk>',ProduitDetailView.as_view(),name = 'article_link'),
    path('articles/<int:pk>/update',ProduitUpdateView.as_view(),name = "article-update"),
    path('articles/<int:pk>/delete',ProduitDeleteView.as_view(),name = "article-delete"),
    path('articles/<int:pr_pk>/addCart',add_to_cart,name = "article-cart"),
    path('panier/',mypanier,name = "panier"),
    path('panier/<int:pr_pk>/plusq',add_quantite,name = "add-quantite"),
    path('panier/<int:pr_pk>/moinsq',remove_quantite,name = "remove-quantite"),
    path('panier/<int:pr_pk>/removeCart',remove_to_cart,name = "remove_cart"),
]