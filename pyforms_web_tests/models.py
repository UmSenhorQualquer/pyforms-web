from django.db import models


class Test(models.Model):

    name = models.CharField('Name', max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ['name__icontains']

