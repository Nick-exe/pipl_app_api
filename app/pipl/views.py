from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .renderers import TagRenderer


from core.models import Tag, Pip, Note, Reminder
from pipl import serializers

class BasePiplAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """Base viewset for userowned pipl attributes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BasePiplAttrViewSet):
    """ Manage tags in the database"""
    renderer_classes = (TagRenderer,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class PipViewSet(viewsets.ModelViewSet):
    """ Manage the pips in the database"""
    queryset = Pip.objects.all()
    serializer_class = serializers.PipSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """ Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        """ Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PipDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class NoteViewSet(viewsets.ModelViewSet):
    """ Manage notes in the database """ 
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return reminder for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class ReminderViewSet(viewsets.ModelViewSet):
    """ Manage notes in the database """ 
    queryset = Reminder.objects.all()
    serializer_class = serializers.ReminderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return reminder for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)