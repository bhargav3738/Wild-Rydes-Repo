from django.urls import path
from .views import UserDetailView, CurrentUserView,UserRegistrationView
from users.views import CustomTokenObtainPairView,login_view, register_view, home_view, logout_view,health_check
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    # path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('<uuid:uuid>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('login/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    
    #test views
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    
    path('logout/', logout_view, name='logout'),
    path('health', health_check, name='health'),
]
