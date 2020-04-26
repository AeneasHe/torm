# torm

mongodb style orm

## install
```
git clone https://github.com/cofepy/torm
cd torm
python setup.py install
```
or
```
pip install torm
```
## .env
add .env file to top folder
for example:

```
TORM_DB_TYPE   = mongo
TORM_DB       = test_default

TORM_HOST     = 127.0.0.1
TORM_PORT     = 27017

TORM_CHARSET  = utf8mb4
```

## useage

``` python

from torm.model import Model
from torm.field import Str,Int


class Record(Model):
    __tablename__ = 'record'

    hash = Str()
    subject = Str()
    promoter = Str()
    attachments_num = Int()
    mail_id = Str()

    commits = Str()
    group = Str()
    group_hash = Str()
    create_at = Str()
    update_at = Str()
    status = Str()
    tx_status = Str()
    recorder = Str()

# 创建
record = Record({"hash": "0x123", "subject": "test"})
Record.InsertOne(record)

# 单条查询
hash="0x123"
record = Record.FindOne(hash)
record = Record.FindOne(hash=hash)
record = Record.FindOne({'hash':hash})
print(record)
# 批量查询
records = Record.FindMany()
print(records)

```