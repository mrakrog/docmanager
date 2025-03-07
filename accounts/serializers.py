from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializador para el perfil de usuario."""
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'department', 'position', 'profile_picture', 'date_joined', 'last_updated']
        read_only_fields = ['date_joined', 'last_updated']

class UserSerializer(serializers.ModelSerializer):
    """Serializador para el usuario."""
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'is_active', 'profile']
        read_only_fields = ['id', 'is_staff', 'is_active']
    
    def create(self, validated_data):
        """Crear un nuevo usuario con contraseña encriptada."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Actualizar usuario y gestionar la contraseña si está presente."""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance 