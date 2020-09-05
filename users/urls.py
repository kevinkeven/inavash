from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('author/signup/', views.SignUpView.as_view(), name='signup'),
    path('author/<str:author>', views.author_info, name='author_info'),
    path('author/update/<int:pk>', views.UpdateUserView.as_view(), name='update'),
]