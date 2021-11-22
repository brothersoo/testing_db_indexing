import time

from django.db import connection
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


def get_param_value(explained_str: str, param: str = 'cost', **kwargs) -> str:
    result = []
    i = explained_str.index(param) + len(param) + 1
    while explained_str[i:i+2] != '..':
        result.append(explained_str[i])
        i += 1
    return ''.join(result)


def compare_between_mass_search_decorator(inner_func):

    def execute_pg_stat_database(cursor, scan_type: str, action_seq: str = 'before'):
        stat_query: str = "SELECT * FROM pg_stat_database WHERE datname='testing';"
        cursor.execute(stat_query)
        bulks_read, bulks_hit = cursor.fetchone()[5:7]
        print(f"bulks_read {action_seq} {scan_type} scan:", bulks_read)
        print()
        return bulks_read, bulks_hit

    def decorated(cursor, scan_type: str):
        pre_bulks_read, pre_bulks_hit = execute_pg_stat_database(cursor, scan_type, 'before')
        time.sleep(3)

        inner_func(cursor, scan_type)
        time.sleep(3)

        post_bulks_read, post_bulks_hit = execute_pg_stat_database(cursor, scan_type, 'after')
        time.sleep(3)

        return pre_bulks_read, post_bulks_read

    return decorated


@compare_between_mass_search_decorator
def execute_and_explain(cursor, scan_type: str):
    search_query: str = "EXPLAIN (analyze) SELECT * FROM it where a='key' and b='go' and c='her'"
    print(f"# === {scan_type.capitalize()} scan === #")

    IndexTest.objects.filter(a='key', b='go', c='her')
    cursor.execute(search_query)
    explained: str = cursor.fetchall()[0][0]
    cost: str = get_param_value(explained, 'cost')
    actual_time: str = get_param_value(explained, 'actual time')
    print(f"cost for {scan_type} scan: {cost}")
    print(f"actual time for {scan_type} scan: {actual_time}")


def with_or_without_index():
    print("====================================================================================")
    print("============================= WITH OR WITHOUT INDEX ================================\n\n\n")

    drop_index_query: str = "DROP INDEX IF EXISTS it_abc_idx;"
    create_index_query: str = "CREATE INDEX it_abc_idx ON it USING btree(a, b, c);"

    cursor = connection.cursor()
    cursor.execute(drop_index_query)

    bulks_read1, bulks_read2 = execute_and_explain(cursor, 'sequence')

    print('\n')

    # === Create index === #
    cursor.execute(create_index_query)

    bulks_read3, bulks_read4 = execute_and_explain(cursor, 'index')

    print("\n\n# === RESULT === #")
    print(f"bulks_read before indexing: {bulks_read2 - bulks_read1}")
    print(f"bulks_read after indexing: {bulks_read4 - bulks_read3}")
    print("====================================================================================")
