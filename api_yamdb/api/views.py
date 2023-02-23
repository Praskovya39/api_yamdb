from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Title, Category, Genre
from api.serializers import (TitleSerializer, TitleReadSerializer, 
                                 CategorySerializer, GenreSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre')

    def get_serializer_class(self):
        if self.action == 'list' or 'retrive':
            return TitleSerializer
        return TitleReadSerializer


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin, mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer