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


class PipSerializer(serializers.ModelSerializer):
    """Serializer for Pip objects"""

    class Meta:
        model = Pip
        fields = '__all__'
        read_only_fields = ('id',)

class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note objects"""

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('owner', 'timestamp', 'id')

class ReminderSerializer(serializers.ModelSerializer):
    """Serializer for Reminder objects"""

    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ('id')