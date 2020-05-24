from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.decorators import action
from rest_framework.response import Response

from .utils import AuthorApiPermissionMixin
from .models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostEditSerializer
)

class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.AllowAny]
    paginate_by = 2
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

class PostReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    permission_classes=[permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer

class PostChangeViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, AuthorApiPermissionMixin])
    def update_post(self, request, pk=None):
        queryset = Post.objects.all()
        post = Post.objects.get(queryset, id=pk)
        serializer = PostEditSerializer(post)
        return Response(serializer.data)

class PostCreateViewSet(CreateAPIView):
    serializer_class = PostEditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostEditViewSet(UpdateAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostEditSerializer
    permission_classes = [AuthorApiPermissionMixin]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        post = Post.objects.filter(id=pk)
        return post

class PostDeleteViewSet(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostEditSerializer
    permission_classes = [AuthorApiPermissionMixin]