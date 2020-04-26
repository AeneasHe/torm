from torm import Model
from torm import f
from torm.utl.Map import Map


class Record(Model):
    __config__ = "mongo"

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


def test_insert():
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


def test_find():
    #hash = "0x123"
    #record = Record.FindOne(hash)
    record = Record.FindOne()
    print(record.to_map())


def test_find_maney():
    records = Record.FindMany()
    print(records)


def test_update_one():
    r = Record.UpdateOne(hash, {'subject': 'test5'})
    print(r)


test_find()
