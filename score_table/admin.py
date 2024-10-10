from django.contrib import admin
from .models import Post,Participant,FujitaRanking,Reservation

# Register your models here.


admin.site.register(Post)
admin.site.register(Participant)
admin.site.register(FujitaRanking)
admin.site.register(Reservation)