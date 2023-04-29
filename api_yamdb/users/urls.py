from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignupView, TokenView, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', TokenView.as_view()),
    path('', include(router.urls)),
]
