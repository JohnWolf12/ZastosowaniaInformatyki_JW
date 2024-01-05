from aplikacjaogloszeniowa.models import Wiadomosc


def liczbawiadomosci(request):
    if request.user.is_authenticated:
        uzytkownik = request.user.uzytkownik
        liczbawiadomosci = Wiadomosc.objects.filter(adresat=uzytkownik, nowa=True)
        liczbawiadomosci = liczbawiadomosci.values('nadawca').distinct().count()
    else:
        liczbawiadomosci = 0
    return {'liczbawiadomosci': liczbawiadomosci}