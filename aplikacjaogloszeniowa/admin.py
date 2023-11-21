from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Uzytkownik
from .models import Kategoria
from .models import Ogloszenie
from .models import Wiadomosc


class UzytkownikInline(admin.StackedInline):
    model = Uzytkownik
    can_delete = False
    verbose_name_plural = 'Uzytkownicy'


class UserAdmin(BaseUserAdmin):
    inlines = (UzytkownikInline,)


class OgloszenieAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'uzytkownik')


class WiadomoscAdmin(admin.ModelAdmin):
    list_display = ('id', 'nadawca', 'adresat')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Kategoria)
admin.site.register(Ogloszenie, OgloszenieAdmin)
admin.site.register(Wiadomosc, WiadomoscAdmin)
