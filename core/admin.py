from django.contrib import admin

# Register your models here.
from core.models import Profile
from datetime import date

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('decade born')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('80s', _('in the eighties')),
            ('90s', _('in the nineties')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '80s':
            return queryset.filter(
                last_login__gte=date(1980, 1, 1),
                last_login__lte=date(1989, 12, 31),
            )
        if self.value() == '90s':
            return queryset.filter(
                last_login__gte=date(1990, 1, 1),
                last_login__lte=date(1999, 12, 31),
            )


# admin.site.register(Profile)
@admin.display(empty_value='???')
def view_last_login_date(obj):
    return obj.last_login


@admin.register(Profile)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', view_last_login_date, 'date_joined',)
    list_filter = ('is_staff', 'is_active', 'is_superuser', DecadeBornListFilter, ('first_name', admin.EmptyFieldListFilter),)
    search_fields = ('first_name', 'last_name', 'email', 'username', )
    # fields = ('first_name', 'last_name')
