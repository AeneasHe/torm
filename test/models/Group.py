import wpath
from torm import Model
from torm import f


class Group(Model):
    __config__ = "mongo"

    group = f.EmailList()
    group_hash = f.Str()
    display_name = f.Str()

    update_at = f.Timestamp()
    create_at = f.Timestamp()


user_email = 'thhk06@163.com'
groups = Group.FindMany({"group": user_email})
print(groups)
