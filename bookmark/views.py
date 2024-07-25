from django.http import HttpResponse
from rest_framework import generics, serializers, status

from rest_framework.response import Response
from core.models import Bookmark
from rest_framework.permissions import IsAuthenticated
from bookmark.serializers import BookmarkSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class ListBookmarkView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return the bookmarks associated with the authenticated user"""
        return self.queryset.filter(user=self.request.user)


class ListCreateBookmarkView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.request.POST._mutable = True
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DestroyBookmarkView(generics.DestroyAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Bookmark.objects.filter(id=self.kwargs['pk'])
        return queryset
