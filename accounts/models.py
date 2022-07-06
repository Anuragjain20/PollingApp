
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .managers import UserManager
from .threads import SendAccountActivationEmail , SendForgetPasswordEmail


import uuid







class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
 
    phone = models.IntegerField(null=True, blank=True)
    email_verification_token = models.CharField(max_length=200 , null=True, blank=True)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)

    number_of_question_allowed = models.IntegerField(default=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


class ForgetPassword(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email















'''  ALL SIGNALS HERE  '''



@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_verification_token = str(uuid.uuid4())
            instance.email_verification_token = email_verification_token
            instance.save()
            ''' EXCEUTING THREAD TO SEND EMAIL '''
            SendAccountActivationEmail(instance.email , email_verification_token).start()

    except Exception as e:
        print(e)
        
@receiver(post_save, sender=ForgetPassword)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            ''' EXCEUTING THREAD TO SEND EMAIL '''

            SendForgetPasswordEmail(instance.user.email , instance.forget_password_token).start()

    except Exception as e:
        print(e)