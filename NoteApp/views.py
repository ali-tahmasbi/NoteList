from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import List
from .forms import ListForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.user = request.user
            list.save()
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = ListForm()
    
    lists = List.objects.filter(user=request.user)
    return render(
        request,
        "home.html",{
            "lists": lists,
            "form": form
        }
    )
        
@login_required
def delete(request, id):
    if request.method == "POST":
        delete = List.objects.get(id=id, user=request.user)
        delete.delete()
        return redirect("home")

@login_required
def update(request, id):
    list = List.objects.get(id=id, user=request.user)
    if request.method == "POST":
        form = ListForm(request.POST, instance=list)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    else:
        form = ListForm(instance=list)
        
        
    return render(
        request,
        "update.html",
        {
            "list": list,
            "form": form,
        }
    )  
    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)
    else: 
        form = UserCreationForm()
        
    return render(
        request, "register.html",
        {
            "form": form,
        }
    )