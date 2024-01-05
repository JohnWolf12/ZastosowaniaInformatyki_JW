from django.contrib.auth.views import LoginView
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('rejestracja/', views.register_view, name='rejestracja'),
    path('logowanie/',
         LoginView.as_view(template_name='aplikacjaogloszeniowa/login.html', authentication_form=LoginForm,
                           next_page='profil'), name='logowanie'),
    path('wylogowanie/', views.logout_view, name='wylogowanie'),
    path('profil/', views.profile_view, name='profil'),
    path('profil/edycja/', views.profileEdit_view, name='edycjaProfilu'),
    path('profil/dodanieogloszenia/', views.addAnnouncement_view, name="dodanieOgloszenia"),
    path('profil/edycjaogloszenia/<int:id>', views.editAnnouncement_view, name="edycjaOgloszenia"),
    path('profil/usuniecieogloszenia/<int:id>', views.deleteAnnouncement_view, name="usuniecieOgloszenia"),
    path('ogloszenia/', views.announcements_view, name="ogloszenia"),
    path('ogloszenie/<int:id>', views.announcement_view, name="ogloszenie"),
    path('uzytkownik/<int:id>', views.user_view, name="uzytkownik"),
    path('konwersacje/', views.konwersacje_view, name='konwersacje'),
    path('konwersacja/<int:id>', views.konwersacja_view, name='konwersacja'),
]
