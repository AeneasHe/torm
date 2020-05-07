# Torm

mongodb style orm.

mongodb,mysql are supported. 

## Install
```
git clone https://github.com/cofepy/torm
cd torm
python setup.py install
```
or
```
pip install torm
```
## Env file
add .env file to top folder or copy one file in envs to top folder.

if database has auth, set TORM_AUTH = on/off (default off).

for example:
```
TORM_DB_TYPE   = mongo
TORM_DB       = test_default

TORM_HOST     = 127.0.0.1
TORM_PORT     = 27017

TORM_CHARSET  = utf8mb4

TORM_AUTH     = on
TORM_USER     = root
TORM_PASSWORD = xxx
```

## Useage

``` python

from torm.model import Model
from torm.field import Str,Int


class Record(Model):
    # config file is ".env.mongo"; if not given, default config file is ".env".
    __configname__ = 'mongo'  
   
    # database type; if not given, will use db defined in config file
    # if no config file, torm will use "mongo" as default.
    __dbtype__ = 'mongo' 

    # database name: if not given, will use db defined in config file
    # if no config file, torm  will use "test" as default.
    __dbname__ = 'test'

    # table name: if not given, torm  will use the snake name of the model class name as default
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