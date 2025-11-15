from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SubscriptionViewSet,
    SummaryView,
    NotificationSettingsViewSet,
    FriendRequestViewSet,
    CommonSubscriptionsView,
)

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'notification-settings', NotificationSettingsViewSet, basename='notificationsettings')
router.register(r'friends', FriendRequestViewSet, basename='friendrequest')

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
    path('common/', CommonSubscriptionsView.as_view(), name='common-subscriptions'),
]

urlpatterns += router.urls
