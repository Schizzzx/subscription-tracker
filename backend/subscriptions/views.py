from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubscriptionSerializer
from datetime import date

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class SummaryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        subs = Subscription.objects.all()

        monthly_total = 0
        yearly_total = 0

        for s in subs:
            if s.billing_period == 'monthly':
                monthly_total += float(s.price)
                yearly_total += float(s.price) * 12
            elif s.billing_period == 'yearly':
                yearly_total += float(s.price)
                monthly_total += float(s.price) / 12
            elif s.billing_period == 'weekly':
                # очень грубо: 4 недели = месяц
                monthly_total += float(s.price) * 4
                yearly_total += float(s.price) * 52

        data = {
            "monthly_total": round(monthly_total, 2),
            "yearly_total": round(yearly_total, 2),
            "count": subs.count(),
        }
        return Response(data)
