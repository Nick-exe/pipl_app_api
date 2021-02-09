from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""
    # location = models.PointField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'location')
        read_only_fields = ('id',)