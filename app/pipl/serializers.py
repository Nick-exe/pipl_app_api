from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.models import Tag, Pip, Reminder, Note


class TagSerializer(GeoFeatureModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        geo_field = 'location'
        fields = ('id', 'name', 'location')
        read_only_fields = ('id',)
