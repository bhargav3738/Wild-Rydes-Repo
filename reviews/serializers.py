# serializers.py

from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'flight_id', 'user_id', 'username', 'content', 'created_at']

    def get_username(self, obj):
        return obj.user.username if obj.user else "Anonymous"