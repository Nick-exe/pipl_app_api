from rest_framework import viewsets, mixins, status
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

    def _params_to_ints(self, qs):
        """convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Return objects for the current authenticated user only"""
        tags = self.request.query_params.get('tags')
        category = self.request.query_params.get('category')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if category:
            queryset = queryset.filter(category=category)
        return queryset.filter(user=self.request.user)


    def get_serializer_class(self):
        """ Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PipDetailSerializer
        elif self.action == 'upload_image':
            return serializers.PiplImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a pip"""
        pip = self.get_object()
        serializer = self.get_serializer(pip, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTPP_400_BAD_REQUEST) 


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