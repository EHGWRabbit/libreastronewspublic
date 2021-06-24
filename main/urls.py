from django.urls import path 
from .views import index#главная
from .views import other_page#другие страницы
from .views import AstroLoginView#вход
from .views import profile#профиль
from .views import AstroLogoutView#выход
from .views import ChangeUserInfoView#изменение данных
from .views import AstroPasswordChangeView#смена пароля
from .views import RegisterUserView#регистрация
from .views import RegisterDoneView#сообщение о регистрации
from .views import user_activate#активация
from .views import DeleteUserView#удаление профиля 
#from .views import ResetPasswordView#сброс пароля
#from .views import ResetPasswordConfirmView#дтверждение сброса
#from .views import ResetPasswordCompleteView
#from .views import ResetPasswordDoneView
from .views import detail#детали новости
from .views import by_rubric#контроллер для рубрик
from django.conf.urls.static import static 
from astron import settings
from .views import profile_bb_detail#нконтроллер данных о новостях, загруженных пользователем
from .views import profile_bb_add#контроллер добавления новости
from .views import profile_bb_change#контроллер изменения новости
from .views import profile_bb_delete#контроллер удаления новости



app_name = 'main'

urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', AstroLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', AstroPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/change/<int:pk>/', profile_bb_change, name='profile_bb_change'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name='profile_bb_delete'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', AstroLoginView.as_view(), name='login'),
    #path('accounts/password/reset/', ResetPasswordView.as_view(), name='reset'),
    #path('accounts/password/reset/confirm/', ResetPasswordConfirmView.as_view(), name='reset_confirm'),
    #path('accounts/password/reset/done/', ResetPasswordDoneView.as_view(), name='reset_done'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]


