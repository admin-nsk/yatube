from django.contrib import admin
from group.models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', "title", "slug", "description")
    search_fields = ("title",)
    empty_value_display = "-пусто-"


admin.site.register(Group, GroupAdmin)