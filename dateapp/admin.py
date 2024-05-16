from django.contrib import admin
from .models import User, Message, Um, Interests,Chatroom

# Register your models here.

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Um)
admin.site.register(Interests)
admin.site.register(Chatroom)

