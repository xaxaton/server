from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User, Department, Position


class HRAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HRAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["name"].disabled = True
            self.fields["surname"].disabled = True
            self.fields["middle_name"].disabled = True
            self.fields["email"].disabled = True
            self.fields["organization"].disabled = True
            self.fields["department"].queryset = Department.objects.filter(
                organization=instance.organization
            )
            self.fields["position"].queryset = Position.objects.filter(
                organization=instance.organization
            )

    class Meta:
        fields = (
            "email",
            "name",
            "surname",
            "middle_name",
            "organization",
            "department",
            "position",
        )

        model = User


class OrganizartionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizartionAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["organization"].disabled = True
            self.fields["department"].queryset = Department.objects.filter(
                organization=instance.organization
            )
            self.fields["position"].queryset = Position.objects.filter(
                organization=instance.organization
            )

    class Meta:
        fields = (
            "email",
            "name",
            "surname",
            "middle_name",
            "organization",
            "department",
            "position",
            "role",
        )
        model = User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "department", "position")

    def full_name(self, obj):
        return f"{obj.surname} {obj.name} {obj.middle_name}"

    full_name.short_description = "ФИО"

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context.update(
            {
                "show_save": True,
                "show_save_and_continue": True,
                "show_save_and_add_another": False,
                "show_delete": False,
            }
        )
        return super().render_change_form(
            request, context, add, change, form_url, obj
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 3:
            return qs
        else:
            return qs.filter(organization=request.user.organization)

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        if request.user.role == 1:
            return HRAdminForm
        if request.user.role == 2:
            return OrganizartionAdminForm
        return form

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        if request.user.role < 3:
            return False
        return True


admin.site.unregister(Group)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_count")

    def unit_count(self, obj):
        return User.objects.filter(position=obj).count()

    unit_count.short_description = "Кол-во сотрудников"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 3:
            return qs
        else:
            return qs.filter(organization=request.user.organization)


@admin.register(Department)
class DepartmentPosition(admin.ModelAdmin):
    list_display = ("name", "unit_count")

    def unit_count(self, obj):
        return User.objects.filter(department=obj).count()

    unit_count.short_description = "Кол-во сотрудников"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 3:
            return qs
        else:
            return qs.filter(organization=request.user.organization)
