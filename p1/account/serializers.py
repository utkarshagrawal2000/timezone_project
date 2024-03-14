from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from geomapapi.utils.Google import Create_Service
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from rest_framework.response import Response
from rest_framework import status
from requests import HTTPError
from django.http import HttpResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'username','tc', 'mobile','password', 'password2','is_admin']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    a=1
    print(a)
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']
class UserLoginSerializer1(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ['username', 'password']
    extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }
class UserLoginSerializer2(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ['mobile', 'password']
    extra_kwargs = {
            'mobile': {
                'validators': [RegexValidator()],
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ['id', 'email', 'mobile','username','password','is_admin']
    extra_kwargs={
      'email':{'read_only':True},
      # 'mobile':{'read_only':True},
      # 'username':{'read_only':True},
    }

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

CLIENT_SECRET_FILE = 'client_secret_610653764729-60g0co55joj77d0dm92ktk939hqevfqk.apps.googleusercontent.com.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
# sender_email = 'narmadakshipramp@gmail.com'
# sender_password = 'mrzjckipbgqsjpqj'
# class SendPasswordResetEmailSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     fields = ['email']
#   def validate(self, attrs):
#     email = attrs.get('email')
#     print(email)
#     if User.objects.filter(email=email).exists():
#       user = User.objects.get(email = email)
#       uid = urlsafe_base64_encode(force_bytes(user.id))
#       print('Encoded UID', uid)
#       token = PasswordResetTokenGenerator().make_token(user)
#       print('Password Reset Token', token)
#       link = 'http://3.109.70.44/api/user/reset/'+uid+'/'+token
#       print('Password Reset Link', link)
#       # Send EMail
#       body = 'Click Following Link to Reset Your Password '+link
#       recipient_email = email
#       print(recipient_email ,'2423432')
#       server = smtplib.SMTP('smtp.gmail.com', 587)
#       server.starttls()
#       server.login(sender_email, sender_password)
#       msg = MIMEMultipart()
#       msg['From'] = sender_email
#       msg['To'] = recipient_email
#       msg['Subject'] = 'User Password Reset'
#       msg.attach(MIMEText(body, 'plain'))

#       text = msg.as_string()
#       server.sendmail(sender_email, recipient_email, text)
#       server.quit()
#       print("Email sent successfully.")
#       print("ok mail sent successfully")
#       return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
#     else:
#       raise serializers.ValidationError('You are not a Registered User')
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']
  def validate(self, attrs):
    # service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    email = attrs.get('email')
    print(email)
    if User.objects.filter(email=email).exists():
      try:
        user = User.objects.get(email = email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        print('Encoded UID', uid)
        token = PasswordResetTokenGenerator().make_token(user)
        print('Password Reset Token', token)
        link = 'http://3.109.70.44/api/user/reset/'+uid+'/'+token
        print('Password Reset Link', link)
        # Send EMail
        body = 'Click Following Link to Reset Your Password '+link

        recipient = email
        print(recipient,'2423432')
              # Create message

        msg = MIMEMultipart()
        msg['to'] = recipient
        msg['Subject'] = 'User Password Reset'
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        message = {'raw': base64.urlsafe_b64encode(text.encode()).decode()}
        try:
          message = service.users().messages().send(userId='me', body=message).execute()
          return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        except HTTPError as error:
          return HttpResponse(f'An error occurred: {error}')
        except Exception as e:
          print("An error occurred:", str(e))
      except:
        raise serializers.ValidationError('Check email api')
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  