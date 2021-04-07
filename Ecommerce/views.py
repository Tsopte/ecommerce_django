from django.shortcuts import render,redirect
from Ecommerce.models import Produit
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.http import HttpResponse,JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from django.utils.timezone import now

from .models import Produit,ProduitPanier
# Create your views here.




def home(request):

    #gérons le panierCount
    nb_produit = 0
    
    if request.user.is_authenticated:
        nb_produit = ProduitPanier.objects.filter(user = request.user).count()

    #occupons nous des produits
    produits = Produit.objects.all()
    promo_prix = list()

    for p in produits:
        promo_prix.append(((100-p.promo)/100)*float(p.price))

    return render(request,'Ecommerce/home.html',{'produits' : zip(produits,promo_prix),'nb_produit' : nb_produit})



@csrf_exempt
def add_to_cart(request,pr_pk):
    
    if request.method == "POST":
        if request.user.is_authenticated:
            pro = get_object_or_404(Produit, pk=pr_pk)
            
            if ProduitPanier.objects.filter(produit_in = pro,user = request.user).count() == 0:
                #d.day() pour obtenir le jour
                p_in = ProduitPanier(produit_in = pro,quantite = 1,user = request.user,ajout = now())
                p_in.save()
                r = HttpResponse()
                r.status_code = 202
                return r
            else:
                r = HttpResponse()
                r.status_code = 302
                return r
        else:
            r = HttpResponse(request.path)
            r.status_code = 403
            return r
    
    else:
        r = HttpResponse(request.path)
        r.status_code = 405
        return r

def remove_to_cart(request,pr_pk):
    
    
    if request.user.is_authenticated:
        pro = get_object_or_404(Produit, pk=pr_pk)
        pro_in = get_object_or_404(ProduitPanier, produit_in = pro,user = request.user)
        
        if pro_in:
            pro_in.delete()
            r = HttpResponse()
            r.status_code = 202
            return redirect("/panier")
    else:
        r = HttpResponse(request.path)
        r.status_code = 403
        return r
    

@csrf_exempt
def add_quantite(request,pr_pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            pro = get_object_or_404(Produit, pk=pr_pk)
            pro_in = get_object_or_404(ProduitPanier, produit_in = pro,user = request.user)
            
            if pro_in:
                pro_in.quantite += 1
                pro_in.save()
                r = HttpResponse()
                r.status_code = 202
                return r

        else:
            r = HttpResponse(request.path)
            r.status_code = 403
            return r
    
    else:
        r = HttpResponse(request.path)
        r.status_code = 405
        return r

@csrf_exempt
def remove_quantite(request,pr_pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            pro = get_object_or_404(Produit, pk=pr_pk)
            pro_in = get_object_or_404(ProduitPanier, produit_in = pro,user = request.user)
            
            if pro_in and pro_in.quantite>=2:
                pro_in.quantite -= 1
                pro_in.save()
                r = HttpResponse()
                r.status_code = 202
                return r
            elif pro_in.quantite<2:
                r = HttpResponse()
                r.status_code = 202
                return r


        else:
            r = HttpResponse(request.path)
            r.status_code = 403
            return r
    
    else:
        r = HttpResponse(request.path)
        r.status_code = 405
        return r

        



##################################################################################################
#CRUD sur les produits


class ProduitUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Produit
    fields = ['title','price','promo','description','image']

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class ProduitDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Produit
    success_url = "/"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class ProduitDetailView(DetailView):
    model = Produit

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        the_product = Produit.objects.filter(pk = self.kwargs['pk'])[0]
        
        context['promo_prix'] = ((100-the_product.promo)/100)*float(the_product.price)
        if self.request.user.is_authenticated:
            context['nb_produit'] = ProduitPanier.objects.filter(user = self.request.user).count()
        return context


##################################################################################################
#CRUD sur le panier

@login_required
def mypanier(request):

    #gérons le panierCount
    nb_produit = ProduitPanier.objects.filter(user = request.user).count()

    #occupons nous des produits

    pr = ProduitPanier.objects.filter(user = request.user)

    promo_prix = list()

    for p in pr:
        promo_prix.append(((100-p.produit_in.promo)/100)*float(p.produit_in.price))



    context = {
        'produits' : zip(pr,promo_prix),
        'nb_produit' : nb_produit
    }

    return render(request,"Ecommerce/panier.html",context)
    
