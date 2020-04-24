import path
from torm.model import *
from torm.field import *


class Record(Model):
    __table__ = 'record'

    hash = Str()
    subject = Str()
    promoter = Str()
    attachments_num = Int()
    mail_id = Str()
    commits = List()
    group = Str()
    group_hash = Str()
    create_at = Str()
    update_at = Str()
    status = Str()
    tx_status = Str()
    recorder = Str()
    hashtags = Dict()


record = Record({"hash": '12', "subject": "test", "hashtags": {'a': 2}})
print(record)

# Record.InsertOne(record)


# hash = "0x123"
# record = Record.FindOne(hash)
# print(record.to_map())

# records = Record.FindMany()
# print(records)

# r = Record.UpdateOne(hash, {'subject': 'test5'})
# print(r)
