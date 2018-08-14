from django.contrib import admin
from .models import WarfareGame, WarfarePlayer, Cult, Member
from .consumers._members import job_from_id


class CultAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'money', 'reputation')

    def owner(obj):
        return obj.owner.user.username


class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ('name', 'cult', 'loyalty', 'specialization', 'job', 'supervisor')

    def supervisor(self, obj):
        supervisor_id = obj.supervisor_id
        if supervisor_id == -1:
            return 'You'
        return Member.objects.get(id=obj.supervisor_id).name

    def cult(self, obj):
        return obj.owner

    def job(self, obj):
        return job_from_id(obj.job_id)

admin.site.register(WarfareGame)
admin.site.register(WarfarePlayer)
admin.site.register(Cult, CultAdmin)
admin.site.register(Member, MemberAdmin)
