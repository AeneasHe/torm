import wpath
wpath.add('/Users/aeneas/Github/python/torm')
from torm import Model
from torm import f


class UserProfile(Model):
    __config__ = 'mongo'

    id = f.Str()
    diplay_name = f.Str()
    user_id = f.Str()
    following_count = f.Int()
    fans_count = f.Int()
    likes_count = f.Int()


profile = {'diplay_name': 'Лиза лис', 'user_id': '380025332',
           'following_count': 1190, 'fans_count': 197, 'likes_count': 1780}

profile = UserProfile(profile)
print(profile)

UserProfile.InsertOne(profile)
