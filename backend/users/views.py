from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import Follow, User
from .permissions import AdminPermission
from .serializers import (FollowSerializer, FollowListSerializer,
                          RegistrationSerializer, TokenSerializer,
                          UserSerializer)
from .utils import send_email


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        send_email(email, default_token_generator.make_token(user))
        return Response(request.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения!'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['patch', 'get', 'post', 'delete']

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=serializer.instance.role)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)

    @action(detail=True, permission_classes=(IsAuthenticated,),
            methods=['post', 'delete'])
    def follow(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        follow_data = {
            'user': user.id,
            'author': author.id
        }
        if request.method == 'POST':
            serializer = FollowSerializer(author,
                                          data=follow_data,
                                          context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')
            author = serializer.validated_data.get('author')
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def follow_list(self, request):
        user = request.user
        following = user.following.all()
        pages = self.paginate_queryset(following)
        serializer = FollowListSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
