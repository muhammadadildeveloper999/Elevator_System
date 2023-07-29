# elevators/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register the viewsets with it.
router = DefaultRouter()
router.register(r'elevators', ElevatorViewSet, basename='elevators')
router.register(r'user-requests', UserRequestViewSet, basename='user-requests')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/initialize_elevator_system/', ElevatorViewSet.as_view({'post': 'initialize_elevator_system'}), name='initialize-elevator-system'),
    path('api/<int:pk>/next_destination/', ElevatorViewSet.as_view({'get': 'next_destination'}), name='next-destination'),
    path('api/make_request/', UserRequestViewSet.as_view({'post': 'make_request'}), name='make_request'),
    path('api/<int:pk>/mark_not_working/', UserRequestViewSet.as_view({'get': 'mark_not_working'}), name='mark_not_working'),
    path('api/<int:pk>/open_door/', UserRequestViewSet.as_view({'get': 'open_door'}), name='open_door'),
    path('api/<int:pk>/close_door/', UserRequestViewSet.as_view({'get': 'close_door'}), name='close_door'),


]

