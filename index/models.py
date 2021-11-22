from faker import Faker

from django.db import models

fake = Faker()


class IndexTest(models.Model):
    gender = models.BooleanField()
    indexed_gender = models.BooleanField(null=True, default=None)

    name = models.CharField(max_length=50)
    indexed_name = models.CharField(max_length=50, null=True, default=None)

    clustered_id = models.BigIntegerField(null=True, default=None)
    nonclustered_id = models.BigIntegerField(null=True, default=None)
    nonindexed_id = models.BigIntegerField(null=True, default=None)

    zero_or_one = models.SmallIntegerField(null=True, default=None)
    indexed_zero_or_one = models.SmallIntegerField(null=True, default=None)

    a = models.CharField(max_length=50, null=True, default=None)
    b = models.CharField(max_length=50, null=True, default=None)
    c = models.CharField(max_length=50, null=True, default=None)

    objects = models.Manager()

    class Meta:
        db_table = 'it'
