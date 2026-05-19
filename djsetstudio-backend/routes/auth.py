from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    """用户注册 - 使用email和密码"""
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    username = (data.get("username") or "").strip()

    if not email or not password:
        return {"error": "email and password are required"}, 400

    # 检查email是否已存在
    if User.query.filter_by(email=email).first():
        return {"error": "email already exists"}, 409

    # 如果没有提供username，使用email的前缀
    if not username:
        username = email.split("@")[0]

    # 检查username是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        # 如果username冲突，添加数字后缀
        base_username = username
        counter = 1
        while existing_user:
            username = f"{base_username}{counter}"
            existing_user = User.query.filter_by(username=username).first()
            counter += 1

    user = User(email=email, username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"id": user.id, "email": user.email, "username": user.username}, 201


@auth_bp.post("/login")
def login():
    """用户登录 - 使用email和密码"""
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return {"error": "email and password are required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"error": "invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }, 200


@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "created_at": user.created_at.isoformat()
    }, 200
