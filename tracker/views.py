from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Time, Medicine
# Create your views here.
class NewMedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'time', 'number']
def index(request):
    return render(request, "tracker/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tracker/register.html")

def create_medicine(request):
    if request.method == "POST":
        medicine_form = NewMedicineForm(request.POST)
        if medicine_form.is_valid():
            name = medicine_form.cleaned_data["name"]
            time = medicine_form.cleaned_data["time"]
            number = medicine_form.cleaned_data["number"]
            patient = request.user
            new_medicine = Medicine(
                name = name,
                time = time,
                patient = patient,
                number = number
            )
            new_medicine.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "tracker/create_medicine.html", {
        "medicine_form": NewMedicineForm
    })

def morning(request):
    time = Time.objects.get(time ="morning")
    medicines = Medicine.objects.filter(time=time)
    return render(request, "tracker/list.html", {
        "medicines": medicines
    })

def afternoon(request):
    time = Time.objects.get(time="afternoon")
    medicines = Medicine.objects.filter(time=time)
    return render(request, "tracker/list.html", {
        "medicines": medicines
    })

def night(request):
    time = Time.objects.get(time="night")
    medicines = Medicine.objects.filter(time=time)
    return render(request, "tracker/list.html", {               
        "medicines": medicines
    })

def take(request, medicine_id):
    medicine = Medicine.objects.get(id = medicine_id)
    if medicine.taken == False:
        medicine.taken = True
    else:
        medicine.taken = False
    medicine.save()
    return render(request, "tracker/index.html")

def reset(request):
    medicines = Medicine.objects.all()
    for medicine in medicines:
        medicine.taken = False
        medicine.save()
    return render(request, "tracker/index.html")