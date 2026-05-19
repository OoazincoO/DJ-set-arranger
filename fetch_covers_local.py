"""在本地获取iTunes封面URL，生成更新脚本"""
import requests
import urllib.parse
import time
import json

# 从服务器获取的歌曲列表（需要先获取）
def get_itunes_artwork(artist, title):
    """从iTunes搜索获取专辑封面URL"""
    try:
        query = f"{artist} {title}".replace("ft.", "").replace("feat.", "").replace("&", "and")
        encoded_query = urllib.parse.quote(query)
        url = f"https://itunes.apple.com/search?term={encoded_query}&entity=song&limit=1"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('resultCount', 0) > 0:
                artwork_url = data['results'][0].get('artworkUrl100', '')
                if artwork_url:
                    return artwork_url.replace('100x100bb', '600x600bb')
    except Exception as e:
        print(f"  Error: {e}")
    return None

# 主要艺术家和歌曲列表
tracks_to_update = [
    # Deadmau5
    ("Deadmau5", "Strobe"),
    ("Deadmau5", "Ghosts n Stuff"),
    ("Deadmau5", "I Remember"),
    ("Deadmau5", "Raise Your Weapon"),
    ("Deadmau5", "Some Chords"),
    ("Deadmau5", "The Veldt"),
    ("Deadmau5", "Faxing Berlin"),
    ("Deadmau5", "Not Exactly"),
    ("Deadmau5", "Aural Psynapse"),
    ("Deadmau5", "Right This Second"),
    ("Deadmau5", "Cthulhu Sleeps"),
    ("Deadmau5", "Arguru"),

    # Tiesto
    ("Tiesto", "Adagio for Strings"),
    ("Tiesto", "Red Lights"),
    ("Tiesto", "Traffic"),
    ("Tiesto", "Elements of Life"),
    ("Tiesto", "Lethal Industry"),
    ("Tiesto", "The Business"),
    ("Tiesto", "Wasted"),
    ("Tiesto", "Secrets"),

    # Armin van Buuren
    ("Armin van Buuren", "This Is What It Feels Like"),
    ("Armin van Buuren", "Blah Blah Blah"),
    ("Armin van Buuren", "Communication"),
    ("Armin van Buuren", "In and Out of Love"),
    ("Armin van Buuren", "Ping Pong"),
    ("Armin van Buuren", "Shivers"),

    # David Guetta
    ("David Guetta", "Titanium"),
    ("David Guetta", "Without You"),
    ("David Guetta", "When Love Takes Over"),
    ("David Guetta", "Sexy Bitch"),
    ("David Guetta", "Memories"),
    ("David Guetta", "Play Hard"),
    ("David Guetta", "Hey Mama"),
    ("David Guetta", "Dangerous"),

    # Calvin Harris
    ("Calvin Harris", "Summer"),
    ("Calvin Harris", "Feel So Close"),
    ("Calvin Harris", "This Is What You Came For"),
    ("Calvin Harris", "How Deep Is Your Love"),
    ("Calvin Harris", "Outside"),
    ("Calvin Harris", "Sweet Nothing"),
    ("Calvin Harris", "We Found Love"),
    ("Calvin Harris", "One Kiss"),
    ("Calvin Harris", "Promises"),

    # Martin Garrix
    ("Martin Garrix", "Animals"),
    ("Martin Garrix", "Scared To Be Lonely"),
    ("Martin Garrix", "High On Life"),
    ("Martin Garrix", "In The Name of Love"),
    ("Martin Garrix", "Forbidden Voices"),
    ("Martin Garrix", "Wizard"),
    ("Martin Garrix", "Ocean"),

    # Skrillex
    ("Skrillex", "Bangarang"),
    ("Skrillex", "Scary Monsters and Nice Sprites"),
    ("Skrillex", "Cinema"),
    ("Skrillex", "First of the Year"),
    ("Skrillex", "Summit"),
    ("Skrillex", "Kyoto"),

    # Avicii
    ("Avicii", "Wake Me Up"),
    ("Avicii", "Levels"),
    ("Avicii", "Hey Brother"),
    ("Avicii", "Waiting For Love"),
    ("Avicii", "The Nights"),
    ("Avicii", "Addicted To You"),
    ("Avicii", "Seek Bromance"),
    ("Avicii", "I Could Be The One"),
    ("Avicii", "Without You"),
    ("Avicii", "SOS"),

    # Swedish House Mafia
    ("Swedish House Mafia", "Don't You Worry Child"),
    ("Swedish House Mafia", "Save The World"),
    ("Swedish House Mafia", "One"),
    ("Swedish House Mafia", "Greyhound"),
    ("Swedish House Mafia", "Antidote"),
    ("Swedish House Mafia", "Moth To A Flame"),

    # Eric Prydz
    ("Eric Prydz", "Call On Me"),
    ("Eric Prydz", "Pjanoo"),
    ("Eric Prydz", "Opus"),
    ("Eric Prydz", "Every Day"),
    ("Eric Prydz", "Liberate"),

    # Daft Punk
    ("Daft Punk", "One More Time"),
    ("Daft Punk", "Around The World"),
    ("Daft Punk", "Get Lucky"),
    ("Daft Punk", "Harder Better Faster Stronger"),
    ("Daft Punk", "Digital Love"),
    ("Daft Punk", "Something About Us"),
    ("Daft Punk", "Instant Crush"),
    ("Daft Punk", "Da Funk"),
    ("Daft Punk", "Robot Rock"),

    # Above & Beyond
    ("Above & Beyond", "Sun Moon"),
    ("Above & Beyond", "Thing Called Love"),
    ("Above & Beyond", "You Got to Go"),
    ("Above & Beyond", "Satellite"),

    # Kygo
    ("Kygo", "Firestone"),
    ("Kygo", "Stole The Show"),
    ("Kygo", "It Aint Me"),
    ("Kygo", "Stargazing"),
    ("Kygo", "Higher Love"),
    ("Kygo", "Happy Now"),

    # Marshmello
    ("Marshmello", "Alone"),
    ("Marshmello", "Happier"),
    ("Marshmello", "Wolves"),
    ("Marshmello", "Friends"),
    ("Marshmello", "Silence"),

    # Zedd
    ("Zedd", "Clarity"),
    ("Zedd", "Stay The Night"),
    ("Zedd", "Beautiful Now"),
    ("Zedd", "Spectrum"),
    ("Zedd", "The Middle"),
    ("Zedd", "Stay"),

    # Fisher
    ("Fisher", "Losing It"),
    ("Fisher", "You Little Beauty"),
    ("Fisher", "Stop It"),

    # Charlotte de Witte
    ("Charlotte de Witte", "Age of Love"),

    # Amelie Lens
    ("Amelie Lens", "In Silence"),
    ("Amelie Lens", "Follow"),

    # Tale of Us
    ("Tale Of Us", "Alone"),

    # Boris Brejcha
    ("Boris Brejcha", "Gravity"),
    ("Boris Brejcha", "Purple Noise"),

    # Chris Lake
    ("Chris Lake", "Operator"),
    ("Chris Lake", "Turn Off The Lights"),

    # RUFUS DU SOL
    ("RUFUS DU SOL", "Innerbloom"),
    ("RUFUS DU SOL", "You Were Right"),
    ("RUFUS DU SOL", "Alive"),

    # CamelPhat
    ("CamelPhat", "Cola"),
    ("CamelPhat", "Panic Room"),
    ("CamelPhat", "Breathe"),

    # Disclosure
    ("Disclosure", "Latch"),
    ("Disclosure", "White Noise"),
    ("Disclosure", "You Me"),
    ("Disclosure", "F for You"),
    ("Disclosure", "Omen"),

    # Flume
    ("Flume", "Never Be Like You"),
    ("Flume", "Say It"),
    ("Flume", "Holdin On"),

    # Illenium
    ("Illenium", "Good Things Fall Apart"),
    ("Illenium", "Takeaway"),
    ("Illenium", "Feel Good"),

    # Seven Lions
    ("Seven Lions", "Strangers"),
    ("Seven Lions", "Don't Leave"),

    # Major Lazer
    ("Major Lazer", "Lean On"),
    ("Major Lazer", "Cold Water"),
    ("Major Lazer", "Light It Up"),
    ("Major Lazer", "Powerful"),

    # Classics
    ("Darude", "Sandstorm"),
    ("Robert Miles", "Children"),
    ("Gigi D'Agostino", "L'Amour Toujours"),
    ("Alice Deejay", "Better Off Alone"),
    ("Eiffel 65", "Blue"),

    # More
    ("Pendulum", "Watercolour"),
    ("Pendulum", "The Island"),
    ("Bassnectar", "Bass Head"),
    ("The xx", "Intro"),
    ("Massive Attack", "Teardrop"),
    ("Moby", "Porcelain"),
    ("M83", "Midnight City"),
]

# 获取封面
cover_mapping = {}
total = len(tracks_to_update)
found = 0

print(f"Fetching covers for {total} tracks...")

for i, (artist, title) in enumerate(tracks_to_update):
    if (i + 1) % 20 == 0:
        print(f"Progress: {i+1}/{total}")

    artwork = get_itunes_artwork(artist, title)
    if artwork:
        cover_mapping[(artist.lower(), title.lower())] = artwork
        found += 1

    time.sleep(0.2)

print(f"\nFound {found}/{total} covers")

# 保存为JSON
with open('c:/project/myDJset/cover_mapping.json', 'w', encoding='utf-8') as f:
    # 转换为可序列化格式
    serializable = {f"{k[0]}|||{k[1]}": v for k, v in cover_mapping.items()}
    json.dump(serializable, f, ensure_ascii=False, indent=2)

print(f"Saved to cover_mapping.json")
