from rest_framework import serializers

from core.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for the bookmarks object"""

    class Meta:
        model = Bookmark
        fields = ('pk', 'user', 'title', 'urls', 'price', 'img')
        extra_kwargs = {'user': {'write_only': True}}
