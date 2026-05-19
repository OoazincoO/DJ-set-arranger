"""使用iTunes Search API更新歌曲封面"""
import requests
import time
import urllib.parse
from app import create_app
from extensions import db
from models import Track

app = create_app()

def get_itunes_artwork(artist, title):
    """从iTunes搜索获取专辑封面URL"""
    try:
        # 构建搜索查询
        query = f"{artist} {title}".replace("ft.", "").replace("feat.", "").replace("&", "")
        encoded_query = urllib.parse.quote(query)
        url = f"https://itunes.apple.com/search?term={encoded_query}&entity=song&limit=1"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('resultCount', 0) > 0:
                artwork_url = data['results'][0].get('artworkUrl100', '')
                # 将100x100替换为600x600获取高清封面
                if artwork_url:
                    return artwork_url.replace('100x100bb', '600x600bb')
    except Exception as e:
        pass
    return None

def update_track_covers():
    """更新所有歌曲的封面"""
    with app.app_context():
        # 获取所有使用placeholder封面的歌曲
        tracks = Track.query.filter(
            Track.cover_url.like('%placeholder%')
        ).all()

        print(f"Found {len(tracks)} tracks to update")

        updated = 0
        failed = 0

        for i, track in enumerate(tracks):
            if (i + 1) % 20 == 0 or i == 0:
                print(f"Processing {i+1}/{len(tracks)}...")

            artwork_url = get_itunes_artwork(track.artist, track.title)

            if artwork_url:
                track.cover_url = artwork_url
                updated += 1
            else:
                failed += 1

            # 避免请求过快被限制
            time.sleep(0.2)

            # 每50首保存一次
            if (i + 1) % 50 == 0:
                db.session.commit()
                print(f"Saved {i + 1} tracks...")

        # 最终保存
        db.session.commit()

        print(f"")
        print(f"Update complete!")
        print(f"Successfully updated: {updated}")
        print(f"Not found: {failed}")

if __name__ == "__main__":
    update_track_covers()
