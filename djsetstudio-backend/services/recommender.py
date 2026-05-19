"""推荐算法模块

提供基于BPM、风格、调性等维度的智能歌曲推荐功能。
"""

from extensions import db
from models import Track


def recommend_tracks(seed_track_ids, limit: int = 10):
    """
    基于种子歌曲推荐相似曲目

    推荐策略：
    1. 计算种子歌曲的平均BPM和最常见风格
    2. 优先推荐BPM接近、风格相同的歌曲
    3. 排除已在种子列表中的歌曲

    Args:
        seed_track_ids: 种子歌曲ID列表
        limit: 返回的推荐数量

    Returns:
        推荐歌曲列表（包含完整信息）
    """
    seed_set = set(int(x) for x in (seed_track_ids or []) if str(x).isdigit())

    # 如果没有种子歌曲，返回最新的歌曲
    if not seed_set:
        tracks = Track.query.order_by(Track.id.desc()).limit(limit).all()
        return _format_tracks(tracks)

    # 获取种子歌曲信息
    seed_tracks = Track.query.filter(Track.id.in_(seed_set)).all()

    # 计算种子歌曲的特征
    avg_bpm = _calculate_avg_bpm(seed_tracks)
    common_genres = _get_common_genres(seed_tracks)

    # 构建推荐查询
    query = Track.query.filter(~Track.id.in_(seed_set))

    # 如果有BPM信息，优先推荐BPM接近的歌曲
    if avg_bpm:
        # BPM容差范围（±10）
        bpm_tolerance = 10
        query = query.filter(
            db.and_(
                Track.bpm != None,
                Track.bpm >= avg_bpm - bpm_tolerance,
                Track.bpm <= avg_bpm + bpm_tolerance
            )
        )

    # 如果有风格信息，优先推荐相同风格的歌曲
    if common_genres:
        # 构建风格过滤条件
        genre_conditions = [Track.genre.ilike(f"%{genre}%") for genre in common_genres]
        query = query.filter(db.or_(*genre_conditions))

    # 获取推荐结果
    tracks = query.order_by(Track.id.desc()).limit(limit).all()

    # 如果结果不够，补充其他歌曲
    if len(tracks) < limit:
        remaining = limit - len(tracks)
        exclude_ids = seed_set.union({t.id for t in tracks})
        additional_tracks = Track.query.filter(
            ~Track.id.in_(exclude_ids)
        ).order_by(Track.id.desc()).limit(remaining).all()
        tracks.extend(additional_tracks)

    return _format_tracks(tracks)


def recommend_by_single_track(track_id: int, limit: int = 10):
    """
    基于单首歌曲推荐相似曲目

    Args:
        track_id: 歌曲ID
        limit: 返回的推荐数量

    Returns:
        推荐歌曲列表
    """
    return recommend_tracks([track_id], limit=limit)


def _calculate_avg_bpm(tracks):
    """计算歌曲列表的平均BPM"""
    bpms = [t.bpm for t in tracks if t.bpm is not None]
    if not bpms:
        return None
    return sum(bpms) / len(bpms)


def _get_common_genres(tracks):
    """获取歌曲列表中最常见的风格"""
    genres = {}
    for track in tracks:
        if track.genre:
            genre = track.genre.strip().lower()
            genres[genre] = genres.get(genre, 0) + 1

    if not genres:
        return []

    # 返回出现次数最多的风格（最多3个）
    sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
    return [genre for genre, count in sorted_genres[:3]]


def _format_tracks(tracks):
    """格式化歌曲列表为返回格式"""
    return [
        {
            "id": t.id,
            "title": t.title,
            "artist": t.artist,
            "bpm": t.bpm,
            "genre": t.genre,
            "key": t.key,
            "duration_sec": t.duration_sec,
            "cover_url": t.cover_url,
        }
        for t in tracks
    ]
