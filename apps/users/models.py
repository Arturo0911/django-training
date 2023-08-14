from typing import Tuple
from django.db import models


from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
)

from apps.base.models import BaseModel
from simple_history.models import HistoricalRecords



class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name,
                     password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password,
                                 True, True, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    
    name = models.CharField("Names", max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    last_name = models.CharField("Last Names", max_length=255, blank=True, null=True)
    email = models.CharField("Email field", max_length=255, unique=True)
    role = models.CharField("position", max_length=255, blank=True, null=True)
    historical = HistoricalRecords()
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "last_name"]
    
    def natural_key(self) -> Tuple[str]:
        return (self.username)
    
    
    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"



class CustomRole(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name

class GroupRole(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.ForeignKey(CustomRole, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.group.name} - {self.role.name}"


"""
Now we're going to create some custom roles for simple samples
"""

# Create custom roles only if they don't already exist
admin_role, created_admin = CustomRole.objects.get_or_create(name="admin", description="Administrator")
user_role, created_user = CustomRole.objects.get_or_create(name="user", description="Regular User")

# Creating groups based on custom roles
admin_group, created_admin_group = Group.objects.get_or_create(name="admin_group")
user_group, created_user_group = Group.objects.get_or_create(name="user_group")

# Creating associations between groups and roles only if they don't already exist
if created_admin_group and created_admin:
    GroupRole.objects.create(group=admin_group, role=admin_role)

if created_user_group and created_user:
    GroupRole.objects.create(group=user_group, role=user_role)

# Creating users and assigning them to roles
admin_user = User.objects.create_user(username="admin", email="admin@admin.com", name="Arthur", last_name="Negreiros")
user_user = User.objects.create_user(username="user", email="user@user.com", name="Regular", last_name="User")

# Adding users to groups
admin_user.groups.add(admin_group)
user_user.groups.add(user_group)
