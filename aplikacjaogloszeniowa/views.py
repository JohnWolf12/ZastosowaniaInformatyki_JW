from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UpdateUserForm, UpdateUzytkownikForm, AnnouncementForm, WiadomoscForm
from .models import Kategoria, Ogloszenie, Uzytkownik, Wiadomosc


def index(request):
    kategorie = Kategoria.objects.all()
    context = {
        'kategorie': kategorie,
    }
    return render(request, 'aplikacjaogloszeniowa/index.html', context)


def register_view(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            registerform.save()
            return redirect("/logowanie")
    else:
        registerform = RegisterForm()
    context = {
        'registerform': registerform
    }
    return render(request, 'aplikacjaogloszeniowa/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request):
    uzytkownik = request.user.uzytkownik
    ogloszenia = Ogloszenie.objects.filter(uzytkownik=uzytkownik).order_by('-id')
    context = {
        'ogloszenia': ogloszenia
    }
    return render(request, 'aplikacjaogloszeniowa/profile.html', context)


@login_required
def profileEdit_view(request):
    if request.method == 'POST':
        userform = UpdateUserForm(request.POST, instance=request.user)
        uzytkownikform = UpdateUzytkownikForm(request.POST, instance=request.user.uzytkownik)
        if userform.is_valid() and uzytkownikform.is_valid():
            userform.save()
            uzytkownikform.save()
            return redirect("/profil")
    else:
        userform = UpdateUserForm(instance=request.user)
        uzytkownikform = UpdateUzytkownikForm(instance=request.user.uzytkownik)
    context = {
        'userform': userform,
        'uzytkownikform': uzytkownikform
    }
    return render(request, 'aplikacjaogloszeniowa/profileEdit.html', context)


@login_required
def addAnnouncement_view(request):
    if request.method == 'POST':
        addannouncementform = AnnouncementForm(request.POST)
        addannouncementform.instance.uzytkownik = request.user.uzytkownik
        if addannouncementform.is_valid():
            addannouncementform.save()
            return redirect("/profil")
    else:
        addannouncementform = AnnouncementForm()
    context = {
        'addannouncementform': addannouncementform
    }
    return render(request, 'aplikacjaogloszeniowa/announcementAdd.html', context)


@login_required
def editAnnouncement_view(request, id):
    ogloszenie = get_object_or_404(Ogloszenie, pk=id, uzytkownik=request.user.uzytkownik)
    if request.method == 'POST':
        editannouncementform = AnnouncementForm(request.POST, instance=ogloszenie)
        if editannouncementform.is_valid():
            editannouncementform.save()
            return redirect("/profil")
    else:
        editannouncementform = AnnouncementForm(instance=ogloszenie)
    context = {
        'editannouncementform': editannouncementform
    }
    return render(request, 'aplikacjaogloszeniowa/announcementEdit.html', context)


@login_required
def deleteAnnouncement_view(request, id):
    uzytkownik = request.user.uzytkownik
    Ogloszenie.objects.filter(uzytkownik=uzytkownik, id=id).delete()
    return redirect('/profil')


def announcements_view(request):
    kategorie = Kategoria.objects.all()
    if 'q' in request.GET:
        nazwa = request.GET.get("q")
    else:
        nazwa = ''
    if 'k' in request.GET:
        kategoria = request.GET.get("k")
    else:
        kategoria = ''
    if 'min' in request.GET:
        cenamin = request.GET.get("min")
        if cenamin == '':
            cmin = ''
            cenamin = '0'
        else:
            cmin = cenamin
    else:
        cmin = ''
        cenamin = '0'
    if 'max' in request.GET:
        cenamax = request.GET.get("max")
        if cenamax == '':
            cmax = ''
            cenamax = '99999999'
        else:
            cmax = cenamax
    else:
        cmax = ''
        cenamax = '99999999'
    if 'sort' in request.GET:
        sort = request.GET.get("sort")
    else:
        sort = ''
    if kategoria == '':
        if sort == '1':
            ogloszenia = Ogloszenie.objects.filter(nazwa__icontains=nazwa, cena__gte=cenamin,
                                                   cena__lte=cenamax).order_by('cena')
        elif sort == '2':
            ogloszenia = Ogloszenie.objects.filter(nazwa__icontains=nazwa, cena__gte=cenamin,
                                                   cena__lte=cenamax).order_by('-cena')
        else:
            ogloszenia = Ogloszenie.objects.filter(nazwa__icontains=nazwa, cena__gte=cenamin,
                                                   cena__lte=cenamax).order_by('-id')
    else:
        if sort == '1':
            ogloszenia = Ogloszenie.objects.filter(kategoria_id=kategoria, nazwa__icontains=nazwa, cena__gte=cenamin,
                                                   cena__lte=cenamax).order_by('cena')
        elif sort == '2':
            ogloszenia = Ogloszenie.objects.filter(kategoria_id=kategoria, nazwa__icontains=nazwa, cena__gte=cenamin,
                                                   cena__lte=cenamax).order_by('-cena')
        else:
            ogloszenia = Ogloszenie.objects.filter(kategoria_id=kategoria, nazwa__icontains=nazwa, cena__gte=cenamin,
                                                   cena__lte=cenamax).order_by('-id')
    paginator = Paginator(ogloszenia, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "kategorie": kategorie,
        "nazwa": nazwa,
        "kategoria": kategoria,
        "cenamin": cmin,
        "cenamax": cmax,
        "sort": sort,
        "page_obj": page_obj
    }
    return render(request, 'aplikacjaogloszeniowa/announcements.html', context)


def announcement_view(request, id):
    ogloszenie = get_object_or_404(Ogloszenie, pk=id)
    context = {
        'ogloszenie': ogloszenie
    }
    return render(request, 'aplikacjaogloszeniowa/announcement.html', context)


def user_view(request, id):
    uzytkownik = get_object_or_404(Uzytkownik, pk=id)
    ogloszenia = Ogloszenie.objects.filter(uzytkownik=uzytkownik).order_by('-id')
    context = {
        'uzytkownik': uzytkownik,
        'ogloszenia': ogloszenia
    }
    return render(request, 'aplikacjaogloszeniowa/user.html', context)


@login_required
def konwersacje_view(request):
    uzytkownik = request.user.uzytkownik
    wiadomosci = Wiadomosc.objects.filter(Q(nadawca=uzytkownik) | Q(adresat=uzytkownik)).order_by('-data')
    lista = []
    lista_id = []
    for wiadomosc in wiadomosci:
        if ((wiadomosc.nadawca_id, wiadomosc.adresat_id) not in lista) and (
                (wiadomosc.adresat_id, wiadomosc.nadawca_id) not in lista):
            lista.append((wiadomosc.nadawca_id, wiadomosc.adresat_id))
            lista_id.append(wiadomosc.id)
    wiadomosci = Wiadomosc.objects.filter(id__in=lista_id).order_by('-data')
    context = {
        'wiadomosci': wiadomosci
    }
    return render(request, 'aplikacjaogloszeniowa/wiadomosci.html', context)


@login_required
def konwersacja_view(request, id):
    rozmowca = get_object_or_404(Uzytkownik, id=id)
    uzytkownik = request.user.uzytkownik
    Wiadomosc.objects.filter(nadawca_id=id, adresat=uzytkownik, nowa=1).update(nowa=0)
    wiadomosci = Wiadomosc.objects.filter(
        (Q(nadawca=uzytkownik) & Q(adresat_id=id)) | (Q(adresat=uzytkownik) & Q(nadawca_id=id))).order_by('data')
    if request.method == 'POST':
        wiadomoscform = WiadomoscForm(request.POST)
        wiadomoscform.instance.nadawca = uzytkownik
        wiadomoscform.instance.adresat = rozmowca
        if wiadomoscform.is_valid():
            wiadomoscform.save()
            return redirect("/konwersacja/" + str(id))
    else:
        wiadomoscform = WiadomoscForm()
    context = {
        'wiadomosci': wiadomosci,
        'rozmowca': rozmowca,
        'wiadomoscform': wiadomoscform
    }
    return render(request, 'aplikacjaogloszeniowa/wiadomosc.html', context)
