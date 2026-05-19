"""添加更多歌曲到数据库"""
from app import create_app
from extensions import db
from models import Track

app = create_app()

# 更多歌曲数据 - 涵盖各种电子音乐风格
new_tracks = [
    # House
    {"title": "Sunset Boulevard", "artist": "Martin Garrix", "bpm": 128, "genre": "House", "key": "Am", "duration_sec": 210, "cover_url": "https://via.placeholder.com/300x300/FF6B6B/fff?text=Sunset+Boulevard"},
    {"title": "Feel The Beat", "artist": "David Guetta", "bpm": 126, "genre": "House", "key": "Fm", "duration_sec": 195, "cover_url": "https://via.placeholder.com/300x300/4ECDC4/fff?text=Feel+The+Beat"},
    {"title": "Paradise", "artist": "Tiesto", "bpm": 130, "genre": "House", "key": "Gm", "duration_sec": 225, "cover_url": "https://via.placeholder.com/300x300/45B7D1/fff?text=Paradise"},
    {"title": "One More Time", "artist": "Daft Punk", "bpm": 122, "genre": "House", "key": "Cm", "duration_sec": 320, "cover_url": "https://via.placeholder.com/300x300/96CEB4/fff?text=One+More+Time"},
    {"title": "Around The World", "artist": "Daft Punk", "bpm": 121, "genre": "House", "key": "Am", "duration_sec": 420, "cover_url": "https://via.placeholder.com/300x300/FFD93D/000?text=Around+The+World"},

    # Tech House
    {"title": "Losing It", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Dm", "duration_sec": 285, "cover_url": "https://via.placeholder.com/300x300/FFEAA7/000?text=Losing+It"},
    {"title": "Cola", "artist": "CamelPhat", "bpm": 124, "genre": "Tech House", "key": "Am", "duration_sec": 340, "cover_url": "https://via.placeholder.com/300x300/DDA0DD/fff?text=Cola"},
    {"title": "Move Your Body", "artist": "Chris Lake", "bpm": 125, "genre": "Tech House", "key": "Gm", "duration_sec": 270, "cover_url": "https://via.placeholder.com/300x300/98D8C8/fff?text=Move+Your+Body"},
    {"title": "The Underground", "artist": "Green Velvet", "bpm": 128, "genre": "Tech House", "key": "Em", "duration_sec": 310, "cover_url": "https://via.placeholder.com/300x300/2C3E50/fff?text=The+Underground"},
    {"title": "Make Me Feel", "artist": "Claptone", "bpm": 123, "genre": "Tech House", "key": "Fm", "duration_sec": 295, "cover_url": "https://via.placeholder.com/300x300/6C3483/fff?text=Make+Me+Feel"},

    # Deep House
    {"title": "Promises", "artist": "Tchami", "bpm": 120, "genre": "Deep House", "key": "Fm", "duration_sec": 295, "cover_url": "https://via.placeholder.com/300x300/9B59B6/fff?text=Promises"},
    {"title": "Show Me Love", "artist": "Sam Feldt", "bpm": 118, "genre": "Deep House", "key": "Am", "duration_sec": 260, "cover_url": "https://via.placeholder.com/300x300/3498DB/fff?text=Show+Me+Love"},
    {"title": "Latch", "artist": "Disclosure", "bpm": 122, "genre": "Deep House", "key": "Gm", "duration_sec": 275, "cover_url": "https://via.placeholder.com/300x300/E74C3C/fff?text=Latch"},
    {"title": "Together", "artist": "Bob Sinclar", "bpm": 116, "genre": "Deep House", "key": "Dm", "duration_sec": 290, "cover_url": "https://via.placeholder.com/300x300/1ABC9C/fff?text=Together"},
    {"title": "White Noise", "artist": "Disclosure", "bpm": 118, "genre": "Deep House", "key": "Em", "duration_sec": 310, "cover_url": "https://via.placeholder.com/300x300/2ECC71/fff?text=White+Noise"},

    # Progressive House
    {"title": "Strobe", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 600, "cover_url": "https://via.placeholder.com/300x300/8E44AD/fff?text=Strobe"},
    {"title": "Opus", "artist": "Eric Prydz", "bpm": 126, "genre": "Progressive House", "key": "Fm", "duration_sec": 540, "cover_url": "https://via.placeholder.com/300x300/2980B9/fff?text=Opus"},
    {"title": "Language", "artist": "Porter Robinson", "bpm": 128, "genre": "Progressive House", "key": "Gm", "duration_sec": 360, "cover_url": "https://via.placeholder.com/300x300/27AE60/fff?text=Language"},
    {"title": "Sun & Moon", "artist": "Above & Beyond", "bpm": 132, "genre": "Progressive House", "key": "Em", "duration_sec": 420, "cover_url": "https://via.placeholder.com/300x300/F39C12/fff?text=Sun+Moon"},
    {"title": "Pjanoo", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Dm", "duration_sec": 385, "cover_url": "https://via.placeholder.com/300x300/5DADE2/fff?text=Pjanoo"},

    # Trance
    {"title": "Adagio for Strings", "artist": "Tiesto", "bpm": 138, "genre": "Trance", "key": "Gm", "duration_sec": 480, "cover_url": "https://via.placeholder.com/300x300/9B59B6/fff?text=Adagio"},
    {"title": "Sandstorm", "artist": "Darude", "bpm": 136, "genre": "Trance", "key": "Dm", "duration_sec": 330, "cover_url": "https://via.placeholder.com/300x300/E67E22/fff?text=Sandstorm"},
    {"title": "Children", "artist": "Robert Miles", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 390, "cover_url": "https://via.placeholder.com/300x300/16A085/fff?text=Children"},
    {"title": "Silence", "artist": "Delerium", "bpm": 140, "genre": "Trance", "key": "Fm", "duration_sec": 450, "cover_url": "https://via.placeholder.com/300x300/8E44AD/fff?text=Silence"},
    {"title": "For An Angel", "artist": "Paul van Dyk", "bpm": 140, "genre": "Trance", "key": "Cm", "duration_sec": 520, "cover_url": "https://via.placeholder.com/300x300/5B2C6F/fff?text=For+An+Angel"},

    # Techno
    {"title": "Acid Track", "artist": "Phuture", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 420, "cover_url": "https://via.placeholder.com/300x300/2C3E50/fff?text=Acid+Track"},
    {"title": "Strings of Life", "artist": "Derrick May", "bpm": 128, "genre": "Techno", "key": "Em", "duration_sec": 480, "cover_url": "https://via.placeholder.com/300x300/34495E/fff?text=Strings+of+Life"},
    {"title": "Spastik", "artist": "Plastikman", "bpm": 134, "genre": "Techno", "key": "Dm", "duration_sec": 360, "cover_url": "https://via.placeholder.com/300x300/1A1A2E/fff?text=Spastik"},
    {"title": "The Bells", "artist": "Jeff Mills", "bpm": 132, "genre": "Techno", "key": "Gm", "duration_sec": 390, "cover_url": "https://via.placeholder.com/300x300/16213E/fff?text=The+Bells"},
    {"title": "Windowlicker", "artist": "Aphex Twin", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 360, "cover_url": "https://via.placeholder.com/300x300/4A235A/fff?text=Windowlicker"},

    # Dubstep/Bass
    {"title": "Scary Monsters", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Fm", "duration_sec": 285, "cover_url": "https://via.placeholder.com/300x300/9B2335/fff?text=Scary+Monsters"},
    {"title": "Cinema Remix", "artist": "Skrillex", "bpm": 138, "genre": "Dubstep", "key": "Am", "duration_sec": 240, "cover_url": "https://via.placeholder.com/300x300/4A235A/fff?text=Cinema+Remix"},
    {"title": "Bangarang", "artist": "Skrillex", "bpm": 110, "genre": "Dubstep", "key": "Em", "duration_sec": 215, "cover_url": "https://via.placeholder.com/300x300/922B21/fff?text=Bangarang"},
    {"title": "Nero Promises", "artist": "Nero", "bpm": 175, "genre": "Drum & Bass", "key": "Dm", "duration_sec": 310, "cover_url": "https://via.placeholder.com/300x300/1B4F72/fff?text=Nero+Promises"},
    {"title": "Killing Time", "artist": "Infected Mushroom", "bpm": 145, "genre": "Dubstep", "key": "Gm", "duration_sec": 420, "cover_url": "https://via.placeholder.com/300x300/641E16/fff?text=Killing+Time"},

    # Future Bass/Melodic
    {"title": "Shelter", "artist": "Porter Robinson & Madeon", "bpm": 100, "genre": "Future Bass", "key": "Gm", "duration_sec": 260, "cover_url": "https://via.placeholder.com/300x300/F8BBD9/000?text=Shelter"},
    {"title": "Sad Machine", "artist": "Porter Robinson", "bpm": 100, "genre": "Future Bass", "key": "Am", "duration_sec": 340, "cover_url": "https://via.placeholder.com/300x300/BB8FCE/fff?text=Sad+Machine"},
    {"title": "Faded", "artist": "Alan Walker", "bpm": 90, "genre": "Future Bass", "key": "Fm", "duration_sec": 212, "cover_url": "https://via.placeholder.com/300x300/5DADE2/fff?text=Faded"},
    {"title": "Alone", "artist": "Marshmello", "bpm": 108, "genre": "Future Bass", "key": "Em", "duration_sec": 235, "cover_url": "https://via.placeholder.com/300x300/FADBD8/000?text=Alone"},
    {"title": "Happier", "artist": "Marshmello", "bpm": 100, "genre": "Future Bass", "key": "Cm", "duration_sec": 210, "cover_url": "https://via.placeholder.com/300x300/AED6F1/000?text=Happier"},

    # EDM/Big Room
    {"title": "Animals", "artist": "Martin Garrix", "bpm": 128, "genre": "Big Room", "key": "Fm", "duration_sec": 290, "cover_url": "https://via.placeholder.com/300x300/E74C3C/fff?text=Animals"},
    {"title": "Tremor", "artist": "Dimitri Vegas & Like Mike", "bpm": 128, "genre": "Big Room", "key": "Gm", "duration_sec": 310, "cover_url": "https://via.placeholder.com/300x300/F1C40F/000?text=Tremor"},
    {"title": "Tsunami", "artist": "DVBBS & Borgeous", "bpm": 128, "genre": "Big Room", "key": "Am", "duration_sec": 275, "cover_url": "https://via.placeholder.com/300x300/3498DB/fff?text=Tsunami"},
    {"title": "Epic", "artist": "Sandro Silva & Quintino", "bpm": 130, "genre": "Big Room", "key": "Dm", "duration_sec": 295, "cover_url": "https://via.placeholder.com/300x300/9B59B6/fff?text=Epic"},
    {"title": "Mammoth", "artist": "Dimitri Vegas & Like Mike", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 280, "cover_url": "https://via.placeholder.com/300x300/E67E22/fff?text=Mammoth"},

    # Chillout/Ambient
    {"title": "Intro", "artist": "The xx", "bpm": 110, "genre": "Chillout", "key": "Am", "duration_sec": 240, "cover_url": "https://via.placeholder.com/300x300/2C3E50/fff?text=Intro"},
    {"title": "Teardrop", "artist": "Massive Attack", "bpm": 78, "genre": "Chillout", "key": "Em", "duration_sec": 330, "cover_url": "https://via.placeholder.com/300x300/1A5276/fff?text=Teardrop"},
    {"title": "Porcelain", "artist": "Moby", "bpm": 98, "genre": "Chillout", "key": "Gm", "duration_sec": 245, "cover_url": "https://via.placeholder.com/300x300/85C1E9/000?text=Porcelain"},
    {"title": "Sunset Lover", "artist": "Petit Biscuit", "bpm": 95, "genre": "Chillout", "key": "Fm", "duration_sec": 215, "cover_url": "https://via.placeholder.com/300x300/FAD7A0/000?text=Sunset+Lover"},
    {"title": "Natural Blues", "artist": "Moby", "bpm": 95, "genre": "Chillout", "key": "Dm", "duration_sec": 260, "cover_url": "https://via.placeholder.com/300x300/AED6F1/000?text=Natural+Blues"},

    # Electro House
    {"title": "Ghosts n Stuff", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 360, "cover_url": "https://via.placeholder.com/300x300/7D3C98/fff?text=Ghosts+n+Stuff"},
    {"title": "Satisfaction", "artist": "Benny Benassi", "bpm": 130, "genre": "Electro House", "key": "Am", "duration_sec": 285, "cover_url": "https://via.placeholder.com/300x300/E74C3C/fff?text=Satisfaction"},
    {"title": "Internet Friends", "artist": "Knife Party", "bpm": 128, "genre": "Electro House", "key": "Dm", "duration_sec": 310, "cover_url": "https://via.placeholder.com/300x300/2ECC71/fff?text=Internet+Friends"},
    {"title": "Raise Your Weapon", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Gm", "duration_sec": 480, "cover_url": "https://via.placeholder.com/300x300/9B59B6/fff?text=Raise+Your+Weapon"},
    {"title": "I Remember", "artist": "Deadmau5 & Kaskade", "bpm": 128, "genre": "Electro House", "key": "Em", "duration_sec": 540, "cover_url": "https://via.placeholder.com/300x300/5B2C6F/fff?text=I+Remember"},

    # Melodic Techno
    {"title": "Cherry", "artist": "Tale Of Us", "bpm": 122, "genre": "Melodic Techno", "key": "Am", "duration_sec": 420, "cover_url": "https://via.placeholder.com/300x300/5D6D7E/fff?text=Cherry"},
    {"title": "Innerbloom", "artist": "RUFUS DU SOL", "bpm": 118, "genre": "Melodic Techno", "key": "Fm", "duration_sec": 590, "cover_url": "https://via.placeholder.com/300x300/85929E/fff?text=Innerbloom"},
    {"title": "Solitude", "artist": "Boris Brejcha", "bpm": 126, "genre": "Melodic Techno", "key": "Gm", "duration_sec": 380, "cover_url": "https://via.placeholder.com/300x300/4A235A/fff?text=Solitude"},
    {"title": "Afterlife", "artist": "Anyma", "bpm": 124, "genre": "Melodic Techno", "key": "Em", "duration_sec": 450, "cover_url": "https://via.placeholder.com/300x300/1C2833/fff?text=Afterlife"},
    {"title": "Age of Love", "artist": "Charlotte de Witte", "bpm": 125, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 390, "cover_url": "https://via.placeholder.com/300x300/17202A/fff?text=Age+of+Love"},

    # Tropical House
    {"title": "Firestone", "artist": "Kygo", "bpm": 100, "genre": "Tropical House", "key": "Am", "duration_sec": 240, "cover_url": "https://via.placeholder.com/300x300/F5B041/000?text=Firestone"},
    {"title": "Stole The Show", "artist": "Kygo", "bpm": 102, "genre": "Tropical House", "key": "Gm", "duration_sec": 225, "cover_url": "https://via.placeholder.com/300x300/58D68D/000?text=Stole+The+Show"},
    {"title": "Ocean", "artist": "Martin Garrix", "bpm": 110, "genre": "Tropical House", "key": "Fm", "duration_sec": 195, "cover_url": "https://via.placeholder.com/300x300/5DADE2/fff?text=Ocean"},
    {"title": "Rather Be", "artist": "Clean Bandit", "bpm": 120, "genre": "Tropical House", "key": "Dm", "duration_sec": 230, "cover_url": "https://via.placeholder.com/300x300/AF7AC5/fff?text=Rather+Be"},

    # Hardstyle
    {"title": "The Power of the Mind", "artist": "Wildstylez", "bpm": 150, "genre": "Hardstyle", "key": "Am", "duration_sec": 310, "cover_url": "https://via.placeholder.com/300x300/CB4335/fff?text=Power+Mind"},
    {"title": "Spaceman", "artist": "Hardwell", "bpm": 150, "genre": "Hardstyle", "key": "Em", "duration_sec": 285, "cover_url": "https://via.placeholder.com/300x300/7B241C/fff?text=Spaceman"},
    {"title": "Bass Cannon", "artist": "Flux Pavilion", "bpm": 150, "genre": "Hardstyle", "key": "Dm", "duration_sec": 265, "cover_url": "https://via.placeholder.com/300x300/512E5F/fff?text=Bass+Cannon"},

    # Psytrance
    {"title": "Vini Vici Chakra", "artist": "Vini Vici", "bpm": 145, "genre": "Psytrance", "key": "Am", "duration_sec": 450, "cover_url": "https://via.placeholder.com/300x300/148F77/fff?text=Chakra"},
    {"title": "Hallucinogen LSD", "artist": "Hallucinogen", "bpm": 142, "genre": "Psytrance", "key": "Em", "duration_sec": 520, "cover_url": "https://via.placeholder.com/300x300/1E8449/fff?text=LSD"},
    {"title": "The Great Spirit", "artist": "Armin van Buuren & Vini Vici", "bpm": 148, "genre": "Psytrance", "key": "Gm", "duration_sec": 380, "cover_url": "https://via.placeholder.com/300x300/0E6251/fff?text=Great+Spirit"},
]

with app.app_context():
    added = 0
    for track_data in new_tracks:
        # 检查是否已存在
        existing = Track.query.filter_by(title=track_data["title"], artist=track_data["artist"]).first()
        if not existing:
            track = Track(**track_data)
            db.session.add(track)
            added += 1
    db.session.commit()
    total = Track.query.count()
    print(f"Added {added} new tracks. Total tracks in database: {total}")
