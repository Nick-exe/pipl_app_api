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
    # add image to this serializer 

    class Meta:
        model = Pip
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note objects"""
    pip = serializers.StringRelatedField(
        many=False, read_only=True
    )
    pip_address = serializers.CharField(source='pip.address')


    class Meta:
        model = Note
        fields = ('id', 'user', 'pip', 'pip_address', 'pinned', 'note_title', 'note_content', 'timestamp')
        read_only_fields = ('owner', 'timestamp', 'id')
    

class ReminderSerializer(serializers.ModelSerializer):
    """Serializer for Reminder objects"""
    pip = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Pip.objects.all()
    )

    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ('id',)


class PipDetailSerializer(PipSerializer):
    """ Serialize a pip detail""" 
    tags = TagSerializer(many=True, read_only=True)
    pip_notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Pip
        fields = ('id', 'name', 'tags', 'pip_notes', 
        'category', 'date_met', 'address', 'location', 'phone')
        read_only_fields = ('id',)
