from django.db import models


class Item(models.Model):
    code = models.CharField(max_length=20, unique=True)
    scheme_name = models.CharField(max_length=255, null=True, blank=True)
    name_russian = models.CharField(max_length=255, null=True, blank=True)
    name_chinese = models.CharField(max_length=255, null=True, blank=True)
    # quantity = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.code
