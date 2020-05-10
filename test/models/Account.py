import wpath
from torm import Model
from torm import f
import time


class Account(Model):
    __config__ = 'mysql'

    id = f.Int()
    user_id = f.Int()
    is_current = f.Bool()
    address = f.Str(42)
    private_key = f.Str(128)

    update_at = f.Timestamp()
    create_at = f.Timestamp()


privateKey = "0x7b2b3db28278e11df1648ba8c741e9d0d67c7794809124afbfbee6f1e505f5be"
address = "0xeCaA62E08a7760C34229D4B5B0FA37B89A264a23"
secretKey = "123456"
private_key = "U2FsdGVkX1/6EIiEKeTvbEkgFxseH0dbfafvMtlNGxdwq03PESAK6jmEUGsojEWp6Pkl0SWkrdG3zUbb29k+BlcSNDmAVoSm904mWo5oGmhQpk5MuQ/zxBafsEPZMLfr"


t = int(time.time())

account = Account(
    user_id=13,
    is_current=True,
    address=address,
    private_key=private_key,
    update_at=t,
    create_at=t)

print(account)

r = Account.InsertOne(account)
print(r)
