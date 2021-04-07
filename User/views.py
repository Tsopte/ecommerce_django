from django.shortcuts import render,redirect
from .form import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,ProfileCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_protect

from .models import Profile
from Ecommerce.models import ProduitPanier




@csrf_protect
def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form  = ProfileCreateForm(request.POST)
        
        if u_form.is_valid() and p_form.is_valid():
            
            data = request.POST
            
            user_save = u_form.save()

            p = Profile.objects.create(user=user_save,
            region = data['region'],quartier = data['quartier'],ville = data['ville'],whatsapp = data['whatsapp'])
            p.save()
            

            
            
            username = u_form.cleaned_data.get('username')
            messages.success(request,'{} Votre compte a été crée avec succès'.format(username))
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form  = ProfileCreateForm()

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'User/register.html',context)


@login_required
def profile(request):

    #gérons le panierCount
    global nb_produit
    
    if request.user.is_authenticated:
        nb_produit = ProduitPanier.objects.filter(user = request.user).count()

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance = request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request,'Votre compte a bien été modifié')

            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)


    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'nb_produit' : nb_produit
    }

    return render(request,"User/profile.html",context)
