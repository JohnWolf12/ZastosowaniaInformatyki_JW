from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from aplikacjaogloszeniowa.models import Uzytkownik, Ogloszenie, Kategoria


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Nazwa użytkownika', widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light'
        }
    ))
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control bg-light'
        }
    ))
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control bg-light'
        }
    ))
    email = forms.EmailField(label='Adres e-mail', widget=forms.EmailInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light',
            'placeholder': 'example@example.com'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika', widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light'
        }
    ))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control bg-light'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(label='Adres e-mail', max_length=50, widget=forms.EmailInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light',
            'placeholder': 'example@example.com'
        }
    ))
    first_name = forms.CharField(label='Imię', max_length=50, required=False, widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light'
        }
    ))
    last_name = forms.CharField(label='Nazwisko', max_length=50, required=False, widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light'
        }
    ))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


def check_number(value):
    if not value.isdigit() or (len(value) != 0 and len(value) != 9):
        raise ValidationError('Numer telefonu musi się składać tylko z 9 cyfr')


class UpdateUzytkownikForm(forms.ModelForm):
    telefon = forms.CharField(validators=[check_number], label='Numer telefonu', max_length=9, required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'autocomplete': 'off',
                                      'class': 'form-control bg-light',
                                      'placeholder': '123123123'
                                  }
                              ))
    miejscowosc = forms.CharField(label='Miejscowość', max_length=50, required=False, widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light'
        }
    ))

    class Meta:
        model = Uzytkownik
        fields = ['telefon', 'miejscowosc']


def check_positive_number(value):
    if value < 0:
        raise ValidationError('Cena musi być liczbą dodatnią')


class AnnouncementForm(forms.ModelForm):
    nazwa = forms.CharField(label='Nazwa', max_length=100, widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'class': 'form-control bg-light',
        }
    ))
    cena = forms.DecimalField(validators=[check_positive_number], label='Cena', max_digits=9, decimal_places=2,
                              widget=forms.NumberInput(
                                  attrs={
                                      'autocomplete': 'off',
                                      'class': 'form-control bg-light'
                                  }
                              ))
    kategoria = forms.ModelChoiceField(label='Kategoria', queryset=Kategoria.objects.all(),
                                       empty_label='Wybierz kategorię', widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ))
    opis = forms.CharField(label='Opis', max_length=1000, required=False, widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-light'
        }
    ))

    class Meta:
        model = Ogloszenie
        fields = ['nazwa', 'cena', 'kategoria', 'opis']
