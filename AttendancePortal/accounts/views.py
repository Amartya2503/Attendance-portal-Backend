from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class LogoutApi(APIView):
    def post(self, request):
        try:
            refresh_token  = request.data.get('refresh')
            if(refresh_token == None):
                return Response({'status':403, 'error': "refresh : This field is required."})
            else:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'status':200, 'message': 'Logout Successfully'})
        except Exception as e:
            return Response({'status':403, 'message': 'Some error has occured', 'error': str(e)})