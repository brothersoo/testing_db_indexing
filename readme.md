# Index Testing

인덱싱이 검색 성능에 얼마나 큰 영향을 끼치는지 확인해보는 작업입니다.

데이터베이스는 Postgresql을 사용했으며

1M개의 레코드로 확인하였습니다.

데이터 생성은 python faker를 사용하여 랜덤 값을 삽입했습니다.

Django는 간편한 데이터베이스 연결 및 간편한 모듈들을 위해서만 사용되었으며, 모든 작업은 CLI에서 실행됩니다.

### Guide for run server in shell

```
git clone https://github.com/brothersoo/testing_db_indexing.git
cd testing

(activate your virtual env)

pip install -r requirements.txt

(setup database environments and secret key in setting.py)

python manage.py shell

```

### Guide for inserting random records
```
>>> from index.utils.insert_records import *
>>> make_index_test(1_000_000)   # 생성할 레코드 수를 조절할 수 있습니다.
>>> sync_index_test_id()         # id와 동일한 값을 가지는 레코드들을 위해 실행합니다.
```

### Guide for multi column index testing
```
>>> from index.utils.multi_column_test import *
>>> with_or_without_multi_index()
```

#### Result

![with_or_without_multi_index()](./resources/images/with_or_without_multi_index().png)

multi index를 사용하기 전에는 18006개의 disk block을 scan한 반면에, multi index를 사용한 후에는 단 네개의 disk block을 scan했음을 확인할 수 있습니다.