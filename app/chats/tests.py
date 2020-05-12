from django.test import TestCase
from django.contrib.auth.models import User
from chats.models import Chat, Message


class TestChatsModels(TestCase):

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
        self.assertEqual(chats[0].messages.all()[0].author.username, users[0].username)
        self.assertEqual(chats[1].messages.all()[0].author.username, users[2].username)
