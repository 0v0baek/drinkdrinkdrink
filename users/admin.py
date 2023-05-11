from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "user_id",
            "nickname",
            "age",
            "profile_img",
            "fav_alcohol",
            "amo_alcohol",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "user_id",
            "nickname",
            "age",
            "profile_img",
            "fav_alcohol",
            "amo_alcohol",
            "is_active",
            "is_admin",
        ]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "email",
        "user_id",
        "nickname",
        "age",
        "profile_img",
        "fav_alcohol",
        "amo_alcohol",
        "is_admin",
    ]
    list_filter = ["is_admin"]
    fieldsets = [
        (
            None,
            {"fields": ("email", "user_id", "password", "fav_alcohol", "amo_alcohol")},
        ),
        ("Permissions", {"fields": ("is_admin",)}),
    ]

    #     fieldsets = [
    #     (None, {"fields": ["email", "password"]}),
    #     ("Personal info", {"fields": ["name"]}),
    #     ("Personal info", {"fields": ["gender"]}),
    #     ("Personal info", {"fields": ["age"]}),
    #     ("Personal info", {"fields": ["intro"]}),
    #     ("Permissions", {"fields": ["is_admin"]}),
    # ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["user_id"]
    ordering = ["user_id"]  # admin 페이지의 오름차순 정렬 기준
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
