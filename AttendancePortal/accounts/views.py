from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import User
from django.contrib.sites.models import Site
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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

class SendVerficationAPI(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        user = request.user
        token =  uuid4()
        user.email_token = token
        user.save()
        try:
            subject = 'Welcome to Attendance Managment System'
            message = f'Hi!\n{user.first_name} {user.last_name}, thank you for registering in Attendance Managment System.\nPlease Click here to verfy Your Account {Site.objects.get_current().domain}accounts/email-verification/{user.id}/{token}/\nThis is a Computer generated mail don\'t reply to this mail'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return Response({'status': 200,'message' : 'Please Check Your Mail, an Email verfication link has been provided'})
        except Exception as e:
            return Response({'status': 405, 'error': str(e) ,'message': 'Sorry Some error has occured, Please try again after sometime'})

class ValidateVerificationView(APIView):
    def get(self, request, id, token):
        try:
            user = User.objects.get(id = id)
            if(token == user.email_token):
                user.is_email_verified = True
                user.save()
                return HttpResponse('<h1>User is Verified Successfully</h1>')
            else:
                return HttpResponse('<h1>Token is not valid</h1>')
        except Exception as e:
            return HttpResponse('<h1>Sorry Some error has occured</h1>')

class PasswordResetAPI(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email = request.data.get('email'))
            subject = 'Password Reset Mail'
            uuid = uuid4()
            user.password_reset_token = uuid
            user.save()
            html_template = 'passwordresetmail.html'
            text_content = f'{Site.objects.get_current().domain}accounts/password-reset-redirect/{user.id}/{uuid}/'
            html_content = render_to_string(html_template, { 'context': text_content,'username': f'{user.first_name} {user.last_name}','logo': 'https://i.postimg.cc/C1CP58Wm/logo.png'})
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            # send_mail( subject, text_content, email_from, recipient_list )
            msg.send()
            return Response({'status': 200, 'message' : 'Please check your mail a password reset link has been provided'})
        except Exception as e:
            return Response({'status': 405, 'error': str(e) ,'message': 'Sorry Some error has occured, Please try again after sometime'})

class PasswordResetView(APIView):
    def get(self , request, id, token):
        user_obj = User.objects.get(id=id)
        if(token == user_obj.password_reset_token):
            return render(request, "passwordreset.html", {'id' : id, 'token' : token})
        else:
            return HttpResponse('<h1>Token is not valid</h1>')
    def post(self, request, id, token):
        password = request.POST['password']
        user_obj = User.objects.get(id=id)
        if(token == user_obj.password_reset_token):
            try:
                user_obj.set_password(password)
                user_obj.save()
                return HttpResponse('<h1>User\'s Password changed Successfully</h1>')
            except:
                return HttpResponse('<h1>Some error has occured</h1>')
        else:
            return HttpResponse('<h1>Token is not valid</h1>')