from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User
from .validators import validate_username
from api.serializers import RecipeReadSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def validate(self, data):
        username = User.objects.filter(username=data['username']).exists()
        email = User.objects.filter(email=data['email']).exists()
        if email and not username:
            raise serializers.ValidationError('400')
        if username and not email:
            raise serializers.ValidationError('400')
        return data


class UserSerializer(serializers.ModelSerializer):
    is_subscriped = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('id', 'password', 'last_login', 'is_superuser',
                   'is_staff', 'is_active', 'date_joined',
                   'groups', 'user_permissions')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(
            user=request.user.id,
            author=obj.id).exists() if request else False


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author')
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise serializers.ValidationError('Нельзя подписываться на себя')
        return data


class FollowListSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        queryset = obj.author.recipes.all()
        return RecipeReadSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
