from django.db import models

# Create your models here.


class BaseModel(models.Model):
    
    id = models.AutoField(primary_key=True)
    state = models.BooleanField("state", default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"
