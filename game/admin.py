from django.contrib import admin
from .models import WarfareGame, WarfarePlayer, Cult, Member


class CultAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'money', 'reputation')

    def owner(self, obj):
        return obj.owner.user.username


class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ('name', 'cult', 'loyalty', 'wage', 'specialization', 'job_name', 'id', 'supervisor_name')

    def supervisor_name(self, obj):
        supervisor = obj.supervisor
        if supervisor is None:
            return 'You'
        return supervisor.name

    def job_name(self, obj):
        return obj.job.title()

    def cult(self, obj):
        return obj.owner

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.object_id = object_id
        return self.changeform_view(request, object_id, form_url, extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'supervisor':
            try:
                # owner.id or is owner_id fine?
                kwargs['queryset'] = Member.objects.filter(owner__id=Member.objects.get(id=self.object_id).owner_id)
            except:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(WarfareGame)
admin.site.register(WarfarePlayer)
admin.site.register(Cult, CultAdmin)
admin.site.register(Member, MemberAdmin)
