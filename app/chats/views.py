from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView


class ContactsView(APIView):

    name = 'contacts'

    def post(self, request: Request, id: str) -> Response:
        pass
