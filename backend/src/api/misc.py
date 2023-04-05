from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import (
    RecipeShortSerializer
)


def recipe_m2m_create_delete(request, pk, model, create_error, delete_error):
    recipe = get_object_or_404(Recipe, id=pk)
    user = request.user
    if request.method == 'POST':
        _, created = model.objects.get_or_create(
            user=user,
            recipe=recipe,
        )
        if not created:
            return Response(
                {'errors': create_error},
                status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        deleted, _ = model.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': delete_error},
                status.HTTP_400_BAD_REQUEST
            )
    return Response(status=status.HTTP_400_BAD_REQUEST)
