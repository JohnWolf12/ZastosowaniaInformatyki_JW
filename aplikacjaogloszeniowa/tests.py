from time import sleep

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from aplikacjaogloszeniowa.forms import WiadomoscForm
from aplikacjaogloszeniowa.models import Wiadomosc, Uzytkownik

from django.test.utils import ignore_warnings

ignore_warnings(message="No directory at", module="whitenoise.base").enable()


class WiadomoscModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="nadawca")
        User.objects.create_user(username="adresat")
        nadawca = Uzytkownik.objects.get(user_id=1)
        adresat = Uzytkownik.objects.get(user_id=2)
        Wiadomosc.objects.create(nadawca=nadawca, adresat=adresat, tresc="test")

    def test_nadawca(self):
        wiadomosc = Wiadomosc.objects.get(id=1)
        nadawca = Uzytkownik.objects.get(user_id=1)
        self.assertEquals(wiadomosc.nadawca, nadawca)

    def test_adresat(self):
        wiadomosc = Wiadomosc.objects.get(id=1)
        adresat = Uzytkownik.objects.get(user_id=2)
        self.assertEquals(wiadomosc.adresat, adresat)

    def test_tresc(self):
        wiadomosc = Wiadomosc.objects.get(id=1)
        self.assertEquals(wiadomosc.tresc, "test")
        max_length = wiadomosc._meta.get_field('tresc').max_length
        self.assertEqual(max_length, 500)

    def test_data(self):
        wiadomosc = Wiadomosc.objects.get(id=1)
        self.assertAlmostEqual(wiadomosc.data, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_nowa(self):
        wiadomosc = Wiadomosc.objects.get(id=1)
        self.assertEquals(wiadomosc.nowa, True)


class WiadomoscFormTest(TestCase):
    def test_wiadomosc_form_tresc_required(self):
        tresc = ''
        form = WiadomoscForm(data={'tresc': tresc})
        self.assertFalse(form.is_valid())

    def test_wiadomosc_form_tresc_max_length(self):
        tresc = "a" * 600
        form = WiadomoscForm(data={'tresc': tresc})
        self.assertFalse(form.is_valid())

    def test_wiadomosc_form_tresc(self):
        tresc = "a" * 100
        form = WiadomoscForm(data={'tresc': tresc})
        self.assertTrue(form.is_valid())


class konwersacje_viewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='pass1')
        test_user2 = User.objects.create_user(username='testuser2', password='pass2')
        test_user3 = User.objects.create_user(username='testuser3', password='pass3')

        test_uzytkownik1 = Uzytkownik.objects.get(user=test_user1)
        test_uzytkownik2 = Uzytkownik.objects.get(user=test_user2)
        test_uzytkownik3 = Uzytkownik.objects.get(user=test_user3)

        Wiadomosc.objects.create(nadawca=test_uzytkownik1, adresat=test_uzytkownik2, tresc="test1")
        sleep(0.0001)
        Wiadomosc.objects.create(nadawca=test_uzytkownik1, adresat=test_uzytkownik3, tresc="test2")
        sleep(0.0001)
        Wiadomosc.objects.create(nadawca=test_uzytkownik3, adresat=test_uzytkownik1, tresc="test3")
        sleep(0.0001)
        Wiadomosc.objects.create(nadawca=test_uzytkownik2, adresat=test_uzytkownik3, tresc="test4")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/konwersacje/')
        self.assertRedirects(response, '/logowanie/?next=/konwersacje/')

    def test_logged_in(self):
        login = self.client.login(username='testuser1', password='pass1')
        response = self.client.get('/konwersacje/')
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aplikacjaogloszeniowa/wiadomosci.html')

    def test_lista_konwersacji(self):
        login = self.client.login(username='testuser1', password='pass1')
        response = self.client.get('/konwersacje/')
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('wiadomosci' in response.context)
        wiadomosci = response.context["wiadomosci"]
        self.assertEqual(len(wiadomosci), 2)
        wiadomosc1 = Wiadomosc.objects.get(tresc="test1")
        wiadomosc2 = Wiadomosc.objects.get(tresc="test3")
        self.assertIn(wiadomosc1, wiadomosci)
        self.assertIn(wiadomosc2, wiadomosci)


class konwersacja_viewTest(TestCase):
    @classmethod
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='pass1')
        test_user2 = User.objects.create_user(username='testuser2', password='pass2')
        test_user3 = User.objects.create_user(username='testuser3', password='pass3')

        test_uzytkownik1 = Uzytkownik.objects.get(user=test_user1)
        test_uzytkownik2 = Uzytkownik.objects.get(user=test_user2)
        self.test_uzytkownik3 = Uzytkownik.objects.get(user=test_user3)

        Wiadomosc.objects.create(nadawca=test_uzytkownik1, adresat=test_uzytkownik2, tresc="test1")
        sleep(0.0001)
        Wiadomosc.objects.create(nadawca=test_uzytkownik1, adresat=self.test_uzytkownik3, tresc="test2")
        sleep(0.0001)
        Wiadomosc.objects.create(nadawca=self.test_uzytkownik3, adresat=test_uzytkownik1, tresc="test3")
        sleep(0.0001)
        Wiadomosc.objects.create(nadawca=test_uzytkownik2, adresat=self.test_uzytkownik3, tresc="test4")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/logowanie/'))

    def test_logged_in(self):
        login = self.client.login(username='testuser1', password='pass1')
        response = self.client.get(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aplikacjaogloszeniowa/wiadomosc.html')

    def test_HTTP404_for_invalid_wiadomosc_if_logged_in(self):
        login = self.client.login(username='testuser1', password='pass1')
        response = self.client.get(reverse('konwersacja', kwargs={'id': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_liczba_nowych_wiadomosci_if_not_logged_in(self):
        response = self.client.get('/')
        self.assertTrue('liczbawiadomosci' in response.context)
        self.assertEqual(response.context['liczbawiadomosci'], 0)

    def test_liczba_nowych_wiadomosci_if_logged_in(self):
        login = self.client.login(username='testuser1', password='pass1')
        response = self.client.get('/konwersacje/')
        self.assertTrue('liczbawiadomosci' in response.context)
        self.assertEqual(response.context['liczbawiadomosci'], 1)
        response = self.client.get(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id}))
        self.assertEqual(response.context['liczbawiadomosci'], 0)

    def test_lista_wiadomosci(self):
        login = self.client.login(username='testuser1', password='pass1')
        response = self.client.get(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rozmowca' in response.context)
        self.assertEqual(response.context['rozmowca'], self.test_uzytkownik3)
        self.assertTrue('wiadomosci' in response.context)
        wiadomosci = response.context["wiadomosci"]
        self.assertEqual(len(wiadomosci), 2)
        wiadomosc1 = Wiadomosc.objects.get(tresc="test2")
        wiadomosc2 = Wiadomosc.objects.get(tresc="test3")
        self.assertIn(wiadomosc1, wiadomosci)
        self.assertIn(wiadomosc2, wiadomosci)

    def test_form_success(self):
        login = self.client.login(username='testuser1', password='pass1')
        tresc = "abc"
        response = self.client.post(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id, }), {'tresc': tresc})
        self.assertRedirects(response, reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id}))

    def test_form_tresc_required_fail(self):
        login = self.client.login(username='testuser1', password='pass1')
        tresc = ""
        response = self.client.post(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id, }), {'tresc': tresc})
        self.assertEqual(response.status_code, 200)

    def test_form_tresc_max_length_fail(self):
        login = self.client.login(username='testuser1', password='pass1')
        tresc = "a" * 600
        response = self.client.post(reverse('konwersacja', kwargs={'id': self.test_uzytkownik3.id, }), {'tresc': tresc})
        self.assertEqual(response.status_code, 200)
