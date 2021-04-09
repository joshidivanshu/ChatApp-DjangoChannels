from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutViewClass.as_view(), name='logout'),  
    path('register/', views.RegisterView.as_view(), name='register'),
    path('addgroup/',views.AddView.as_view(), name="addgroup"),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('delete/<str:room_id>/<int:id>', views.delete_chat, name='delete'),
    path('history/<str:room_id>/', views.history, name='history'),
    path('<str:group_id>/', views.room, name='room'),
]