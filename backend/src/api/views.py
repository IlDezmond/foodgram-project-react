from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow
from .filters import IngredientFilter, RecipeFilter
from .misc import recipe_m2m_create_delete
from .pagination import CustomPageNumberPagination
from .permissions import AuthorOrReadOnly
from .serializers import (
    IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer,
    TagSerializer, UserFollowSerializer
)

User = get_user_model()


class UserViewSet(DjUserViewSet):
    pagination_class = CustomPageNumberPagination

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        user = request.user
        if author == user:
            return Response(
                {'errors': 'Вы не можете подписаться на самого себя.'},
                status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            _, created = Follow.objects.get_or_create(
                user=user,
                author=author
            )
            if not created:
                return Response(
                    {'errors': 'Вы уже подписаны на этого пользователя'},
                    status.HTTP_400_BAD_REQUEST
                )
            serializer = UserFollowSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            deleted, _ = Follow.objects.filter(
                user=user,
                author=author
            ).delete()
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Вы не были подписаны на этого пользователя'},
                    status.HTTP_400_BAD_REQUEST
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = UserFollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags', 'author', 'ingredients')
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return recipe_m2m_create_delete(
            request,
            pk,
            Favorite,
            'Вы уже добавили этот рецепт в избранное',
            'Этот рецепт не был в избранном'
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return recipe_m2m_create_delete(
            request,
            pk,
            ShoppingCart,
            'Вы уже добавили этот рецепт в список покупок',
            'Этот рецепт не был в списке покупок'
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = (
            Ingredient.objects.filter(recipes__shopping_cart__user=user)
            .annotate(amount=Sum('recipe__amount')).
            values_list('name', 'amount', 'measurement_unit')
        )
        cart = 'Список покупок\n\n'
        for item in ingredients:
            cart += ' '.join(map(str, item)) + '\n'

        return FileResponse(
            cart,
            content_type='text/plain',
            as_attachment=True,
            status=status.HTTP_200_OK
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
