from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class TopApps(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    score = models.FloatField(default=0, null=True, blank=True)
    icon = models.URLField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    webpage = models.URLField(default='', null=True, blank=True)

    class Meta:
        verbose_name = _("Top Application")
        verbose_name_plural = _("Top Applications")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name