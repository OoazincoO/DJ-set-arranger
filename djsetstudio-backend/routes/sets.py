from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import Set, SetTrack, Track
from services.recommender import recommend_tracks

sets_bp = Blueprint("sets", __name__)


@sets_bp.get("/")
@jwt_required()
def list_sets():
    """获取当前用户的所有Set列表"""
    user_id = int(get_jwt_identity())
    sets = Set.query.filter_by(user_id=user_id).order_by(Set.id.desc()).all()
    return {
        "items": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "cover_url": s.cover_url,
                "track_count": len(s.set_tracks),
                "track_ids": s.get_track_ids(),
                "created_at": s.created_at.isoformat(),
            }
            for s in sets
        ]
    }, 200


@sets_bp.post("/")
@jwt_required()
def create_set():
    """创建新的Set"""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return {"error": "name is required"}, 400

    # 创建Set
    s = Set(
        name=name,
        description=(data.get("description") or "").strip() or None,
        cover_url=(data.get("cover_url") or "").strip() or None,
        user_id=user_id
    )
    db.session.add(s)
    db.session.flush()  # 获取set的id

    # 添加tracks
    track_ids = data.get("track_ids") or []
    if isinstance(track_ids, list):
        for order, track_id in enumerate(track_ids):
            # 验证track是否存在
            track = Track.query.get(track_id)
            if track:
                set_track = SetTrack(set_id=s.id, track_id=track_id, order=order)
                db.session.add(set_track)

    db.session.commit()
    return {
        "id": s.id,
        "name": s.name,
        "description": s.description,
        "cover_url": s.cover_url,
        "track_ids": s.get_track_ids()
    }, 201


@sets_bp.get("/<int:set_id>")
@jwt_required()
def get_set(set_id: int):
    """获取Set详情，包含完整的track信息"""
    user_id = int(get_jwt_identity())
    s = Set.query.filter_by(id=set_id, user_id=user_id).first_or_404()

    # 获取所有tracks的完整信息
    tracks_info = []
    for st in s.get_ordered_tracks():
        if st.track:
            tracks_info.append({
                "id": st.track.id,
                "title": st.track.title,
                "artist": st.track.artist,
                "bpm": st.track.bpm,
                "genre": st.track.genre,
                "key": st.track.key,
                "duration_sec": st.track.duration_sec,
                "cover_url": st.track.cover_url,
                "order": st.order
            })

    return {
        "id": s.id,
        "name": s.name,
        "description": s.description,
        "cover_url": s.cover_url,
        "track_ids": s.get_track_ids(),
        "tracks": tracks_info,
        "created_at": s.created_at.isoformat(),
    }, 200


@sets_bp.put("/<int:set_id>")
@jwt_required()
def update_set(set_id: int):
    """更新Set信息（包括名称、描述、封面和tracks）"""
    user_id = int(get_jwt_identity())
    s = Set.query.filter_by(id=set_id, user_id=user_id).first_or_404()

    data = request.get_json(silent=True) or {}

    # 更新基本信息
    if "name" in data:
        name = (data["name"] or "").strip()
        if not name:
            return {"error": "name cannot be empty"}, 400
        s.name = name

    if "description" in data:
        s.description = (data["description"] or "").strip() or None

    if "cover_url" in data:
        s.cover_url = (data["cover_url"] or "").strip() or None

    # 更新tracks（如果提供）
    if "track_ids" in data:
        track_ids = data["track_ids"]
        if isinstance(track_ids, list):
            # 删除旧的关联
            SetTrack.query.filter_by(set_id=s.id).delete()

            # 添加新的关联
            for order, track_id in enumerate(track_ids):
                track = Track.query.get(track_id)
                if track:
                    set_track = SetTrack(set_id=s.id, track_id=track_id, order=order)
                    db.session.add(set_track)

    db.session.commit()

    return {
        "id": s.id,
        "name": s.name,
        "description": s.description,
        "cover_url": s.cover_url,
        "track_ids": s.get_track_ids()
    }, 200


@sets_bp.delete("/<int:set_id>")
@jwt_required()
def delete_set(set_id: int):
    """删除Set"""
    user_id = int(get_jwt_identity())
    s = Set.query.filter_by(id=set_id, user_id=user_id).first_or_404()

    db.session.delete(s)
    db.session.commit()
    return {}, 204


@sets_bp.post("/<int:set_id>/recommend")
@jwt_required()
def recommend_for_set(set_id: int):
    """为Set推荐相似歌曲"""
    user_id = int(get_jwt_identity())
    s = Set.query.filter_by(id=set_id, user_id=user_id).first_or_404()

    data = request.get_json(silent=True) or {}
    limit = int(data.get("limit") or 10)

    recs = recommend_tracks(seed_track_ids=s.get_track_ids(), limit=limit)
    return {"items": recs}, 200


@sets_bp.get("/<int:set_id>/tracks")
@jwt_required()
def get_set_tracks(set_id: int):
    """获取Set中的所有tracks（带顺序）"""
    user_id = int(get_jwt_identity())
    s = Set.query.filter_by(id=set_id, user_id=user_id).first_or_404()

    tracks_info = []
    for st in s.get_ordered_tracks():
        if st.track:
            tracks_info.append({
                "id": st.track.id,
                "title": st.track.title,
                "artist": st.track.artist,
                "bpm": st.track.bpm,
                "genre": st.track.genre,
                "key": st.track.key,
                "cover_url": st.track.cover_url,
                "order": st.order
            })

    return {"items": tracks_info}, 200
