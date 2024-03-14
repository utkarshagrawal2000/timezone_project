from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from account.serializers import UserLoginSerializer1,UserLoginSerializer2
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User
from rest_framework.decorators import authentication_classes, permission_classes


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
@authentication_classes([])  # No authentication required
@permission_classes([])  
class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    print(request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if request.data.get('is_admin')=='admin':
      print('admin creation')
      user1 = serializer.save()
      y=user1.is_admin = '2'
      user = user1.save()
      return Response({ 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    elif request.data.get('is_admin')=='user':
      print('user creation')
      user1 = serializer.save()
      y=user1.is_admin = '3'
      user = user1.save()
      return Response({ 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    print ('user creation')
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    
      
       
      
@authentication_classes([])  # No authentication required
@permission_classes([])  
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    x=request.data
    email=x['email'] 
    password=x['password']
    user = authenticate(username=email, password=password)
    if user is not None:
      if user.is_active:
        user1 = user.is_admin
        token = get_tokens_for_user(user)
        token["privilege"]=str(user1)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors': {'non_field_errors': ['User is not active']}}, status=status.HTTP_404_NOT_FOUND)
    else:
      return Response({'errors':{'non_field_errors':['Email/Username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    
@authentication_classes([])  # No authentication required
@permission_classes([])  
class UserLogin2View(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    x=request.data
    mobile=x['mobile'] 
    password=x['password']
    user = authenticate(username=mobile, password=password)
    request.session['signin'] = mobile   
    if user is not None:
      user1 = user.is_admin
      token = get_tokens_for_user(user)
      token["privilege"]=str(user1)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Mobile or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    current_user = request.user
    user_data = current_user.id
    print(user_data)
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class userdisableView(APIView):
  
  def put(self, request, format=None):
        try:
          id=request.data.get('id')
          task=request.data.get('task')
          obj=User.objects.get(id=id)
          if task == 'Disable':
            obj.is_active=False
            obj.save()
            return Response({'msg':'User is disabled'}, status=status.HTTP_200_OK) 
          else:
            obj.is_active=True
            obj.save()
            return Response({'msg':'User is Enabled'}, status=status.HTTP_200_OK) 
        except Exception as e:   
          return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)
      
      
      
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

@authentication_classes([])  # No authentication required
@permission_classes([]) 
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

@authentication_classes([])  # No authentication required
@permission_classes([]) 
class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


