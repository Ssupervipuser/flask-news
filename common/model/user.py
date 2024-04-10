# 模型
from app import db


class User(db.Model):
    """user basic ifno"""
    __tablename__ = 'user_basic'

    id = db.Column(db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String(11), doc='手机号')
    name = db.Column(db.String(20), doc='昵称')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    introduction = db.Column(db.String(50), doc='简介')
    article_count = db.Column(db.Integer, default=0, doc='作品数')
    floolowing_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='粉丝数')
    profile_photo = db.Column(db.String(130), doc='头像')

    def to_dict(self):

        """模型转字典，用于序列化处理"""
        return {

            'id': self.id,
            'name': self.name,
            'photo': self.profile_photo,
            #注意：redis不支持None类型但是支持空字符串
            'intro': self.introduction if self.introduction else "",
            'art_count': self.article_count,
            'follow_count': self.following_count,
            'fans_count': self.fans_count
        }
