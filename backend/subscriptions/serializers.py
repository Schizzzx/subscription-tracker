from rest_framework import serializers
from .models import Subscription, NotificationSettings, FriendRequest


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        """
        Проверка на дубли подписок по (user, name) до удара об UniqueConstraint.
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        
        if not user or not user.is_authenticated:
            return attrs

        
        name = attrs.get('name') or getattr(self.instance, 'name', None)

        if not name:
            return attrs

        qs = Subscription.objects.filter(
            user=user,
            name__iexact=name.strip(),  # "Netflix" == "netflix"
        )

        
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({
                'name': 'You already have a subscription with this name.'
            })

        return attrs


class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = '__all__'
        read_only_fields = ['user']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['from_user']
