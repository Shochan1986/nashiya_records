from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    )
from rest_framework.response import Response
from django.contrib.auth.models import User
from farm.serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt import exceptions as jwt_exp


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('Eメールアドレスもしくはパスワードが正しくありません。')
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v    
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['name'] = user.first_name
        token['email'] = user.email
        token['isAdmin'] = user.is_staff
        token['isSuper'] = user.is_superuser

        return token


class MyTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])
        
        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        return res


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'このEメールアドレスは既に登録されています'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('ユーザーは削除されました')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
