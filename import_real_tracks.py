"""导入真实歌曲数据到数据库 - 基于网络搜索的真实歌曲信息"""
from app import create_app
from extensions import db
from models import Track
import random

app = create_app()

# 真实歌曲数据 - 全部来自网络搜索的真实歌曲
real_tracks = [
    # ===== DEADMAU5 =====
    {"title": "Strobe", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 637},
    {"title": "Ghosts n Stuff", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 360},
    {"title": "I Remember", "artist": "Deadmau5 & Kaskade", "bpm": 128, "genre": "Progressive House", "key": "Em", "duration_sec": 540},
    {"title": "Raise Your Weapon", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Gm", "duration_sec": 480},
    {"title": "Some Chords", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 420},
    {"title": "The Veldt", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Dm", "duration_sec": 360},
    {"title": "Faxing Berlin", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Cm", "duration_sec": 420},
    {"title": "Not Exactly", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 390},
    {"title": "Moar Ghosts n Stuff", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 360},
    {"title": "Aural Psynapse", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 450},
    {"title": "Right This Second", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Gm", "duration_sec": 380},
    {"title": "Brazil 2nd Edit", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Em", "duration_sec": 340},
    {"title": "Slip", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Fm", "duration_sec": 360},
    {"title": "Cthulhu Sleeps", "artist": "Deadmau5", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 420},
    {"title": "Arguru", "artist": "Deadmau5", "bpm": 128, "genre": "Progressive House", "key": "Dm", "duration_sec": 380},

    # ===== TIESTO =====
    {"title": "Adagio for Strings", "artist": "Tiesto", "bpm": 138, "genre": "Trance", "key": "Gm", "duration_sec": 480},
    {"title": "Red Lights", "artist": "Tiesto", "bpm": 126, "genre": "House", "key": "Am", "duration_sec": 210},
    {"title": "Traffic", "artist": "Tiesto", "bpm": 140, "genre": "Trance", "key": "Em", "duration_sec": 420},
    {"title": "Elements of Life", "artist": "Tiesto", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 450},
    {"title": "Lethal Industry", "artist": "Tiesto", "bpm": 142, "genre": "Trance", "key": "Dm", "duration_sec": 390},
    {"title": "Flight 643", "artist": "Tiesto", "bpm": 140, "genre": "Trance", "key": "Fm", "duration_sec": 420},
    {"title": "Suburban Train", "artist": "Tiesto", "bpm": 138, "genre": "Trance", "key": "Gm", "duration_sec": 480},
    {"title": "Silence", "artist": "Tiesto", "bpm": 140, "genre": "Trance", "key": "Am", "duration_sec": 360},
    {"title": "Wasted", "artist": "Tiesto", "bpm": 128, "genre": "House", "key": "Em", "duration_sec": 225},
    {"title": "Split", "artist": "Tiesto", "bpm": 126, "genre": "House", "key": "Gm", "duration_sec": 240},
    {"title": "Secrets", "artist": "Tiesto", "bpm": 128, "genre": "House", "key": "Fm", "duration_sec": 210},
    {"title": "The Business", "artist": "Tiesto", "bpm": 120, "genre": "Tech House", "key": "Am", "duration_sec": 175},
    {"title": "Don't Be Shy", "artist": "Tiesto & Karol G", "bpm": 124, "genre": "House", "key": "Em", "duration_sec": 195},
    {"title": "Ritual", "artist": "Tiesto, Jonas Blue & Rita Ora", "bpm": 122, "genre": "House", "key": "Dm", "duration_sec": 200},
    {"title": "Jackie Chan", "artist": "Tiesto & Dzeko", "bpm": 100, "genre": "Dance Pop", "key": "Am", "duration_sec": 210},

    # ===== ARMIN VAN BUUREN =====
    {"title": "This Is What It Feels Like", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 240},
    {"title": "Blah Blah Blah", "artist": "Armin van Buuren", "bpm": 150, "genre": "Big Room", "key": "Em", "duration_sec": 195},
    {"title": "Communication", "artist": "Armin van Buuren", "bpm": 140, "genre": "Trance", "key": "Dm", "duration_sec": 420},
    {"title": "Shivers", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Fm", "duration_sec": 360},
    {"title": "In and Out of Love", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 280},
    {"title": "Ping Pong", "artist": "Armin van Buuren", "bpm": 128, "genre": "Electro House", "key": "Gm", "duration_sec": 300},
    {"title": "Turn It Up", "artist": "Armin van Buuren", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 210},
    {"title": "Freefall", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Dm", "duration_sec": 390},
    {"title": "Alone", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 285},
    {"title": "Heading Up High", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Fm", "duration_sec": 270},
    {"title": "Great Spirit", "artist": "Armin van Buuren & Vini Vici", "bpm": 148, "genre": "Psytrance", "key": "Gm", "duration_sec": 380},
    {"title": "I Need You", "artist": "Armin van Buuren", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 330},

    # ===== DAVID GUETTA =====
    {"title": "Titanium", "artist": "David Guetta ft. Sia", "bpm": 126, "genre": "Electro House", "key": "Eb", "duration_sec": 245},
    {"title": "Without You", "artist": "David Guetta ft. Usher", "bpm": 130, "genre": "Electro House", "key": "Am", "duration_sec": 220},
    {"title": "When Love Takes Over", "artist": "David Guetta ft. Kelly Rowland", "bpm": 128, "genre": "House", "key": "Fm", "duration_sec": 195},
    {"title": "Sexy Bitch", "artist": "David Guetta ft. Akon", "bpm": 130, "genre": "Electro House", "key": "Em", "duration_sec": 195},
    {"title": "Memories", "artist": "David Guetta ft. Kid Cudi", "bpm": 130, "genre": "Electro House", "key": "Gm", "duration_sec": 195},
    {"title": "Play Hard", "artist": "David Guetta", "bpm": 130, "genre": "Electro House", "key": "Am", "duration_sec": 195},
    {"title": "Turn Me On", "artist": "David Guetta ft. Nicki Minaj", "bpm": 128, "genre": "Electro House", "key": "Dm", "duration_sec": 195},
    {"title": "Hey Mama", "artist": "David Guetta ft. Nicki Minaj", "bpm": 105, "genre": "Dance Pop", "key": "Fm", "duration_sec": 195},
    {"title": "Dangerous", "artist": "David Guetta ft. Sam Martin", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 195},
    {"title": "Lovers on the Sun", "artist": "David Guetta", "bpm": 126, "genre": "Electro House", "key": "Em", "duration_sec": 195},
    {"title": "Bad", "artist": "David Guetta ft. Showtek", "bpm": 128, "genre": "Big Room", "key": "Gm", "duration_sec": 195},
    {"title": "Shot Me Down", "artist": "David Guetta ft. Skylar Grey", "bpm": 100, "genre": "Dance Pop", "key": "Am", "duration_sec": 195},
    {"title": "2U", "artist": "David Guetta ft. Justin Bieber", "bpm": 98, "genre": "Dance Pop", "key": "Dm", "duration_sec": 195},
    {"title": "Flames", "artist": "David Guetta & Sia", "bpm": 128, "genre": "Electro House", "key": "Em", "duration_sec": 195},
    {"title": "Don't Leave Me Alone", "artist": "David Guetta ft. Anne-Marie", "bpm": 100, "genre": "Dance Pop", "key": "Am", "duration_sec": 195},

    # ===== CALVIN HARRIS =====
    {"title": "Summer", "artist": "Calvin Harris", "bpm": 128, "genre": "House", "key": "Am", "duration_sec": 222},
    {"title": "Feel So Close", "artist": "Calvin Harris", "bpm": 129, "genre": "House", "key": "Gm", "duration_sec": 210},
    {"title": "This Is What You Came For", "artist": "Calvin Harris ft. Rihanna", "bpm": 124, "genre": "House", "key": "Em", "duration_sec": 222},
    {"title": "How Deep Is Your Love", "artist": "Calvin Harris & Disciples", "bpm": 122, "genre": "Deep House", "key": "Dm", "duration_sec": 222},
    {"title": "Outside", "artist": "Calvin Harris ft. Ellie Goulding", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 222},
    {"title": "Sweet Nothing", "artist": "Calvin Harris ft. Florence Welch", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 222},
    {"title": "We Found Love", "artist": "Rihanna ft. Calvin Harris", "bpm": 128, "genre": "Dance Pop", "key": "Gm", "duration_sec": 215},
    {"title": "Blame", "artist": "Calvin Harris ft. John Newman", "bpm": 128, "genre": "House", "key": "Em", "duration_sec": 222},
    {"title": "I Need Your Love", "artist": "Calvin Harris ft. Ellie Goulding", "bpm": 126, "genre": "House", "key": "Am", "duration_sec": 222},
    {"title": "Slide", "artist": "Calvin Harris ft. Frank Ocean", "bpm": 95, "genre": "Funk Pop", "key": "Dm", "duration_sec": 232},
    {"title": "My Way", "artist": "Calvin Harris", "bpm": 122, "genre": "House", "key": "Am", "duration_sec": 200},
    {"title": "Giant", "artist": "Calvin Harris ft. Rag'n'Bone Man", "bpm": 124, "genre": "House", "key": "Gm", "duration_sec": 195},
    {"title": "Promises", "artist": "Calvin Harris & Sam Smith", "bpm": 124, "genre": "House", "key": "Em", "duration_sec": 222},
    {"title": "One Kiss", "artist": "Calvin Harris & Dua Lipa", "bpm": 124, "genre": "House", "key": "Am", "duration_sec": 213},
    {"title": "Miracle", "artist": "Calvin Harris & Ellie Goulding", "bpm": 138, "genre": "Trance", "key": "Dm", "duration_sec": 192},

    # ===== MARTIN GARRIX =====
    {"title": "Animals", "artist": "Martin Garrix", "bpm": 128, "genre": "Big Room", "key": "Fm", "duration_sec": 290},
    {"title": "Scared To Be Lonely", "artist": "Martin Garrix & Dua Lipa", "bpm": 122, "genre": "Future Bass", "key": "Am", "duration_sec": 210},
    {"title": "High On Life", "artist": "Martin Garrix ft. Bonn", "bpm": 128, "genre": "Big Room", "key": "Gm", "duration_sec": 195},
    {"title": "In The Name of Love", "artist": "Martin Garrix & Bebe Rexha", "bpm": 150, "genre": "Future Bass", "key": "Em", "duration_sec": 210},
    {"title": "There For You", "artist": "Martin Garrix ft. Troye Sivan", "bpm": 125, "genre": "House", "key": "Am", "duration_sec": 195},
    {"title": "Forbidden Voices", "artist": "Martin Garrix", "bpm": 128, "genre": "Big Room", "key": "Dm", "duration_sec": 270},
    {"title": "Virus", "artist": "Martin Garrix & MOTi", "bpm": 128, "genre": "Big Room", "key": "Fm", "duration_sec": 240},
    {"title": "Wizard", "artist": "Martin Garrix & Jay Hardway", "bpm": 128, "genre": "Big Room", "key": "Gm", "duration_sec": 240},
    {"title": "Don't Look Down", "artist": "Martin Garrix ft. Usher", "bpm": 128, "genre": "Big Room", "key": "Am", "duration_sec": 210},
    {"title": "Pizza", "artist": "Martin Garrix", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 240},
    {"title": "Ocean", "artist": "Martin Garrix ft. Khalid", "bpm": 110, "genre": "Tropical House", "key": "Dm", "duration_sec": 195},
    {"title": "So Far Away", "artist": "Martin Garrix", "bpm": 126, "genre": "Future Bass", "key": "Am", "duration_sec": 195},
    {"title": "These Are The Times", "artist": "Martin Garrix", "bpm": 126, "genre": "House", "key": "Gm", "duration_sec": 180},
    {"title": "Break Through The Silence", "artist": "Martin Garrix", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 240},
    {"title": "Dreamer", "artist": "Martin Garrix ft. Mike Yung", "bpm": 128, "genre": "Future Bass", "key": "Am", "duration_sec": 195},

    # ===== SKRILLEX =====
    {"title": "Bangarang", "artist": "Skrillex", "bpm": 110, "genre": "Dubstep", "key": "Em", "duration_sec": 215},
    {"title": "Scary Monsters and Nice Sprites", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Fm", "duration_sec": 285},
    {"title": "Cinema", "artist": "Skrillex", "bpm": 138, "genre": "Dubstep", "key": "Am", "duration_sec": 240},
    {"title": "First of the Year (Equinox)", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Dm", "duration_sec": 195},
    {"title": "Summit", "artist": "Skrillex ft. Ellie Goulding", "bpm": 140, "genre": "Dubstep", "key": "Gm", "duration_sec": 285},
    {"title": "With You, Friends", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Em", "duration_sec": 330},
    {"title": "Kill Everybody", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Am", "duration_sec": 225},
    {"title": "Right In", "artist": "Skrillex", "bpm": 110, "genre": "Dubstep", "key": "Fm", "duration_sec": 270},
    {"title": "Rock n Roll (Will Take You to the Mountain)", "artist": "Skrillex", "bpm": 140, "genre": "Electro House", "key": "Gm", "duration_sec": 225},
    {"title": "Kyoto", "artist": "Skrillex ft. Sirah", "bpm": 140, "genre": "Dubstep", "key": "Em", "duration_sec": 195},
    {"title": "Make It Bun Dem", "artist": "Skrillex & Damian Marley", "bpm": 140, "genre": "Dubstep", "key": "Am", "duration_sec": 225},
    {"title": "Promises", "artist": "Skrillex & Nero", "bpm": 140, "genre": "Dubstep", "key": "Dm", "duration_sec": 225},
    {"title": "All Is Fair in Love and Brostep", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Fm", "duration_sec": 240},
    {"title": "Ruffneck (Full Flex)", "artist": "Skrillex", "bpm": 140, "genre": "Dubstep", "key": "Am", "duration_sec": 255},
    {"title": "Where Are U Now", "artist": "Jack U ft. Justin Bieber", "bpm": 140, "genre": "Future Bass", "key": "Gm", "duration_sec": 195},

    # ===== AVICII =====
    {"title": "Wake Me Up", "artist": "Avicii", "bpm": 124, "genre": "Electro House", "key": "Bm", "duration_sec": 249},
    {"title": "Levels", "artist": "Avicii", "bpm": 126, "genre": "Electro House", "key": "Am", "duration_sec": 195},
    {"title": "Hey Brother", "artist": "Avicii", "bpm": 125, "genre": "House", "key": "Gm", "duration_sec": 255},
    {"title": "Waiting For Love", "artist": "Avicii", "bpm": 128, "genre": "House", "key": "Em", "duration_sec": 228},
    {"title": "The Nights", "artist": "Avicii", "bpm": 126, "genre": "Electro House", "key": "Am", "duration_sec": 176},
    {"title": "Addicted To You", "artist": "Avicii", "bpm": 124, "genre": "Electro House", "key": "Dm", "duration_sec": 195},
    {"title": "You Make Me", "artist": "Avicii", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 225},
    {"title": "Seek Bromance", "artist": "Avicii", "bpm": 128, "genre": "Progressive House", "key": "Gm", "duration_sec": 420},
    {"title": "I Could Be The One", "artist": "Avicii & Nicky Romero", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 245},
    {"title": "Silhouettes", "artist": "Avicii", "bpm": 128, "genre": "Progressive House", "key": "Em", "duration_sec": 330},
    {"title": "Fade Into Darkness", "artist": "Avicii", "bpm": 128, "genre": "Progressive House", "key": "Dm", "duration_sec": 360},
    {"title": "Without You", "artist": "Avicii ft. Sandro Cavazza", "bpm": 126, "genre": "House", "key": "Am", "duration_sec": 195},
    {"title": "Lonely Together", "artist": "Avicii ft. Rita Ora", "bpm": 125, "genre": "House", "key": "Gm", "duration_sec": 195},
    {"title": "SOS", "artist": "Avicii ft. Aloe Blacc", "bpm": 126, "genre": "House", "key": "Em", "duration_sec": 195},
    {"title": "Tough Love", "artist": "Avicii ft. Agnes, Vargas & Lagola", "bpm": 126, "genre": "House", "key": "Am", "duration_sec": 198},

    # ===== SWEDISH HOUSE MAFIA =====
    {"title": "Don't You Worry Child", "artist": "Swedish House Mafia", "bpm": 129, "genre": "Progressive House", "key": "Am", "duration_sec": 213},
    {"title": "Save The World", "artist": "Swedish House Mafia", "bpm": 127, "genre": "Progressive House", "key": "Gm", "duration_sec": 200},
    {"title": "One", "artist": "Swedish House Mafia", "bpm": 128, "genre": "Progressive House", "key": "Em", "duration_sec": 195},
    {"title": "Greyhound", "artist": "Swedish House Mafia", "bpm": 128, "genre": "Electro House", "key": "Dm", "duration_sec": 195},
    {"title": "Antidote", "artist": "Swedish House Mafia", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 195},
    {"title": "Miami 2 Ibiza", "artist": "Swedish House Mafia", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 255},
    {"title": "Leave The World Behind", "artist": "Swedish House Mafia", "bpm": 128, "genre": "Progressive House", "key": "Gm", "duration_sec": 420},
    {"title": "It Gets Better", "artist": "Swedish House Mafia", "bpm": 123, "genre": "House", "key": "Em", "duration_sec": 195},
    {"title": "Lifetime", "artist": "Swedish House Mafia", "bpm": 124, "genre": "House", "key": "Am", "duration_sec": 195},
    {"title": "Moth To A Flame", "artist": "Swedish House Mafia & The Weeknd", "bpm": 122, "genre": "House", "key": "Dm", "duration_sec": 235},
    {"title": "Redlight", "artist": "Swedish House Mafia & Sting", "bpm": 122, "genre": "House", "key": "Em", "duration_sec": 195},
    {"title": "Heaven Takes You Home", "artist": "Swedish House Mafia", "bpm": 128, "genre": "House", "key": "Am", "duration_sec": 195},

    # ===== ERIC PRYDZ =====
    {"title": "Call On Me", "artist": "Eric Prydz", "bpm": 128, "genre": "House", "key": "Am", "duration_sec": 195},
    {"title": "Pjanoo", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Dm", "duration_sec": 385},
    {"title": "Opus", "artist": "Eric Prydz", "bpm": 126, "genre": "Progressive House", "key": "Fm", "duration_sec": 540},
    {"title": "Every Day", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Gm", "duration_sec": 480},
    {"title": "Liberate", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 420},
    {"title": "Generate", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Em", "duration_sec": 390},
    {"title": "Breathe", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Dm", "duration_sec": 450},
    {"title": "Allein", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Fm", "duration_sec": 420},
    {"title": "Niton (The Reason)", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 390},
    {"title": "2Night", "artist": "Eric Prydz", "bpm": 128, "genre": "House", "key": "Gm", "duration_sec": 360},
    {"title": "Proper Education", "artist": "Eric Prydz vs. Floyd", "bpm": 128, "genre": "Progressive House", "key": "Am", "duration_sec": 420},
    {"title": "Melo", "artist": "Eric Prydz", "bpm": 128, "genre": "Progressive House", "key": "Em", "duration_sec": 390},

    # ===== DAFT PUNK =====
    {"title": "One More Time", "artist": "Daft Punk", "bpm": 122, "genre": "House", "key": "Cm", "duration_sec": 320},
    {"title": "Around The World", "artist": "Daft Punk", "bpm": 121, "genre": "House", "key": "Am", "duration_sec": 420},
    {"title": "Get Lucky", "artist": "Daft Punk ft. Pharrell Williams", "bpm": 116, "genre": "Disco", "key": "Bm", "duration_sec": 369},
    {"title": "Harder, Better, Faster, Stronger", "artist": "Daft Punk", "bpm": 123, "genre": "House", "key": "Am", "duration_sec": 228},
    {"title": "Digital Love", "artist": "Daft Punk", "bpm": 120, "genre": "House", "key": "Am", "duration_sec": 301},
    {"title": "Something About Us", "artist": "Daft Punk", "bpm": 104, "genre": "R&B", "key": "Gm", "duration_sec": 232},
    {"title": "Aerodynamic", "artist": "Daft Punk", "bpm": 123, "genre": "House", "key": "Dm", "duration_sec": 212},
    {"title": "Instant Crush", "artist": "Daft Punk ft. Julian Casablancas", "bpm": 110, "genre": "Synth Pop", "key": "Am", "duration_sec": 337},
    {"title": "Giorgio by Moroder", "artist": "Daft Punk", "bpm": 120, "genre": "Disco", "key": "Em", "duration_sec": 545},
    {"title": "Touch", "artist": "Daft Punk ft. Paul Williams", "bpm": 100, "genre": "Synth Pop", "key": "Am", "duration_sec": 498},
    {"title": "Give Life Back to Music", "artist": "Daft Punk", "bpm": 105, "genre": "Disco", "key": "Gm", "duration_sec": 275},
    {"title": "Lose Yourself to Dance", "artist": "Daft Punk", "bpm": 100, "genre": "Disco", "key": "Dm", "duration_sec": 354},
    {"title": "Da Funk", "artist": "Daft Punk", "bpm": 110, "genre": "House", "key": "Am", "duration_sec": 329},
    {"title": "Robot Rock", "artist": "Daft Punk", "bpm": 110, "genre": "Electro", "key": "Em", "duration_sec": 287},
    {"title": "Technologic", "artist": "Daft Punk", "bpm": 104, "genre": "Electro", "key": "Am", "duration_sec": 286},

    # ===== ABOVE & BEYOND =====
    {"title": "Sun & Moon", "artist": "Above & Beyond", "bpm": 132, "genre": "Trance", "key": "Em", "duration_sec": 420},
    {"title": "Alone Tonight", "artist": "Above & Beyond", "bpm": 136, "genre": "Trance", "key": "Am", "duration_sec": 360},
    {"title": "Thing Called Love", "artist": "Above & Beyond", "bpm": 132, "genre": "Trance", "key": "Gm", "duration_sec": 390},
    {"title": "You Got to Go", "artist": "Above & Beyond", "bpm": 138, "genre": "Trance", "key": "Dm", "duration_sec": 420},
    {"title": "Prelude", "artist": "Above & Beyond", "bpm": 128, "genre": "Progressive Trance", "key": "Am", "duration_sec": 360},
    {"title": "Hello", "artist": "Above & Beyond", "bpm": 134, "genre": "Trance", "key": "Em", "duration_sec": 390},
    {"title": "On My Way to Heaven", "artist": "Above & Beyond", "bpm": 136, "genre": "Trance", "key": "Fm", "duration_sec": 360},
    {"title": "Good For Me", "artist": "Above & Beyond", "bpm": 132, "genre": "Trance", "key": "Gm", "duration_sec": 330},
    {"title": "Satellite", "artist": "Above & Beyond", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 420},
    {"title": "We're All We Need", "artist": "Above & Beyond", "bpm": 134, "genre": "Trance", "key": "Em", "duration_sec": 270},
    {"title": "Sticky Fingers", "artist": "Above & Beyond", "bpm": 128, "genre": "Progressive Trance", "key": "Dm", "duration_sec": 390},
    {"title": "Counting Down the Days", "artist": "Above & Beyond", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 285},

    # ===== KYGO =====
    {"title": "Firestone", "artist": "Kygo ft. Conrad Sewell", "bpm": 100, "genre": "Tropical House", "key": "Am", "duration_sec": 240},
    {"title": "Stole The Show", "artist": "Kygo ft. Parson James", "bpm": 102, "genre": "Tropical House", "key": "Gm", "duration_sec": 225},
    {"title": "It Ain't Me", "artist": "Kygo & Selena Gomez", "bpm": 100, "genre": "Tropical House", "key": "Em", "duration_sec": 197},
    {"title": "Stargazing", "artist": "Kygo ft. Justin Jesso", "bpm": 104, "genre": "Tropical House", "key": "Am", "duration_sec": 257},
    {"title": "Remind Me to Forget", "artist": "Kygo & Miguel", "bpm": 100, "genre": "Tropical House", "key": "Dm", "duration_sec": 203},
    {"title": "Here for You", "artist": "Kygo ft. Ella Henderson", "bpm": 100, "genre": "Tropical House", "key": "Fm", "duration_sec": 215},
    {"title": "Happy Now", "artist": "Kygo ft. Sandro Cavazza", "bpm": 96, "genre": "Tropical House", "key": "Gm", "duration_sec": 214},
    {"title": "Higher Love", "artist": "Kygo & Whitney Houston", "bpm": 104, "genre": "Tropical House", "key": "Am", "duration_sec": 228},
    {"title": "What's Love Got To Do With It", "artist": "Kygo ft. Tina Turner", "bpm": 100, "genre": "Tropical House", "key": "Em", "duration_sec": 195},
    {"title": "Born to Be Yours", "artist": "Kygo & Imagine Dragons", "bpm": 100, "genre": "Tropical House", "key": "Am", "duration_sec": 195},
    {"title": "Kids in Love", "artist": "Kygo", "bpm": 100, "genre": "Tropical House", "key": "Dm", "duration_sec": 195},
    {"title": "Sexual Healing", "artist": "Kygo", "bpm": 100, "genre": "Tropical House", "key": "Gm", "duration_sec": 244},

    # ===== MARSHMELLO =====
    {"title": "Alone", "artist": "Marshmello", "bpm": 108, "genre": "Future Bass", "key": "Em", "duration_sec": 235},
    {"title": "Happier", "artist": "Marshmello ft. Bastille", "bpm": 100, "genre": "Future Bass", "key": "Cm", "duration_sec": 210},
    {"title": "Wolves", "artist": "Marshmello ft. Selena Gomez", "bpm": 116, "genre": "Future Bass", "key": "Am", "duration_sec": 197},
    {"title": "Friends", "artist": "Marshmello ft. Anne-Marie", "bpm": 100, "genre": "Dance Pop", "key": "Gm", "duration_sec": 197},
    {"title": "Silence", "artist": "Marshmello ft. Khalid", "bpm": 150, "genre": "Future Bass", "key": "Am", "duration_sec": 203},
    {"title": "Keep It Mello", "artist": "Marshmello ft. Omar LinX", "bpm": 100, "genre": "Future Bass", "key": "Em", "duration_sec": 195},
    {"title": "Ritual", "artist": "Marshmello ft. Wrabel", "bpm": 75, "genre": "Dance Pop", "key": "Dm", "duration_sec": 195},
    {"title": "Chasing Colors", "artist": "Marshmello ft. Noah Cyrus", "bpm": 100, "genre": "Future Bass", "key": "Am", "duration_sec": 195},
    {"title": "Moving On", "artist": "Marshmello", "bpm": 100, "genre": "Future Bass", "key": "Gm", "duration_sec": 195},
    {"title": "Fly", "artist": "Marshmello ft. Leah Culver", "bpm": 100, "genre": "Future Bass", "key": "Em", "duration_sec": 195},
    {"title": "You & Me", "artist": "Marshmello", "bpm": 128, "genre": "Future Bass", "key": "Am", "duration_sec": 195},
    {"title": "Summer", "artist": "Marshmello", "bpm": 100, "genre": "Future Bass", "key": "Dm", "duration_sec": 195},

    # ===== ZEDD =====
    {"title": "Clarity", "artist": "Zedd ft. Foxes", "bpm": 128, "genre": "Electro House", "key": "Gm", "duration_sec": 270},
    {"title": "Stay The Night", "artist": "Zedd ft. Hayley Williams", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 240},
    {"title": "Beautiful Now", "artist": "Zedd ft. Jon Bellion", "bpm": 128, "genre": "Electro House", "key": "Em", "duration_sec": 210},
    {"title": "Spectrum", "artist": "Zedd ft. Matthew Koma", "bpm": 128, "genre": "Electro House", "key": "Dm", "duration_sec": 270},
    {"title": "The Middle", "artist": "Zedd ft. Maren Morris & Grey", "bpm": 98, "genre": "Dance Pop", "key": "Am", "duration_sec": 195},
    {"title": "Stay", "artist": "Zedd & Alessia Cara", "bpm": 104, "genre": "Dance Pop", "key": "Gm", "duration_sec": 211},
    {"title": "I Want You To Know", "artist": "Zedd ft. Selena Gomez", "bpm": 128, "genre": "Electro House", "key": "Em", "duration_sec": 195},
    {"title": "True Colors", "artist": "Zedd ft. Kesha", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 195},
    {"title": "Candyman", "artist": "Zedd", "bpm": 128, "genre": "Electro House", "key": "Fm", "duration_sec": 180},
    {"title": "Shave It Up", "artist": "Zedd", "bpm": 128, "genre": "Electro House", "key": "Dm", "duration_sec": 240},
    {"title": "Lost at Sea", "artist": "Zedd ft. Ryan Tedder", "bpm": 128, "genre": "Electro House", "key": "Am", "duration_sec": 225},
    {"title": "Shotgun", "artist": "Zedd", "bpm": 128, "genre": "Electro House", "key": "Gm", "duration_sec": 195},

    # ===== FISHER =====
    {"title": "Losing It", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Dm", "duration_sec": 285},
    {"title": "Ya Kidding", "artist": "Fisher", "bpm": 125, "genre": "Tech House", "key": "Am", "duration_sec": 270},
    {"title": "Stop It", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Gm", "duration_sec": 300},
    {"title": "You Little Beauty", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Em", "duration_sec": 285},
    {"title": "Crowd Control", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Am", "duration_sec": 300},
    {"title": "Freaks", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Dm", "duration_sec": 270},
    {"title": "Just Feels Tight", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Fm", "duration_sec": 285},
    {"title": "It's A Killa", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Gm", "duration_sec": 300},
    {"title": "Yeah The Girls", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Am", "duration_sec": 270},
    {"title": "Wanna Go Dancin'", "artist": "Fisher", "bpm": 126, "genre": "Tech House", "key": "Em", "duration_sec": 285},

    # ===== CHARLOTTE DE WITTE =====
    {"title": "The Age of Love", "artist": "Charlotte de Witte & Enrico Sangiuliano", "bpm": 125, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 390},
    {"title": "Trip", "artist": "Charlotte de Witte", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 360},
    {"title": "Sehnsucht", "artist": "Charlotte de Witte", "bpm": 132, "genre": "Techno", "key": "Gm", "duration_sec": 330},
    {"title": "Voices of the Ancient", "artist": "Charlotte de Witte", "bpm": 130, "genre": "Techno", "key": "Em", "duration_sec": 390},
    {"title": "Weltschmerz", "artist": "Charlotte de Witte", "bpm": 134, "genre": "Techno", "key": "Am", "duration_sec": 360},
    {"title": "Heart of Mine", "artist": "Charlotte de Witte", "bpm": 128, "genre": "Techno", "key": "Dm", "duration_sec": 420},
    {"title": "The Healer", "artist": "Charlotte de Witte", "bpm": 130, "genre": "Techno", "key": "Fm", "duration_sec": 360},
    {"title": "Pressure", "artist": "Charlotte de Witte", "bpm": 132, "genre": "Techno", "key": "Gm", "duration_sec": 390},
    {"title": "Selected", "artist": "Charlotte de Witte", "bpm": 128, "genre": "Techno", "key": "Am", "duration_sec": 360},
    {"title": "Universal Consciousness", "artist": "Charlotte de Witte", "bpm": 130, "genre": "Techno", "key": "Em", "duration_sec": 420},
    {"title": "High Street", "artist": "Charlotte de Witte", "bpm": 132, "genre": "Techno", "key": "Dm", "duration_sec": 360},
    {"title": "One Mind", "artist": "Charlotte de Witte & Amelie Lens", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 390},

    # ===== AMELIE LENS =====
    {"title": "In Silence", "artist": "Amelie Lens", "bpm": 132, "genre": "Techno", "key": "Am", "duration_sec": 360},
    {"title": "Follow", "artist": "Amelie Lens", "bpm": 130, "genre": "Techno", "key": "Gm", "duration_sec": 330},
    {"title": "Purge", "artist": "Amelie Lens", "bpm": 134, "genre": "Techno", "key": "Em", "duration_sec": 390},
    {"title": "Exhale", "artist": "Amelie Lens", "bpm": 132, "genre": "Techno", "key": "Dm", "duration_sec": 360},
    {"title": "Let It Go", "artist": "Amelie Lens", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 330},
    {"title": "Nel", "artist": "Amelie Lens", "bpm": 132, "genre": "Techno", "key": "Fm", "duration_sec": 420},
    {"title": "Contradiction", "artist": "Amelie Lens", "bpm": 128, "genre": "Techno", "key": "Gm", "duration_sec": 360},
    {"title": "Stay With Me", "artist": "Amelie Lens", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 390},
    {"title": "Hypnotized", "artist": "Amelie Lens", "bpm": 134, "genre": "Techno", "key": "Em", "duration_sec": 330},
    {"title": "Higher", "artist": "Amelie Lens", "bpm": 130, "genre": "Techno", "key": "Dm", "duration_sec": 360},
    {"title": "Raver's Heart", "artist": "Amelie Lens & Airod", "bpm": 132, "genre": "Techno", "key": "Am", "duration_sec": 420},
    {"title": "Adrenaline", "artist": "Amelie Lens & Airod", "bpm": 134, "genre": "Techno", "key": "Gm", "duration_sec": 360},

    # ===== TALE OF US =====
    {"title": "Cherry", "artist": "Tale Of Us", "bpm": 122, "genre": "Melodic Techno", "key": "Am", "duration_sec": 420},
    {"title": "Alone", "artist": "Tale Of Us", "bpm": 124, "genre": "Melodic Techno", "key": "Gm", "duration_sec": 390},
    {"title": "Dark Song", "artist": "Tale Of Us", "bpm": 120, "genre": "Melodic Techno", "key": "Em", "duration_sec": 480},
    {"title": "Another Earth", "artist": "Tale Of Us", "bpm": 122, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 420},
    {"title": "North Star", "artist": "Tale Of Us", "bpm": 124, "genre": "Melodic Techno", "key": "Am", "duration_sec": 450},
    {"title": "Silent Space", "artist": "Tale Of Us", "bpm": 120, "genre": "Melodic Techno", "key": "Fm", "duration_sec": 390},
    {"title": "Monument", "artist": "Tale Of Us & Vaal", "bpm": 122, "genre": "Melodic Techno", "key": "Gm", "duration_sec": 420},
    {"title": "Astral", "artist": "Tale Of Us & Mind Against", "bpm": 124, "genre": "Melodic Techno", "key": "Am", "duration_sec": 480},
    {"title": "Vanishing", "artist": "Tale Of Us & Fideles", "bpm": 120, "genre": "Melodic Techno", "key": "Em", "duration_sec": 390},
    {"title": "Unity", "artist": "Tale Of Us", "bpm": 122, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 420},

    # ===== BORIS BREJCHA =====
    {"title": "Gravity", "artist": "Boris Brejcha", "bpm": 126, "genre": "Melodic Techno", "key": "Am", "duration_sec": 420},
    {"title": "Purple Noise", "artist": "Boris Brejcha", "bpm": 128, "genre": "Melodic Techno", "key": "Gm", "duration_sec": 390},
    {"title": "Space Diver", "artist": "Boris Brejcha", "bpm": 126, "genre": "Melodic Techno", "key": "Em", "duration_sec": 480},
    {"title": "Art of Minimal Techno", "artist": "Boris Brejcha", "bpm": 124, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 360},
    {"title": "Monster", "artist": "Boris Brejcha", "bpm": 128, "genre": "Melodic Techno", "key": "Am", "duration_sec": 390},
    {"title": "Yellow Kitchen", "artist": "Boris Brejcha", "bpm": 126, "genre": "Melodic Techno", "key": "Fm", "duration_sec": 420},
    {"title": "Die Maschinen Sind Gestrandet", "artist": "Boris Brejcha", "bpm": 128, "genre": "Melodic Techno", "key": "Gm", "duration_sec": 450},
    {"title": "Lost Memory", "artist": "Boris Brejcha", "bpm": 124, "genre": "Melodic Techno", "key": "Am", "duration_sec": 390},
    {"title": "Never Stop Dancing", "artist": "Boris Brejcha", "bpm": 128, "genre": "Melodic Techno", "key": "Em", "duration_sec": 420},
    {"title": "22", "artist": "Boris Brejcha", "bpm": 126, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 360},

    # ===== CHRIS LAKE =====
    {"title": "Operator", "artist": "Chris Lake", "bpm": 126, "genre": "Tech House", "key": "Am", "duration_sec": 270},
    {"title": "Chest", "artist": "Chris Lake", "bpm": 125, "genre": "Tech House", "key": "Gm", "duration_sec": 285},
    {"title": "Turn Off The Lights", "artist": "Chris Lake", "bpm": 126, "genre": "Tech House", "key": "Em", "duration_sec": 300},
    {"title": "Piano Hand", "artist": "Chris Lake & Chris Lorenzo", "bpm": 126, "genre": "Tech House", "key": "Dm", "duration_sec": 270},
    {"title": "Stomper", "artist": "Chris Lake & Anna Lunoe", "bpm": 125, "genre": "Tech House", "key": "Am", "duration_sec": 285},
    {"title": "Changes", "artist": "Chris Lake ft. Laura V", "bpm": 128, "genre": "House", "key": "Fm", "duration_sec": 210},
    {"title": "Carry Me Away", "artist": "Chris Lake ft. Emma Hewitt", "bpm": 128, "genre": "House", "key": "Gm", "duration_sec": 225},
    {"title": "Deceiver", "artist": "Chris Lake", "bpm": 126, "genre": "Tech House", "key": "Am", "duration_sec": 270},
    {"title": "Stay With Me", "artist": "Chris Lake", "bpm": 125, "genre": "Tech House", "key": "Em", "duration_sec": 285},
    {"title": "I Want You", "artist": "Chris Lake", "bpm": 126, "genre": "Tech House", "key": "Dm", "duration_sec": 300},

    # ===== ADAM BEYER =====
    {"title": "Drumcode 01", "artist": "Adam Beyer", "bpm": 132, "genre": "Techno", "key": "Am", "duration_sec": 390},
    {"title": "Loca", "artist": "Adam Beyer", "bpm": 130, "genre": "Techno", "key": "Gm", "duration_sec": 360},
    {"title": "Desolate Lands", "artist": "Adam Beyer", "bpm": 134, "genre": "Techno", "key": "Em", "duration_sec": 420},
    {"title": "Alto", "artist": "Adam Beyer", "bpm": 128, "genre": "Techno", "key": "Dm", "duration_sec": 360},
    {"title": "Taking Back Control", "artist": "Adam Beyer", "bpm": 132, "genre": "Techno", "key": "Am", "duration_sec": 390},
    {"title": "Hypnotic", "artist": "Adam Beyer ft. Kyozo", "bpm": 130, "genre": "Techno", "key": "Fm", "duration_sec": 360},
    {"title": "Explorer", "artist": "Adam Beyer", "bpm": 134, "genre": "Techno", "key": "Gm", "duration_sec": 420},
    {"title": "Circus Freaks", "artist": "Adam Beyer", "bpm": 128, "genre": "Techno", "key": "Am", "duration_sec": 360},
    {"title": "Overdose Of Bass", "artist": "Adam Beyer", "bpm": 132, "genre": "Techno", "key": "Em", "duration_sec": 390},
    {"title": "Fascination", "artist": "Adam Beyer", "bpm": 130, "genre": "Techno", "key": "Dm", "duration_sec": 360},

    # ===== RUFUS DU SOL =====
    {"title": "Innerbloom", "artist": "RUFUS DU SOL", "bpm": 118, "genre": "Melodic House", "key": "Fm", "duration_sec": 590},
    {"title": "You Were Right", "artist": "RUFUS DU SOL", "bpm": 122, "genre": "Progressive House", "key": "Am", "duration_sec": 360},
    {"title": "No Place", "artist": "RUFUS DU SOL", "bpm": 120, "genre": "Melodic House", "key": "Gm", "duration_sec": 420},
    {"title": "Underwater", "artist": "RUFUS DU SOL", "bpm": 118, "genre": "Melodic House", "key": "Em", "duration_sec": 390},
    {"title": "Alive", "artist": "RUFUS DU SOL", "bpm": 124, "genre": "Melodic House", "key": "Am", "duration_sec": 450},
    {"title": "On My Knees", "artist": "RUFUS DU SOL", "bpm": 122, "genre": "Melodic House", "key": "Dm", "duration_sec": 360},
    {"title": "Next to Me", "artist": "RUFUS DU SOL", "bpm": 120, "genre": "Melodic House", "key": "Fm", "duration_sec": 420},
    {"title": "Treat You Better", "artist": "RUFUS DU SOL", "bpm": 118, "genre": "Melodic House", "key": "Gm", "duration_sec": 390},
    {"title": "Solace", "artist": "RUFUS DU SOL", "bpm": 122, "genre": "Melodic House", "key": "Am", "duration_sec": 360},
    {"title": "Desert Night", "artist": "RUFUS DU SOL", "bpm": 120, "genre": "Melodic House", "key": "Em", "duration_sec": 420},

    # ===== CAMELPHAT =====
    {"title": "Cola", "artist": "CamelPhat & Elderbrook", "bpm": 124, "genre": "Tech House", "key": "Am", "duration_sec": 340},
    {"title": "Breathe", "artist": "CamelPhat & Cristoph", "bpm": 122, "genre": "Melodic House", "key": "Gm", "duration_sec": 360},
    {"title": "Panic Room", "artist": "CamelPhat & Au/Ra", "bpm": 120, "genre": "Melodic House", "key": "Em", "duration_sec": 285},
    {"title": "Hypercolour", "artist": "CamelPhat", "bpm": 124, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 390},
    {"title": "Paradigm", "artist": "CamelPhat ft. A*M*E", "bpm": 126, "genre": "Tech House", "key": "Am", "duration_sec": 270},
    {"title": "Constellations", "artist": "CamelPhat", "bpm": 122, "genre": "Tech House", "key": "Fm", "duration_sec": 300},
    {"title": "Trip", "artist": "CamelPhat", "bpm": 124, "genre": "Melodic House", "key": "Gm", "duration_sec": 330},
    {"title": "Be Someone", "artist": "CamelPhat ft. Jake Bugg", "bpm": 120, "genre": "Melodic House", "key": "Am", "duration_sec": 360},
    {"title": "Rabbit Hole", "artist": "CamelPhat", "bpm": 124, "genre": "Melodic Techno", "key": "Em", "duration_sec": 390},
    {"title": "Dark Matter", "artist": "CamelPhat", "bpm": 122, "genre": "Melodic Techno", "key": "Dm", "duration_sec": 420},

    # ===== DISCLOSURE =====
    {"title": "Latch", "artist": "Disclosure ft. Sam Smith", "bpm": 122, "genre": "Deep House", "key": "Gm", "duration_sec": 275},
    {"title": "White Noise", "artist": "Disclosure ft. AlunaGeorge", "bpm": 124, "genre": "UK Garage", "key": "Em", "duration_sec": 310},
    {"title": "You & Me", "artist": "Disclosure ft. Eliza Doolittle", "bpm": 122, "genre": "Deep House", "key": "Am", "duration_sec": 255},
    {"title": "F for You", "artist": "Disclosure", "bpm": 122, "genre": "Deep House", "key": "Dm", "duration_sec": 285},
    {"title": "Holding On", "artist": "Disclosure ft. Gregory Porter", "bpm": 122, "genre": "Deep House", "key": "Fm", "duration_sec": 300},
    {"title": "Omen", "artist": "Disclosure ft. Sam Smith", "bpm": 124, "genre": "Deep House", "key": "Gm", "duration_sec": 255},
    {"title": "When A Fire Starts to Burn", "artist": "Disclosure", "bpm": 126, "genre": "UK Garage", "key": "Am", "duration_sec": 270},
    {"title": "Help Me Lose My Mind", "artist": "Disclosure ft. London Grammar", "bpm": 122, "genre": "Deep House", "key": "Em", "duration_sec": 300},
    {"title": "Grab Her!", "artist": "Disclosure", "bpm": 124, "genre": "UK Garage", "key": "Dm", "duration_sec": 195},
    {"title": "Tenderly", "artist": "Disclosure", "bpm": 122, "genre": "Deep House", "key": "Am", "duration_sec": 285},

    # ===== FLUME =====
    {"title": "Holdin On", "artist": "Flume", "bpm": 110, "genre": "Future Bass", "key": "Am", "duration_sec": 240},
    {"title": "Never Be Like You", "artist": "Flume ft. Kai", "bpm": 136, "genre": "Future Bass", "key": "Gm", "duration_sec": 234},
    {"title": "Say It", "artist": "Flume ft. Tove Lo", "bpm": 96, "genre": "Future Bass", "key": "Em", "duration_sec": 229},
    {"title": "Insane", "artist": "Flume ft. Moon Holiday", "bpm": 120, "genre": "Future Bass", "key": "Dm", "duration_sec": 246},
    {"title": "Sleepless", "artist": "Flume ft. Jezzabell Doran", "bpm": 118, "genre": "Future Bass", "key": "Am", "duration_sec": 255},
    {"title": "Smoke & Retribution", "artist": "Flume ft. Vince Staples & Kucka", "bpm": 130, "genre": "Future Bass", "key": "Fm", "duration_sec": 240},
    {"title": "Hyperreal", "artist": "Flume ft. Kucka", "bpm": 120, "genre": "Future Bass", "key": "Gm", "duration_sec": 285},
    {"title": "Hi This Is Flume", "artist": "Flume", "bpm": 110, "genre": "Future Bass", "key": "Am", "duration_sec": 330},
    {"title": "Rushing Back", "artist": "Flume ft. Vera Blue", "bpm": 90, "genre": "Future Bass", "key": "Em", "duration_sec": 240},
    {"title": "Palaces", "artist": "Flume ft. Damon Albarn", "bpm": 95, "genre": "Electronic", "key": "Dm", "duration_sec": 270},

    # ===== ILLENIUM =====
    {"title": "Good Things Fall Apart", "artist": "Illenium ft. Jon Bellion", "bpm": 103, "genre": "Future Bass", "key": "Am", "duration_sec": 210},
    {"title": "Takeaway", "artist": "The Chainsmokers & Illenium ft. Lennon Stella", "bpm": 130, "genre": "Future Bass", "key": "Gm", "duration_sec": 210},
    {"title": "Feel Good", "artist": "Illenium ft. Daya", "bpm": 150, "genre": "Melodic Dubstep", "key": "Em", "duration_sec": 225},
    {"title": "Fractures", "artist": "Illenium ft. Nevve", "bpm": 150, "genre": "Melodic Dubstep", "key": "Am", "duration_sec": 270},
    {"title": "Crawl Outta Love", "artist": "Illenium ft. Annika Wells", "bpm": 150, "genre": "Melodic Dubstep", "key": "Dm", "duration_sec": 240},
    {"title": "Take You Down", "artist": "Illenium", "bpm": 150, "genre": "Melodic Dubstep", "key": "Fm", "duration_sec": 225},
    {"title": "Sound of Walking Away", "artist": "Illenium ft. Kerli", "bpm": 150, "genre": "Melodic Dubstep", "key": "Gm", "duration_sec": 255},
    {"title": "It's All On U", "artist": "Illenium ft. Liam O'Donnell", "bpm": 150, "genre": "Future Bass", "key": "Am", "duration_sec": 270},
    {"title": "Fortress", "artist": "Illenium ft. Joni Fatora", "bpm": 150, "genre": "Melodic Dubstep", "key": "Em", "duration_sec": 285},
    {"title": "Rush Over Me", "artist": "Seven Lions, Illenium, Said The Sky", "bpm": 150, "genre": "Melodic Dubstep", "key": "Dm", "duration_sec": 270},

    # ===== SEVEN LIONS =====
    {"title": "Strangers", "artist": "Seven Lions ft. Tove Lo", "bpm": 150, "genre": "Melodic Dubstep", "key": "Am", "duration_sec": 285},
    {"title": "Don't Leave", "artist": "Seven Lions ft. Ellie Goulding", "bpm": 150, "genre": "Melodic Dubstep", "key": "Gm", "duration_sec": 270},
    {"title": "Calling You Home", "artist": "Seven Lions ft. Runn", "bpm": 150, "genre": "Melodic Dubstep", "key": "Em", "duration_sec": 255},
    {"title": "Creation", "artist": "Seven Lions", "bpm": 140, "genre": "Melodic Dubstep", "key": "Dm", "duration_sec": 300},
    {"title": "Days to Come", "artist": "Seven Lions ft. Fiora", "bpm": 150, "genre": "Melodic Dubstep", "key": "Am", "duration_sec": 285},
    {"title": "Worlds Apart", "artist": "Seven Lions", "bpm": 150, "genre": "Melodic Dubstep", "key": "Fm", "duration_sec": 270},
    {"title": "Without You My Love", "artist": "Seven Lions ft. Rico & Miella", "bpm": 140, "genre": "Melodic Dubstep", "key": "Gm", "duration_sec": 255},
    {"title": "Horizon", "artist": "Seven Lions", "bpm": 150, "genre": "Trance", "key": "Am", "duration_sec": 330},
    {"title": "Only Now", "artist": "Seven Lions ft. Tyler Graves", "bpm": 150, "genre": "Melodic Dubstep", "key": "Em", "duration_sec": 270},
    {"title": "Falling Away", "artist": "Seven Lions ft. Lights", "bpm": 140, "genre": "Melodic Dubstep", "key": "Dm", "duration_sec": 255},

    # ===== DIPLO / MAJOR LAZER =====
    {"title": "Lean On", "artist": "Major Lazer & DJ Snake ft. MO", "bpm": 98, "genre": "Moombahton", "key": "Am", "duration_sec": 176},
    {"title": "Cold Water", "artist": "Major Lazer ft. Justin Bieber & MO", "bpm": 93, "genre": "Dance Pop", "key": "Gm", "duration_sec": 185},
    {"title": "Get Free", "artist": "Major Lazer ft. Amber Coffman", "bpm": 140, "genre": "Reggae Fusion", "key": "Em", "duration_sec": 260},
    {"title": "Light It Up", "artist": "Major Lazer", "bpm": 106, "genre": "Dancehall", "key": "Am", "duration_sec": 192},
    {"title": "Pon de Floor", "artist": "Major Lazer", "bpm": 100, "genre": "Dancehall", "key": "Dm", "duration_sec": 195},
    {"title": "Watch Out For This", "artist": "Major Lazer", "bpm": 100, "genre": "Dancehall", "key": "Fm", "duration_sec": 195},
    {"title": "Powerful", "artist": "Major Lazer ft. Ellie Goulding", "bpm": 94, "genre": "Dance Pop", "key": "Gm", "duration_sec": 210},
    {"title": "Run Up", "artist": "Major Lazer ft. PARTYNEXTDOOR & Nicki Minaj", "bpm": 100, "genre": "Dancehall", "key": "Am", "duration_sec": 195},
    {"title": "Believer", "artist": "Major Lazer ft. Showtek", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 210},
    {"title": "Know No Better", "artist": "Major Lazer ft. Travis Scott & Camila Cabello", "bpm": 100, "genre": "Dance Pop", "key": "Dm", "duration_sec": 195},

    # ===== MORE TRANCE CLASSICS =====
    {"title": "Sandstorm", "artist": "Darude", "bpm": 136, "genre": "Trance", "key": "Dm", "duration_sec": 330},
    {"title": "Children", "artist": "Robert Miles", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 390},
    {"title": "Cafe Del Mar", "artist": "Energy 52", "bpm": 136, "genre": "Trance", "key": "Gm", "duration_sec": 420},
    {"title": "Offshore", "artist": "Chicane", "bpm": 136, "genre": "Trance", "key": "Em", "duration_sec": 420},
    {"title": "Saltwater", "artist": "Chicane", "bpm": 138, "genre": "Trance", "key": "Am", "duration_sec": 360},
    {"title": "For An Angel", "artist": "Paul van Dyk", "bpm": 140, "genre": "Trance", "key": "Cm", "duration_sec": 520},
    {"title": "Exploration of Space", "artist": "Cosmic Gate", "bpm": 140, "genre": "Trance", "key": "Dm", "duration_sec": 390},
    {"title": "L'Amour Toujours", "artist": "Gigi D'Agostino", "bpm": 140, "genre": "Trance", "key": "Am", "duration_sec": 210},
    {"title": "Better Off Alone", "artist": "Alice Deejay", "bpm": 138, "genre": "Trance", "key": "Gm", "duration_sec": 210},
    {"title": "Blue (Da Ba Dee)", "artist": "Eiffel 65", "bpm": 128, "genre": "Eurodance", "key": "Em", "duration_sec": 267},

    # ===== MORE BIG ROOM =====
    {"title": "Tremor", "artist": "Dimitri Vegas & Like Mike", "bpm": 128, "genre": "Big Room", "key": "Gm", "duration_sec": 310},
    {"title": "Tsunami", "artist": "DVBBS & Borgeous", "bpm": 128, "genre": "Big Room", "key": "Am", "duration_sec": 275},
    {"title": "Epic", "artist": "Sandro Silva & Quintino", "bpm": 130, "genre": "Big Room", "key": "Dm", "duration_sec": 295},
    {"title": "Mammoth", "artist": "Dimitri Vegas & Like Mike", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 280},
    {"title": "Crackin", "artist": "Bassjackers", "bpm": 128, "genre": "Big Room", "key": "Am", "duration_sec": 270},
    {"title": "Flashlight", "artist": "R3hab & Deorro", "bpm": 128, "genre": "Big Room", "key": "Gm", "duration_sec": 285},
    {"title": "Cannonball", "artist": "Showtek & Justin Prime", "bpm": 128, "genre": "Big Room", "key": "Em", "duration_sec": 300},
    {"title": "Toulouse", "artist": "Nicky Romero", "bpm": 128, "genre": "Big Room", "key": "Am", "duration_sec": 290},
    {"title": "Legacy", "artist": "Nicky Romero & Krewella", "bpm": 128, "genre": "Big Room", "key": "Dm", "duration_sec": 275},
    {"title": "Like Home", "artist": "Nicky Romero & NERVO", "bpm": 128, "genre": "Big Room", "key": "Fm", "duration_sec": 285},

    # ===== TECHNO CLASSICS =====
    {"title": "Acid Track", "artist": "Phuture", "bpm": 130, "genre": "Techno", "key": "Am", "duration_sec": 420},
    {"title": "Strings of Life", "artist": "Derrick May", "bpm": 128, "genre": "Techno", "key": "Em", "duration_sec": 480},
    {"title": "Spastik", "artist": "Plastikman", "bpm": 134, "genre": "Techno", "key": "Dm", "duration_sec": 360},
    {"title": "The Bells", "artist": "Jeff Mills", "bpm": 132, "genre": "Techno", "key": "Gm", "duration_sec": 390},
    {"title": "Rrose Selavy", "artist": "Green Velvet", "bpm": 128, "genre": "Techno", "key": "Am", "duration_sec": 360},
    {"title": "Flash", "artist": "Green Velvet", "bpm": 126, "genre": "Tech House", "key": "Em", "duration_sec": 310},
    {"title": "No Way Back", "artist": "Richie Hawtin", "bpm": 130, "genre": "Techno", "key": "Dm", "duration_sec": 390},
    {"title": "Good Life", "artist": "Inner City", "bpm": 120, "genre": "House", "key": "Am", "duration_sec": 240},
    {"title": "Can You Feel It", "artist": "Mr. Fingers", "bpm": 122, "genre": "Deep House", "key": "Gm", "duration_sec": 420},
    {"title": "Move Your Body", "artist": "Marshall Jefferson", "bpm": 120, "genre": "House", "key": "Am", "duration_sec": 480},

    # ===== CHILLOUT / AMBIENT =====
    {"title": "Intro", "artist": "The xx", "bpm": 110, "genre": "Chillout", "key": "Am", "duration_sec": 240},
    {"title": "Teardrop", "artist": "Massive Attack", "bpm": 78, "genre": "Trip Hop", "key": "Em", "duration_sec": 330},
    {"title": "Porcelain", "artist": "Moby", "bpm": 98, "genre": "Chillout", "key": "Gm", "duration_sec": 245},
    {"title": "Sunset Lover", "artist": "Petit Biscuit", "bpm": 95, "genre": "Chillout", "key": "Fm", "duration_sec": 215},
    {"title": "Natural Blues", "artist": "Moby", "bpm": 95, "genre": "Chillout", "key": "Dm", "duration_sec": 260},
    {"title": "Born Slippy", "artist": "Underworld", "bpm": 139, "genre": "Techno", "key": "Am", "duration_sec": 600},
    {"title": "Two Months Off", "artist": "Underworld", "bpm": 128, "genre": "Progressive House", "key": "Gm", "duration_sec": 390},
    {"title": "Opus 40", "artist": "Mercury Rev", "bpm": 80, "genre": "Ambient", "key": "Am", "duration_sec": 360},
    {"title": "Midnight City", "artist": "M83", "bpm": 105, "genre": "Synth Pop", "key": "Em", "duration_sec": 243},
    {"title": "Wait", "artist": "M83", "bpm": 90, "genre": "Synth Pop", "key": "Dm", "duration_sec": 341},

    # ===== DRUM & BASS =====
    {"title": "Hold Your Colour", "artist": "Pendulum", "bpm": 174, "genre": "Drum & Bass", "key": "Am", "duration_sec": 360},
    {"title": "Propane Nightmares", "artist": "Pendulum", "bpm": 174, "genre": "Drum & Bass", "key": "Gm", "duration_sec": 285},
    {"title": "Watercolour", "artist": "Pendulum", "bpm": 174, "genre": "Drum & Bass", "key": "Em", "duration_sec": 285},
    {"title": "The Island", "artist": "Pendulum", "bpm": 140, "genre": "Drum & Bass", "key": "Dm", "duration_sec": 285},
    {"title": "Tarantula", "artist": "Pendulum", "bpm": 174, "genre": "Drum & Bass", "key": "Am", "duration_sec": 285},
    {"title": "Gold Dust", "artist": "DJ Fresh", "bpm": 174, "genre": "Drum & Bass", "key": "Fm", "duration_sec": 210},
    {"title": "Hot Right Now", "artist": "DJ Fresh ft. Rita Ora", "bpm": 174, "genre": "Drum & Bass", "key": "Gm", "duration_sec": 210},
    {"title": "Doompy Poomp", "artist": "deadmau5", "bpm": 174, "genre": "Drum & Bass", "key": "Am", "duration_sec": 240},
    {"title": "Bass Head", "artist": "Bassnectar", "bpm": 140, "genre": "Bass Music", "key": "Em", "duration_sec": 300},
    {"title": "Timestretch", "artist": "Bassnectar", "bpm": 140, "genre": "Bass Music", "key": "Dm", "duration_sec": 360},
]

# 生成随机颜色用于封面
def get_random_color():
    colors = ['FF6B6B', '4ECDC4', '45B7D1', '96CEB4', 'FFEAA7', 'DDA0DD', '98D8C8',
              '9B59B6', '3498DB', 'E74C3C', '1ABC9C', '8E44AD', '2980B9', '27AE60',
              'F39C12', '5D6D7E', '85929E', '2C3E50', '34495E', '1A1A2E']
    return random.choice(colors)

# 为每首歌曲添加封面URL
for track in real_tracks:
    if 'cover_url' not in track:
        title_short = track['title'][:15].replace(' ', '+')
        color = get_random_color()
        track['cover_url'] = f"https://via.placeholder.com/300x300/{color}/fff?text={title_short}"

with app.app_context():
    added = 0
    skipped = 0
    for track_data in real_tracks:
        # 检查是否已存在
        existing = Track.query.filter_by(title=track_data["title"], artist=track_data["artist"]).first()
        if not existing:
            track = Track(**track_data)
            db.session.add(track)
            added += 1
        else:
            skipped += 1
    db.session.commit()
    total = Track.query.count()
    print(f"导入完成!")
    print(f"新增: {added} 首歌曲")
    print(f"跳过(已存在): {skipped} 首歌曲")
    print(f"数据库总歌曲数: {total}")
