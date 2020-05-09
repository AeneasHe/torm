from torm.field.Field import Field
# 基础数据类型
from torm.field.Int import Int
from torm.field.Float import Float
from torm.field.Str import Str
from torm.field.Bool import Bool

# 语义化数据类型
from torm.field.Email import Email
from torm.field.Timestamp import Timestamp

# 复杂数据类型，只有mongodb支持
from torm.field.Dict import Dict
from torm.field.Map import Map

# 复杂列表数据类型，只有mongodb支持
from torm.field.List import List
from torm.field.EmailList import EmailList
from torm.field.DictList import DictList
