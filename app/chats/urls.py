from django.urls import path
from chats.views import ContactsView


urlpatterns = [
    path('contacts/', ContactsView.as_view(), name=ContactsView.name),
]
