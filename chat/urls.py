from django.urls import path
from .views import CreateThreadView, DeleteThreadView

urlpatterns = [
    path('threads/create/', CreateThreadView.as_view(), name='thread-create'),
    path('threads/<uuid:pk>/delete/', DeleteThreadView.as_view(), name='thread-delete'),
]