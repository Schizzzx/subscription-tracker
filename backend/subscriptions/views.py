from datetime import date

from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Subscription, NotificationSettings, FriendRequest
from .serializers import (
    SubscriptionSerializer,
    NotificationSettingsSerializer,
    FriendRequestSerializer,
)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        
        serializer.save(user=self.request.user)


class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subs = Subscription.objects.filter(user=request.user, is_active=True)
        today = date.today()

        monthly_total = 0.0
        yearly_total = 0.0

        for s in subs:
            price = float(s.price)

            
            if s.has_trial and s.trial_end_date and s.trial_end_date >= today:
                continue

            if s.billing_period == 'monthly':
                monthly_total += price
                yearly_total += price * 12
            elif s.billing_period == 'yearly':
                yearly_total += price
                monthly_total += price / 12
            elif s.billing_period == 'weekly':
                yearly_total += price * 52
                monthly_total += price * 52 / 12

        data = {
            "monthly_total": round(monthly_total, 2),
            "yearly_total": round(yearly_total, 2),
            "count": subs.count(),
        }

        return Response(data)


class NotificationSettingsViewSet(viewsets.ModelViewSet):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
       
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        instance = NotificationSettings.objects.filter(user=request.user).first()

        if instance is not None:
            
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        return super().create(request, *args, **kwargs)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class CommonSubscriptionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        accepted = FriendRequest.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='accepted',
        )

        friend_users = [
            fr.to_user if fr.from_user == user else fr.from_user
            for fr in accepted
        ]

        results = []

        my_subs = Subscription.objects.filter(user=user, is_active=True)

        for friend in friend_users:
            f_subs = Subscription.objects.filter(user=friend, is_active=True)

            for s1 in my_subs:
                for s2 in f_subs:
                    if s1.name.strip().lower() == s2.name.strip().lower():
                        results.append({
                            "friend": friend.username,
                            "service": s1.name,
                            "you_pay": float(s1.price),
                            "friend_pays": float(s2.price),
                            "suggestion": "Consider using a shared or family plan to reduce costs.",
                        })

        return Response(results)
