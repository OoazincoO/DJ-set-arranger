from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    sets = db.relationship("Set", backref="user", lazy=True)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=True)
    bpm = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    key = db.Column(db.String(32), nullable=True)
    duration_sec = db.Column(db.Integer, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Set(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 多对多关系
    set_tracks = db.relationship("SetTrack", backref="set", lazy=True, cascade="all, delete-orphan")

    def get_track_ids(self):
        """获取Set中所有track的ID列表（按order排序）"""
        return [st.track_id for st in sorted(self.set_tracks, key=lambda x: x.order)]

    def get_ordered_tracks(self):
        """获取Set中所有track对象（按order排序）"""
        return sorted(self.set_tracks, key=lambda x: x.order)


class SetTrack(db.Model):
    """Set和Track的多对多关联表"""
    __tablename__ = "set_tracks"

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey("sets.id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 关系
    track = db.relationship("Track", backref="set_tracks", lazy=True)
