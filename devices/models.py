from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    '''	
    Class to define a user's profile
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    profile_pic = models.ImageField(upload_to="profile-pic/", blank=True, default='/profile-pic/default-no-profile-pic.jpg')

    def __str__(self):

        return self.user.username

    @classmethod
    def get_profiles(cls):

        profiles = Profile.objects.all()

        return profiles

    @classmethod
    def get_other_profiles(cls,user_id):


        profiles = Profile.objects.all()

        other_profiles = []

        for profile in profiles:

            if profile.user.id != user_id:

                other_profiles.append(profile)

        return other_profiles


# Create Profile when creating a User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save Profile when saving a User
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

