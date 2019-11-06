from rest_framework import serializers
from apiserver.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    vk_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.vk_id = validated_data.get('vk_id', instance.vk_id)
        instance.save()
        return instance
