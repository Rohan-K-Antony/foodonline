from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile

@receiver(post_save,sender = User)    
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("username")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("user is updated")
        except:
            #created the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print("Userprofile doesnot exist and craeted one for the user")


@receiver(pre_save,sender =User)
def pre_save_test(sender,instance,**kwargs):
    print("{} is going to be created".format(instance.username))
