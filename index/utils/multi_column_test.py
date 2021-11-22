from django.db import connection

from index.utils.core import execute_and_explain


def with_or_without_multi_index():
    print("====================================================================================")
    print("============================= WITH OR WITHOUT INDEX ================================\n\n\n")

    drop_index_query: str = "DROP INDEX IF EXISTS it_abc_idx;"
    create_index_query: str = "CREATE INDEX it_abc_idx ON it USING btree(a, b, c);"
    search_query: str = "EXPLAIN (analyze) SELECT * FROM it where a='key' and b='go' and c='her'"

    cursor = connection.cursor()
    cursor.execute(drop_index_query)

    blocks_read1, blocks_read2 = execute_and_explain(cursor, 'sequence', search_query)

    cursor.execute(create_index_query)

    blocks_read3, blocks_read4 = execute_and_explain(cursor, 'index', search_query)

    print("\n\n# === RESULT === #")
    print(f"blocks_read before indexing: {blocks_read2 - blocks_read1}")
    print(f"blocks_read after indexing: {blocks_read4 - blocks_read3}")
    print("====================================================================================")
