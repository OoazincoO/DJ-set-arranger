"""数据库初始化脚本

用于创建测试数据，方便开发和演示。
"""

from app import create_app
from extensions import db
from models import User, Track, Set, SetTrack


def init_db():
    """初始化数据库并创建示例数据"""
    app = create_app()

    with app.app_context():
        print("正在创建数据库表...")
        db.create_all()
        print("✓ 数据库表创建成功")

        # 检查是否已有数据
        if User.query.first():
            print("! 数据库已包含数据，跳过初始化")
            return

        print("\n正在创建示例数据...")

        # 创建测试用户
        user1 = User(email="dj@example.com", username="dj_master")
        user1.set_password("password123")
        db.session.add(user1)

        user2 = User(email="music@example.com", username="music_lover")
        user2.set_password("password123")
        db.session.add(user2)

        db.session.commit()
        print(f"✓ 创建用户: {user1.username}, {user2.username}")

        # 创建示例歌曲
        tracks_data = [
            {
                "title": "Summer Vibes",
                "artist": "DJ Sunshine",
                "bpm": 128,
                "genre": "House",
                "key": "Am",
                "duration_sec": 240,
                "cover_url": "https://via.placeholder.com/300x300?text=Summer+Vibes"
            },
            {
                "title": "Night Drive",
                "artist": "Electronic Dreams",
                "bpm": 124,
                "genre": "Deep House",
                "key": "Gm",
                "duration_sec": 300,
                "cover_url": "https://via.placeholder.com/300x300?text=Night+Drive"
            },
            {
                "title": "Euphoria",
                "artist": "Trance Master",
                "bpm": 138,
                "genre": "Trance",
                "key": "Em",
                "duration_sec": 360,
                "cover_url": "https://via.placeholder.com/300x300?text=Euphoria"
            },
            {
                "title": "Bass Drop",
                "artist": "Heavy Beats",
                "bpm": 140,
                "genre": "Dubstep",
                "key": "Dm",
                "duration_sec": 220,
                "cover_url": "https://via.placeholder.com/300x300?text=Bass+Drop"
            },
            {
                "title": "Midnight Groove",
                "artist": "DJ Smooth",
                "bpm": 120,
                "genre": "Deep House",
                "key": "Fm",
                "duration_sec": 280,
                "cover_url": "https://via.placeholder.com/300x300?text=Midnight+Groove"
            },
            {
                "title": "Rising Sun",
                "artist": "Progressive Sounds",
                "bpm": 130,
                "genre": "Progressive House",
                "key": "Cm",
                "duration_sec": 320,
                "cover_url": "https://via.placeholder.com/300x300?text=Rising+Sun"
            },
            {
                "title": "Electric Dreams",
                "artist": "Synth Wave",
                "bpm": 126,
                "genre": "House",
                "key": "Dm",
                "duration_sec": 270,
                "cover_url": "https://via.placeholder.com/300x300?text=Electric+Dreams"
            },
            {
                "title": "Ocean Waves",
                "artist": "Chill Master",
                "bpm": 115,
                "genre": "Chillout",
                "key": "Am",
                "duration_sec": 340,
                "cover_url": "https://via.placeholder.com/300x300?text=Ocean+Waves"
            }
        ]

        tracks = []
        for track_data in tracks_data:
            track = Track(**track_data)
            db.session.add(track)
            tracks.append(track)

        db.session.commit()
        print(f"✓ 创建 {len(tracks)} 首示例歌曲")

        # 创建示例Set
        set1 = Set(
            name="Summer House Mix",
            description="夏日派对精选House音乐合集",
            cover_url="https://via.placeholder.com/400x400?text=Summer+House+Mix",
            user_id=user1.id
        )
        db.session.add(set1)
        db.session.flush()

        # 添加tracks到set1
        set1_tracks = [0, 1, 4, 6]  # indices
        for order, idx in enumerate(set1_tracks):
            st = SetTrack(set_id=set1.id, track_id=tracks[idx].id, order=order)
            db.session.add(st)

        set2 = Set(
            name="Progressive Journey",
            description="渐进式电子音乐之旅",
            cover_url="https://via.placeholder.com/400x400?text=Progressive+Journey",
            user_id=user1.id
        )
        db.session.add(set2)
        db.session.flush()

        # 添加tracks到set2
        set2_tracks = [2, 3, 5]
        for order, idx in enumerate(set2_tracks):
            st = SetTrack(set_id=set2.id, track_id=tracks[idx].id, order=order)
            db.session.add(st)

        db.session.commit()
        print(f"✓ 创建 2 个示例Set")

        print("\n✓ 数据库初始化完成！")
        print("\n测试账号：")
        print(f"  Email: {user1.email}")
        print(f"  Password: password123")
        print(f"\n  Email: {user2.email}")
        print(f"  Password: password123")


if __name__ == "__main__":
    init_db()
