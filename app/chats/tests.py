from urllib.parse import urljoin

from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.http import HttpResponse
from django.contrib import auth

from chats.models import Chat, Message
from chats.views import ContactsView


class TestChatsModels(TestCase):

    CONTACTS_URL = reverse(ContactsView.name)

    @classmethod
    def setUpClass(cls):
        # Create 4 users
        users = []
        for n in range(4):
            user = User(email=f'email{n}@email.com', username=f'username{n}')
            user.set_password('password')
            user.save()
            users.append(user)

        # Create 2 chats
        chats = []
        limit = 2
        offset = 0
        for n in range(2):
            chat = Chat.objects.create()
            chat.members.set(users[offset:offset + limit])
            chat.save()
            chats.append(chat)
            offset += 2

        # One message for every user
        messages = []
        for chat in chats:
            for i in range(chat.members.count()):
                message = Message(
                    author=chat.members.all()[i],
                    chat=chat,
                    content=f'Hello {i}!',
                )
                messages.append(message)

        Message.objects.bulk_create(messages)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_set_up(self):
        users = User.objects.all()
        chats = Chat.objects.all()

        self.assertEqual(chats[0].members.count(), 2)
        self.assertEqual(chats[1].members.count(), 2)
        self.assertEqual(chats[0].messages.count(), 2)
        self.assertEqual(chats[1].messages.count(), 2)
        self.assertEqual(chats[0].messages.all()[0].author.username,
                         users[0].username)
        self.assertEqual(chats[1].messages.all()[0].author.username,
                         users[2].username)

    def test_add_contact_unauthorized(self):
        response: HttpResponse = self.client.post(urljoin(self.CONTACTS_URL,
                                                          str(1)))
        self.assertEqual(response.status_code, 403)

    def test_add_contact_correct(self):
        self.client.login(username='username1', password='password')
        response: HttpResponse = self.client.post(urljoin(self.CONTACTS_URL,
                                                          str(1)))
        self.assertEqual(response.status_code, 201)
        user: User = auth.get_user(self.client)
        self.assertEqual(user.contacts.count(), 1)
