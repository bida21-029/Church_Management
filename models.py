from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

##########################
##########PROFILE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    CATEGORY_CHOICES = [
        ('Adult', 'Adult'),
        ('Teen', 'Teen'),
        ('Sunday School', 'Sunday School'),
        ('Visitor', 'Visitor'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add phone number field
    email = models.EmailField(blank=True, null=True)  # Add email field
    bio = bio = models.TextField(blank=True)
    

    def __str__(self):
       return f"{self.first_name},{self.last_name} "


   



##############################################
#######MEMBERS
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    CATEGORY_CHOICES = [
        ('Adult', 'Adult'),
        ('Teen', 'Teen'),
        ('Sunday School', 'Sunday School'),
        ('Visitor', 'Visitor'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add phone number field
    email = models.EmailField(blank=True, null=True)  # Add email field



    def __str__(self):
       return f"{self.first_name},{self.last_name} "


###SET PASSWORD FO MEMBER ADDED BY STAFF

    

##################################
###########EVENT

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title
#######################################
##############DONATION
class Donation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    donation_type_choices = [
        ('Cash', 'Cash'),
        ('Online', 'Online'),
        ('Tithes', 'Tithes'),
    ]
    donation_type = models.CharField(max_length=20, choices=donation_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member}, {self.donation_type}"

#################################
###########COMMUNICATION
class Message(models.Model):
    MESSAGE_TYPES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('letter', 'Letter'),
    )
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f"{self.message_type}, {self.recipient}"    


