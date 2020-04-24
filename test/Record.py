import path
from torm.model import *
import torm.field as f
from torm.utl.Map import Map


class Record(Model):
    # __dbname__ = 'dd'  # 指定数据库名，默认采用env中的DB值作为数据库名
    __tablename__ = 'record'  # 指定表名，默认采用类名的小写作为表名

    hash = f.Str()
    subject = f.Str()
    promoter = f.Str()
    recorder = f.Email()

    attachments_num = f.Int()
    mail_id = f.Str()
    group_hash = f.Str()

    status = f.Str()
    tx_status = f.Str()

    commits = f.Dict()
    group = f.EmailList()
    hashtags = f.Map()

    create_at = f.Int()
    update_at = f.Int()


commits = {'user_id': 'some thing'}

hashtags = Map({'a': 2})
record = Record({
    "hash": '12',
    "recorder": "thhk06@163.com",
    "subject": "test",
    "hashtags": hashtags,
    "group": ["thhk06@163.com", "kai.he@taraxa.io"],
    "commits": commits
})

# print(record.pretty())

# print(record.group)

# Record.InsertOne(record)

# hash = "0x123"
# record = Record.FindOne(hash)
# print(record.to_map())#

records = Record.FindMany()
print(records)

# r = Record.UpdateOne(hash, {'subject': 'test5'})
# print(r)
