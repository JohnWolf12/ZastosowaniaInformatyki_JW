from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Uzytkownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(blank=True, max_length=9)
    miejscowosc = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "użytkownik"
        verbose_name_plural = "użytkownicy"


@receiver(post_save, sender=User)
def create_user_uzytkownik(sender, instance, created, **kwargs):
    if created:
        Uzytkownik.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_uzytkownik(sender, instance, **kwargs):
    instance.uzytkownik.save()


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "kategoria"
        verbose_name_plural = "kategorie"


class Ogloszenie(models.Model):
    nazwa = models.CharField(max_length=100)
    cena = models.DecimalField(max_digits=9, decimal_places=2)
    opis = models.TextField(blank=True, max_length=1000)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "ogłoszenie"
        verbose_name_plural = "ogłoszenia"

