from rest_framework import routers
from django.urls import path
from .views import SubscriptionViewSet, SummaryView

router = routers.DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
]

urlpatterns += router.urls
