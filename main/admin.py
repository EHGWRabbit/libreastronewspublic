from django.contrib import admin
import datetime
from .models import AstroUser
from .utilities import send_activation_note

def send_activation_notes(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_note(rec)
    modeladmin.message_user(request, 'Письма с требованиями активации отправлены')
send_activation_notes.short_description = 'Отправка писем с требованиями активации'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activates', 'Прошли'),
            ('threedays', 'Не прошли более 3-х дней'),
            ('week', 'Не прошли более недели'),
        )
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)

class AstroUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = (('username', 'email', 'first_name', 'last_name'),
                    ('send_messages', 'is_active', 'is_activated'),
                    ('is_staff', 'is_superuser'),
                    'groups', 'user_permissions',
                    ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notes,)


admin.site.register(AstroUser, AstroUserAdmin)