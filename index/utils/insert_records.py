from django.db.models import F

from faker import Faker

from index.models import IndexTest

fake = Faker()


def make_index_test(n: int):
    bulk_list: list = []
    for _ in range(n):
        gender: bool = fake.pybool()
        name: str = fake.first_name()
        zero_or_one: int = fake.pyint(min_value=0, max_value=1)
        a = fake.word()
        b = fake.word()
        c = fake.word()
        bulk_list.append(IndexTest(
            gender=gender, indexed_gender=gender,
            name=name, indexed_name=name,
            zero_or_one=zero_or_one, indexed_zero_or_one=zero_or_one,
            a=a, b=b, c=c
        ))
    IndexTest.objects.bulk_create(bulk_list)


def sync_index_test_id():
    IndexTest.objects.all().update(clustered_id=F('id'), nonclustered_id=F('id'), nonindexed_id=F('id'))
