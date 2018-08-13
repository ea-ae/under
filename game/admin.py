from django.contrib import admin
from .models import WarfareGame, WarfarePlayer, Cult, Member


class CultAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'money', 'reputation')

    def owner(obj):
        return obj.owner.user.username


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'cult', 'job')

    def cult(self, obj):
        return obj.owner

    def job(self, obj):
        job_id = obj.job_id
        if job_id == 0:
            return 'No job'
        elif job_id == 1:
            return 'Recruiting',
        elif job_id == 2:
            return 'Researching',
        elif job_id == 3:
            return 'Guarding'
        else:
            return 'Unknown'

admin.site.register(WarfareGame)
admin.site.register(WarfarePlayer)
admin.site.register(Cult, CultAdmin)
admin.site.register(Member, MemberAdmin)
