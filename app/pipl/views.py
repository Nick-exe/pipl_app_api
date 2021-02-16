from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .renderers import TagRenderer


from core.models import Tag, Pip
from pipl import serializers

class BasePiplAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for userowned piple attributes """
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
    

class PipViewSet(BasePiplAttrViewSet):
    """ Manage the pips in the database"""
    queryset = Pip.objects.all()
    serializer_class = serializers.PipSerializer
