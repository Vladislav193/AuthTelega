from django.urls import path
from .views import login_page, telega_login, home


urlpatterns = [
    path('', login_page, name='login_page'),
    path('auth/telegram/', telega_login, name='telega_login'),
    path('home/', home, name='home')
]