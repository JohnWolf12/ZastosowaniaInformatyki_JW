from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from aplikacjaogloszeniowa.models import Wiadomosc, Uzytkownik


class TestWiadomoscModel(TestCase):
    def test_create_wiadomosc(self):
        nadawcaTest = User.objects.create_user(username="nadawca")
        adresatTest = User.objects.create_user(username="adresat")
        nadawcaTest.save()
        adresatTest.save()
        saved_nadawca = Uzytkownik.objects.get(user=nadawcaTest)
        saved_adresat = Uzytkownik.objects.get(user=adresatTest)
        wiadomoscTest = Wiadomosc.objects.create(nadawca=saved_nadawca, adresat=saved_adresat,
                                                 tresc="test")
        wiadomoscTest.save()
        saved_wiadomosc = Wiadomosc.objects.get(id=wiadomoscTest.id)
        self.assertEquals(saved_wiadomosc.nadawca, wiadomoscTest.nadawca)
        self.assertEquals(saved_wiadomosc.adresat, wiadomoscTest.adresat)
        self.assertEquals(saved_wiadomosc.tresc, "test")
        self.assertAlmostEqual(saved_wiadomosc.data, timezone.now(), delta=timezone.timedelta(seconds=1))
        self.assertEquals(saved_wiadomosc.nowa, True)
