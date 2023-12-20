from django.contrib import admin

# Register your models here.
from .models import Member,Profile, Event, Donation, Message
# Register your models here.
admin.site.register(Member)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Donation)
admin.site.register(Message)
