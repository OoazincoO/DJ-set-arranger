from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from extensions import db
from models import Track
from services.recommender import recommend_by_single_track

tracks_bp = Blueprint("tracks", __name__)


@tracks_bp.get("/")
@jwt_required(optional=True)
def list_tracks():
    """获取所有歌曲列表"""
    tracks = Track.query.order_by(Track.id.desc()).all()
    return {
        "items": [
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
    }, 200


@tracks_bp.get("/search")
@jwt_required(optional=True)
def search_tracks():
    """搜索歌曲 - 支持关键词、艺术家、风格、BPM筛选"""
    keyword = request.args.get("keyword", "").strip()
    artist = request.args.get("artist", "").strip()
    genre = request.args.get("genre", "").strip()
    min_bpm = request.args.get("min_bpm", type=float)
    max_bpm = request.args.get("max_bpm", type=float)

    query = Track.query

    # 关键词搜索（歌名或艺术家）
    if keyword:
        query = query.filter(
            db.or_(
                Track.title.ilike(f"%{keyword}%"),
                Track.artist.ilike(f"%{keyword}%")
            )
        )

    # 艺术家筛选
    if artist:
        query = query.filter(Track.artist.ilike(f"%{artist}%"))

    # 风格筛选
    if genre:
        query = query.filter(Track.genre.ilike(f"%{genre}%"))

    # BPM范围筛选
    if min_bpm is not None:
        query = query.filter(Track.bpm >= min_bpm)
    if max_bpm is not None:
        query = query.filter(Track.bpm <= max_bpm)

    tracks = query.order_by(Track.id.desc()).all()

    return {
        "items": [
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
        ],
        "count": len(tracks)
    }, 200


@tracks_bp.post("/")
@jwt_required()
def create_track():
    """创建新歌曲"""
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return {"error": "title is required"}, 400

    track = Track(
        title=title,
        artist=(data.get("artist") or "").strip() or None,
        bpm=data.get("bpm"),
        genre=(data.get("genre") or "").strip() or None,
        key=(data.get("key") or "").strip() or None,
        duration_sec=data.get("duration_sec"),
        cover_url=(data.get("cover_url") or "").strip() or None,
    )
    db.session.add(track)
    db.session.commit()

    return {
        "id": track.id,
        "title": track.title,
        "artist": track.artist,
        "bpm": track.bpm,
        "genre": track.genre,
        "cover_url": track.cover_url,
    }, 201


@tracks_bp.get("/<int:track_id>")
@jwt_required(optional=True)
def get_track(track_id: int):
    """获取单个歌曲详情"""
    track = Track.query.get_or_404(track_id)
    return {
        "id": track.id,
        "title": track.title,
        "artist": track.artist,
        "bpm": track.bpm,
        "genre": track.genre,
        "key": track.key,
        "duration_sec": track.duration_sec,
        "cover_url": track.cover_url,
        "created_at": track.created_at.isoformat(),
    }, 200


@tracks_bp.put("/<int:track_id>")
@jwt_required()
def update_track(track_id: int):
    """更新歌曲信息"""
    track = Track.query.get_or_404(track_id)
    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = (data["title"] or "").strip()
        if not title:
            return {"error": "title cannot be empty"}, 400
        track.title = title

    if "artist" in data:
        track.artist = (data["artist"] or "").strip() or None

    if "bpm" in data:
        track.bpm = data["bpm"]

    if "genre" in data:
        track.genre = (data["genre"] or "").strip() or None

    if "key" in data:
        track.key = (data["key"] or "").strip() or None

    if "duration_sec" in data:
        track.duration_sec = data["duration_sec"]

    if "cover_url" in data:
        track.cover_url = (data["cover_url"] or "").strip() or None

    db.session.commit()

    return {
        "id": track.id,
        "title": track.title,
        "artist": track.artist,
        "bpm": track.bpm,
        "genre": track.genre,
        "cover_url": track.cover_url,
    }, 200


@tracks_bp.delete("/<int:track_id>")
@jwt_required()
def delete_track(track_id: int):
    """删除歌曲"""
    track = Track.query.get_or_404(track_id)
    db.session.delete(track)
    db.session.commit()
    return {}, 204


@tracks_bp.get("/<int:track_id>/recommend")
@jwt_required(optional=True)
def recommend_similar_tracks(track_id: int):
    """基于单首歌曲推荐相似曲目"""
    # 验证歌曲存在
    Track.query.get_or_404(track_id)

    limit = request.args.get("limit", default=10, type=int)
    recs = recommend_by_single_track(track_id, limit=limit)

    return {"items": recs, "count": len(recs)}, 200
