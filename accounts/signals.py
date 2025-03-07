from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crear un perfil de usuario automáticamente cuando se crea un usuario."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guardar el perfil cuando se actualiza el usuario."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # En caso de que el perfil no exista, crearlo
        UserProfile.objects.create(user=instance) 