from django.urls import path
from .views import CreateThreadView, DeleteThreadView, ThreadListView, CreateMessageView, MessageListView

urlpatterns = [
    path('threads/create/', CreateThreadView.as_view(), name='thread-create'),
    path('threads/<uuid:pk>/delete/', DeleteThreadView.as_view(), name='thread-delete'),
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    path('threads/<uuid:thread_id>/messages/create/', CreateMessageView.as_view(), name='message-create'),
    path('threads/<uuid:thread_id>/messages/', MessageListView.as_view(), name='list-message'),
]