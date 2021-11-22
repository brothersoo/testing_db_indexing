import time

from index.models import IndexTest


def get_param_value(explained_str: str, param: str = 'cost') -> str:
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
        blocks_read, blocks_hit = cursor.fetchone()[5:7]
        print(f"blocks_read {action_seq} {scan_type} scan:", blocks_read)
        print()
        return blocks_read, blocks_hit

    def decorated(cursor, scan_type: str, query: str):
        pre_blocks_read, pre_blocks_hit = execute_pg_stat_database(cursor, scan_type, 'before')
        time.sleep(3)

        inner_func(cursor, scan_type, query)
        time.sleep(3)

        post_blocks_read, post_blocks_hit = execute_pg_stat_database(cursor, scan_type, 'after')
        time.sleep(3)

        return pre_blocks_read, post_blocks_read

    return decorated


@compare_between_mass_search_decorator
def execute_and_explain(cursor, scan_type: str, query: str):
    print(f"# === {scan_type.capitalize()} scan === #")

    IndexTest.objects.filter(a='key', b='go', c='her')
    cursor.execute(query)
    explained: str = cursor.fetchall()[0][0]
    cost: str = get_param_value(explained, 'cost')
    actual_time: str = get_param_value(explained, 'actual time')
    print(f"cost for {scan_type} scan: {cost}")
    print(f"actual time for {scan_type} scan: {actual_time}")
