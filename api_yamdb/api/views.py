from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from api.filters import FilterTitle
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users.permissions import (
    IsAdminOrReadOnlyPermission,
    IsValidOrReadonly,
)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = [
        IsValidOrReadonly,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [
        IsValidOrReadonly,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = FilterTitle

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadSerializer
        return TitleWriteSerializer
