'''
Created on Jun 25, 2023

@author: nguye
'''
from accounts.models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile is created for User:", instance.username)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("User profile is updated for User:", instance.username)
        except UserProfile.DoesNotExist:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print("User profile is created for User:", instance.username)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, "This user is being saved")

# post_save.connect(post_save_create_profile_receiver, sender=User)
