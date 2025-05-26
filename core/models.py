from django.db import models

from apps.accounts.models import PoliceUser


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        PoliceUser,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user is not None:
            if not self.pk:
                self.created_by = user
            self.created_by = user
        super().save(*args, **kwargs)

    @property
    def get_police_names(self):
        return f"{self.created_by.first_name} {self.created_by.last_name}"
