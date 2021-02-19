from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pipl import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('pips', views.PipViewSet)
router.register('notes', views.NoteViewSet)
router.register('reminders', views.ReminderViewSet)

app_name = 'pipl'

urlpatterns = [
    path('', include(router.urls)),
]