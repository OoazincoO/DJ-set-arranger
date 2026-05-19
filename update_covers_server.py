"""使用预获取的封面URL更新数据库"""
import json
from app import create_app
from extensions import db
from models import Track

app = create_app()

# 预获取的封面映射
cover_mapping = {
  "deadmau5|||strobe": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/f7/24/19/f724197c-b6b7-b2ad-94a9-06b2f5f95455/617465226458.jpg/600x600bb.jpg",
  "deadmau5|||ghosts n stuff": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/c1/90/35/c19035ef-7547-05d0-b284-98f055dde14b/617465219856.jpg/600x600bb.jpg",
  "deadmau5|||i remember": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/62/64/f2/6264f273-04fa-d05d-a067-22a7ca9bbeec/617465186851.jpg/600x600bb.jpg",
  "deadmau5|||raise your weapon": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/8b/d2/14/8bd21495-6ed2-ae2d-5b00-e93f4a5eaf57/617465272752.jpg/600x600bb.jpg",
  "deadmau5|||some chords": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/f0/47/e0/f047e076-ce02-917c-cbf6-5ecd9af97859/617465272059.jpg/600x600bb.jpg",
  "deadmau5|||the veldt": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/8a/6e/5b/8a6e5be3-1c1d-5b15-750d-8de652915c71/617465759055.jpg/600x600bb.jpg",
  "deadmau5|||faxing berlin": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/43/95/87/439587b4-7b73-67bd-1767-9311fa086d95/cover.jpg/600x600bb.jpg",
  "deadmau5|||not exactly": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/62/64/f2/6264f273-04fa-d05d-a067-22a7ca9bbeec/617465186851.jpg/600x600bb.jpg",
  "deadmau5|||aural psynapse": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/e1/fd/30/e1fd30f7-5e6b-22e6-33ea-ed7c31ac7a6e/617465013379.jpg/600x600bb.jpg",
  "deadmau5|||right this second": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/17/65/93/176593fa-d668-b58f-b3d3-11947787328e/617465272158.jpg/600x600bb.jpg",
  "deadmau5|||cthulhu sleeps": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/05/b5/39/05b53989-4d8e-152b-2a59-1dfc402d2c27/617465251856.jpg/600x600bb.jpg",
  "deadmau5|||arguru": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/62/64/f2/6264f273-04fa-d05d-a067-22a7ca9bbeec/617465186851.jpg/600x600bb.jpg",
  "tiesto|||adagio for strings": "https://is1-ssl.mzstatic.com/image/thumb/Features125/v4/31/fb/47/31fb47be-6c25-08bf-c501-36bf6f436739/dj.xbgrvowk.jpg/600x600bb.jpg",
  "tiesto|||red lights": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/9e/63/2e/9e632ec7-2a63-5ea2-ab24-f02eb11f5d30/00602537844234.rgb.jpg/600x600bb.jpg",
  "tiesto|||traffic": "https://is1-ssl.mzstatic.com/image/thumb/Features125/v4/31/fb/47/31fb47be-6c25-08bf-c501-36bf6f436739/dj.xbgrvowk.jpg/600x600bb.jpg",
  "tiesto|||elements of life": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/05/aa/43/05aa43fb-cea3-3f79-95f6-61e1486f03b2/8715197080729.jpg/600x600bb.jpg",
  "tiesto|||lethal industry": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/23/a3/eb/23a3ebbe-7cdd-d8b8-7675-28aab1b9861e/8718522112799.png/600x600bb.jpg",
  "tiesto|||the business": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/cf/81/b8/cf81b800-bc37-cb1e-008e-a1211ce21d19/075679803429.jpg/600x600bb.jpg",
  "tiesto|||wasted": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/9e/63/2e/9e632ec7-2a63-5ea2-ab24-f02eb11f5d30/00602537844234.rgb.jpg/600x600bb.jpg",
  "tiesto|||secrets": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/3f/39/26/3f39260d-2183-d0b5-9532-dd8bc69f2afa/00602547380845.rgb.jpg/600x600bb.jpg",
  "armin van buuren|||this is what it feels like": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/94/2f/7d/942f7db7-8f8f-9cd3-49ea-f0b31b421dde/8718522020803.png/600x600bb.jpg",
  "armin van buuren|||blah blah blah": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/bd/d2/dd/bdd2dd9e-c9a0-43d0-1cef-6b238c82fd4c/8718522270444.png/600x600bb.jpg",
  "armin van buuren|||communication": "https://is1-ssl.mzstatic.com/image/thumb/Features/v4/69/22/93/692293df-6b0c-cbe8-b5ea-805d2a5d0fb7/dj.vqjmcigh.jpg/600x600bb.jpg",
  "armin van buuren|||in and out of love": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/a6/27/02/a6270273-796d-de56-03b6-59e47018911c/8717306944908.png/600x600bb.jpg",
  "armin van buuren|||ping pong": "https://is1-ssl.mzstatic.com/image/thumb/Music2/v4/f5/b9/de/f5b9dead-7932-caf2-f5ea-69bb204e8200/8718522040771.jpg/600x600bb.jpg",
  "armin van buuren|||shivers": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/16/d2/a1/16d2a1e5-e7e4-00b6-954d-49fdd629a057/mzi.ehxjkgcy.tif/600x600bb.jpg",
  "david guetta|||titanium": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/99/b4/7b/99b47bd8-2b22-e1ef-2e60-c5147f27a861/dj.thrvmjqj.jpg/600x600bb.jpg",
  "david guetta|||without you": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/99/b4/7b/99b47bd8-2b22-e1ef-2e60-c5147f27a861/dj.thrvmjqj.jpg/600x600bb.jpg",
  "david guetta|||when love takes over": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/0a/0c/4f/0a0c4f12-1489-3bda-ab41-7cb04f181e5f/5099990837951.jpg/600x600bb.jpg",
  "david guetta|||sexy bitch": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/0a/0c/4f/0a0c4f12-1489-3bda-ab41-7cb04f181e5f/5099990837951.jpg/600x600bb.jpg",
  "david guetta|||memories": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/0a/0c/4f/0a0c4f12-1489-3bda-ab41-7cb04f181e5f/5099990837951.jpg/600x600bb.jpg",
  "david guetta|||play hard": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/f6/b9/e2/f6b9e2df-c638-3e4b-c28d-a68b06465758/5099997943051.jpg/600x600bb.jpg",
  "david guetta|||hey mama": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/68/7f/d5/687fd582-2387-5044-a881-0bc4f0697338/825646194315.jpg/600x600bb.jpg",
  "david guetta|||dangerous": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/68/7f/d5/687fd582-2387-5044-a881-0bc4f0697338/825646194315.jpg/600x600bb.jpg",
  "calvin harris|||summer": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/da/50/cc/da50cc80-3515-a38d-369b-0d700ffd249d/886444820448.jpg/600x600bb.jpg",
  "calvin harris|||feel so close": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/15/ba/ec/15baec26-2db7-0abd-4197-76372183a628/mzi.xbpaeiac.jpg/600x600bb.jpg",
  "calvin harris|||this is what you came for": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/59/57/a6/5957a66e-fb10-4065-5739-7c54236339e4/886445857290.jpg/600x600bb.jpg",
  "calvin harris|||how deep is your love": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/04/5c/85/045c85d9-94cb-a9c7-f39b-aa5b7e803c04/dj.dkdebfmh.jpg/600x600bb.jpg",
  "calvin harris|||outside": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/da/50/cc/da50cc80-3515-a38d-369b-0d700ffd249d/886444820448.jpg/600x600bb.jpg",
  "calvin harris|||sweet nothing": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/ab/af/22/abaf2296-ed4d-6da2-c24d-503cfdfa4c1f/0617465356858.jpg/600x600bb.jpg",
  "calvin harris|||we found love": "https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/ac/51/45/ac51452d-c03f-94fb-6f3b-4f18b7beee53/11UMGIM38934.rgb.jpg/600x600bb.jpg",
  "calvin harris|||one kiss": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/91/2a/7b/912a7bdb-c2f6-b887-9392-49728fece0df/886447044360.jpg/600x600bb.jpg",
  "calvin harris|||promises": "https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/95/94/14/9594147f-63c4-92ba-bfd5-74e8199aba51/886447242926.jpg/600x600bb.jpg",
  "martin garrix|||animals": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/6e/1e/f0/6e1ef055-195a-bb73-d5a8-5926058366a5/8712944577525.png/600x600bb.jpg",
  "martin garrix|||scared to be lonely": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/44/46/1f/44461f0c-a949-ce72-0164-704056469fc8/886446328331.jpg/600x600bb.jpg",
  "martin garrix|||high on life": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/58/a2/33/58a23353-b253-405c-b930-d5f3e6b87476/886447232422.jpg/600x600bb.jpg",
  "martin garrix|||in the name of love": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/fc/8a/d2/fc8ad2a2-c75b-c33f-5d1a-070539e647bd/886446028088.jpg/600x600bb.jpg",
  "martin garrix|||forbidden voices": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/b0/28/a7/b028a717-937c-5bdd-43ad-f1b696431cfc/8712944473490.jpg/600x600bb.jpg",
  "martin garrix|||wizard": "https://is1-ssl.mzstatic.com/image/thumb/Music118/v4/8f/66/59/8f6659e9-1337-01e4-64f9-778cbfa42772/8712944448238.jpg/600x600bb.jpg",
  "martin garrix|||ocean": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/f4/26/52/f42652d9-b61d-27d9-5c5f-e2d96090e296/886447147665.jpg/600x600bb.jpg",
  "skrillex|||bangarang": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a3/5b/c9/a35bc94e-e7b4-a5bb-e1c2-b77c8bb50ac2/3700093949012.jpg/600x600bb.jpg",
  "skrillex|||scary monsters and nice sprites": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/33/60/c9/3360c973-0a60-a09e-1f9b-7bdcb1ec4424/791139260015.jpg/600x600bb.jpg",
  "skrillex|||cinema": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/b9/8e/0e/b98e0e1b-6cfe-e5b6-dd5f-3a2d97d1fe0c/dj.ufaybldr.jpg/600x600bb.jpg",
  "skrillex|||first of the year": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/4e/91/6d/4e916d54-23a7-b9f2-3ff1-c42ca7d2f3c8/791139260015.jpg/600x600bb.jpg",
  "skrillex|||summit": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a3/5b/c9/a35bc94e-e7b4-a5bb-e1c2-b77c8bb50ac2/3700093949012.jpg/600x600bb.jpg",
  "skrillex|||kyoto": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a3/5b/c9/a35bc94e-e7b4-a5bb-e1c2-b77c8bb50ac2/3700093949012.jpg/600x600bb.jpg",
  "avicii|||wake me up": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/9d/33/3a/9d333aa6-70f7-ce6a-8fad-28ab27e6c9a9/13UAAIM27579.rgb.jpg/600x600bb.jpg",
  "avicii|||levels": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/67/38/43/67384338-9ed7-fc68-5927-93f1fcf4705d/11UMGIM36900.rgb.jpg/600x600bb.jpg",
  "avicii|||hey brother": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/9d/33/3a/9d333aa6-70f7-ce6a-8fad-28ab27e6c9a9/13UAAIM27579.rgb.jpg/600x600bb.jpg",
  "avicii|||waiting for love": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/83/42/96/83429600-66dc-c3e2-db7b-82e6f1ea49e4/15UMGIM31251.rgb.jpg/600x600bb.jpg",
  "avicii|||the nights": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/29/13/06/29130600-2fc0-5a5f-1ed2-6e75b9914cb0/14UMGIM30168.rgb.jpg/600x600bb.jpg",
  "avicii|||addicted to you": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/9d/33/3a/9d333aa6-70f7-ce6a-8fad-28ab27e6c9a9/13UAAIM27579.rgb.jpg/600x600bb.jpg",
  "avicii|||seek bromance": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/cb/7e/dc/cb7edc82-be2f-a095-7c15-b0f6a1ba9af0/886443509788.jpg/600x600bb.jpg",
  "avicii|||i could be the one": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/41/aa/24/41aa24a2-5bb9-0f5d-dac9-5f4d82e1baa9/5054196218621.jpg/600x600bb.jpg",
  "avicii|||without you": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/d5/a5/5c/d5a55c99-f9b4-ba79-ab49-5107a5c15af7/17UMGIM10099.rgb.jpg/600x600bb.jpg",
  "avicii|||sos": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/0a/37/92/0a3792bd-7dd9-c5ca-bb29-71a11c36d065/19UMGIM31206.rgb.jpg/600x600bb.jpg",
  "swedish house mafia|||don't you worry child": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/c5/6a/38/c56a385e-fa4f-2ece-7a7c-48dad59f8c5f/dj.hpqpvvtr.jpg/600x600bb.jpg",
  "swedish house mafia|||save the world": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/a9/2f/82/a92f82f9-fc78-5ebf-9a1a-e2b7d3e08d15/5099908770554.jpg/600x600bb.jpg",
  "swedish house mafia|||one": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/26/e0/54/26e05451-6b16-b6ba-7dfe-0b3ccdd34a11/00602435405407.rgb.jpg/600x600bb.jpg",
  "swedish house mafia|||greyhound": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/52/ff/a7/52ffa79a-76ec-ea4d-94df-de60073f8b9e/5054196224639.jpg/600x600bb.jpg",
  "swedish house mafia|||antidote": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/a9/2f/82/a92f82f9-fc78-5ebf-9a1a-e2b7d3e08d15/5099908770554.jpg/600x600bb.jpg",
  "swedish house mafia|||moth to a flame": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/71/59/6a/71596ac9-c4dd-e0da-1acf-77a19df2eb2e/21UMGIM94922.rgb.jpg/600x600bb.jpg",
  "eric prydz|||call on me": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/1e/68/0c/1e680ccc-8df4-c79e-b33e-0f5f9ce27903/mzi.xzxnprmt.jpg/600x600bb.jpg",
  "eric prydz|||pjanoo": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/1a/60/07/1a6007ac-d2c4-58fb-a1ee-4dd29b73ff1e/3614599651513.jpg/600x600bb.jpg",
  "eric prydz|||opus": "https://is1-ssl.mzstatic.com/image/thumb/Music118/v4/00/09/fb/0009fb2e-9a01-c5e7-c7fb-2a2dd0a4f6da/886445640724.jpg/600x600bb.jpg",
  "eric prydz|||every day": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/0d/cc/2c/0dcc2c7a-29ec-07b7-efd7-20f1e9e46b01/5054197015151.jpg/600x600bb.jpg",
  "eric prydz|||liberate": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/18/8d/c7/188dc7f9-8b3b-7b94-2b20-0fb4ee4cdc8e/886443899247.jpg/600x600bb.jpg",
  "daft punk|||one more time": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/47/e4/ab/47e4ab96-2e7d-ad46-8dd8-518254216c37/dj.xotsvndl.jpg/600x600bb.jpg",
  "daft punk|||around the world": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/c8/8a/f8/c88af80b-c4f3-0dd6-da0e-d1b5ad34de2f/dj.ipxlbupf.jpg/600x600bb.jpg",
  "daft punk|||get lucky": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/db/8c/7a/db8c7a2c-a842-3c89-c23c-58c82970e498/886443919266.jpg/600x600bb.jpg",
  "daft punk|||harder better faster stronger": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/47/e4/ab/47e4ab96-2e7d-ad46-8dd8-518254216c37/dj.xotsvndl.jpg/600x600bb.jpg",
  "daft punk|||digital love": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/47/e4/ab/47e4ab96-2e7d-ad46-8dd8-518254216c37/dj.xotsvndl.jpg/600x600bb.jpg",
  "daft punk|||something about us": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/47/e4/ab/47e4ab96-2e7d-ad46-8dd8-518254216c37/dj.xotsvndl.jpg/600x600bb.jpg",
  "daft punk|||instant crush": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/db/8c/7a/db8c7a2c-a842-3c89-c23c-58c82970e498/886443919266.jpg/600x600bb.jpg",
  "daft punk|||da funk": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/c8/8a/f8/c88af80b-c4f3-0dd6-da0e-d1b5ad34de2f/dj.ipxlbupf.jpg/600x600bb.jpg",
  "daft punk|||robot rock": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/d5/62/c5/d562c522-0e2c-1b57-d03e-0cae58b53b0e/825646310258.jpg/600x600bb.jpg",
  "above & beyond|||sun moon": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/ef/65/6a/ef656a3b-a86b-e41e-a310-a71d88fc0fcc/5054197604355.jpg/600x600bb.jpg",
  "above & beyond|||thing called love": "https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/36/27/70/3627701d-e9c3-c0d7-05f7-9e2fab2bcbcc/5054197546860.jpg/600x600bb.jpg",
  "above & beyond|||you got to go": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/ef/65/6a/ef656a3b-a86b-e41e-a310-a71d88fc0fcc/5054197604355.jpg/600x600bb.jpg",
  "above & beyond|||satellite": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/ae/a3/85/aea38562-c15d-22c6-b7df-5808b54ffcbf/5054197621611.jpg/600x600bb.jpg",
  "kygo|||firestone": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/61/97/81/619781de-8920-0ba9-c4f9-83bd1b69faed/886445100211.jpg/600x600bb.jpg",
  "kygo|||stole the show": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/61/97/81/619781de-8920-0ba9-c4f9-83bd1b69faed/886445100211.jpg/600x600bb.jpg",
  "kygo|||it aint me": "https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/10/d1/fc/10d1fc50-a0d9-18ff-9aab-dd5e20bb1a17/886446377919.jpg/600x600bb.jpg",
  "kygo|||stargazing": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/6d/10/77/6d10774e-80ea-ea1e-83b7-b9cefb0d9693/886446912479.jpg/600x600bb.jpg",
  "kygo|||higher love": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/7e/e4/10/7ee410d7-2c0a-4dd3-5001-2b0a50eb9de9/886447810804.jpg/600x600bb.jpg",
  "kygo|||happy now": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/6d/10/77/6d10774e-80ea-ea1e-83b7-b9cefb0d9693/886446912479.jpg/600x600bb.jpg",
  "marshmello|||alone": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/e5/61/70/e5617013-6ed6-dd08-ba28-dbb6aa37b96e/859729600271.jpg/600x600bb.jpg",
  "marshmello|||happier": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/bc/fe/32/bcfe32b9-9c79-e2c4-0887-85bf54f8e1dc/00602567952961.rgb.jpg/600x600bb.jpg",
  "marshmello|||wolves": "https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/c0/d9/e5/c0d9e59d-84e3-d70f-1a91-9bcb6d32ff4c/00602557849912.rgb.jpg/600x600bb.jpg",
  "marshmello|||friends": "https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/f3/c1/89/f3c189a4-0bfc-8af3-f00e-0e5fe6f00ca9/075679878588.jpg/600x600bb.jpg",
  "marshmello|||silence": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/4b/08/f7/4b08f794-2e3c-b11f-d2b1-2c36e3edb01f/859729505378.jpg/600x600bb.jpg",
  "zedd|||clarity": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a9/be/43/a9be4364-a52b-bf41-e879-5cc69c9b3c24/00602537240654.rgb.jpg/600x600bb.jpg",
  "zedd|||stay the night": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a9/be/43/a9be4364-a52b-bf41-e879-5cc69c9b3c24/00602537240654.rgb.jpg/600x600bb.jpg",
  "zedd|||beautiful now": "https://is1-ssl.mzstatic.com/image/thumb/Music113/v4/48/0a/24/480a245b-a66a-73ee-2988-e6a2bf450168/00602547344939.rgb.jpg/600x600bb.jpg",
  "zedd|||spectrum": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a9/be/43/a9be4364-a52b-bf41-e879-5cc69c9b3c24/00602537240654.rgb.jpg/600x600bb.jpg",
  "zedd|||the middle": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/c9/50/72/c9507249-e8a0-6ab0-fdba-b6bb0d20a133/00602567307631.rgb.jpg/600x600bb.jpg",
  "zedd|||stay": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/7c/a9/d9/7ca9d94a-d95e-a5f6-a6bf-4fb0e3e6f25e/00602567307631.rgb.jpg/600x600bb.jpg",
  "fisher|||losing it": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/46/c7/b9/46c7b93d-2a3b-ab90-7fc4-3a2a01feff44/5056022660771.jpg/600x600bb.jpg",
  "fisher|||you little beauty": "https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/6d/5a/cc/6d5accb5-3385-01dd-66a9-8a2bf01e31e6/5056022660887.jpg/600x600bb.jpg",
  "fisher|||stop it": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/fd/3f/9a/fd3f9ad9-0a09-ce13-88df-f5ae27098903/cover.jpg/600x600bb.jpg",
  "charlotte de witte|||age of love": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/1a/73/b3/1a73b3c9-5c58-d3e2-93ee-a28ed5bdf9d6/cover.jpg/600x600bb.jpg",
  "amelie lens|||in silence": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/42/a5/9f/42a59f89-9fd4-cc07-7dd2-4ed04d5017a7/cover.jpg/600x600bb.jpg",
  "amelie lens|||follow": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/42/a5/9f/42a59f89-9fd4-cc07-7dd2-4ed04d5017a7/cover.jpg/600x600bb.jpg",
  "tale of us|||alone": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/e9/d4/ee/e9d4ee9d-3c52-9f9f-61e9-d89f3e6a5f73/5054197316760.jpg/600x600bb.jpg",
  "boris brejcha|||gravity": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/bc/eb/da/bcebda45-58cb-8a86-1fac-1dfcc8ffed1c/825646416455.jpg/600x600bb.jpg",
  "boris brejcha|||purple noise": "https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/2f/f9/ef/2ff9ef2c-1da2-3ce4-c25a-c79afbc4b1a9/825646315307.jpg/600x600bb.jpg",
  "chris lake|||operator": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/49/f9/ed/49f9ed4e-49a8-f7e7-0a55-d9f63b9e6aba/190296898853.jpg/600x600bb.jpg",
  "chris lake|||turn off the lights": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/ab/54/c9/ab54c9bf-98f5-e3a4-1d81-f7eb0d1f4e57/190296962509.jpg/600x600bb.jpg",
  "rufus du sol|||innerbloom": "https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/df/83/ea/df83eac6-48f6-c1cf-a327-1caab7044b08/5054197035814.jpg/600x600bb.jpg",
  "rufus du sol|||you were right": "https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/df/83/ea/df83eac6-48f6-c1cf-a327-1caab7044b08/5054197035814.jpg/600x600bb.jpg",
  "rufus du sol|||alive": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/a9/46/de/a946de28-32e0-20f5-59bf-9fdf97ab6e60/5054197254086.jpg/600x600bb.jpg",
  "camelphat|||cola": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/a9/1b/99/a91b9939-fe50-7dd1-8e5b-a5dfc85a65b9/826194398026.jpg/600x600bb.jpg",
  "camelphat|||panic room": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/0a/c3/e9/0ac3e9ed-4e39-b64e-2c79-dd0e0b5b03b3/886447437766.jpg/600x600bb.jpg",
  "camelphat|||breathe": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/c0/1f/11/c01f11f5-0b27-f2a7-3dd2-1fb92cc4dd6e/886447430774.jpg/600x600bb.jpg",
  "disclosure|||latch": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/eb/73/96/eb739679-21eb-8a31-78b9-c80e6d31ecfe/00602537409242.rgb.jpg/600x600bb.jpg",
  "disclosure|||white noise": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/eb/73/96/eb739679-21eb-8a31-78b9-c80e6d31ecfe/00602537409242.rgb.jpg/600x600bb.jpg",
  "disclosure|||you me": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/eb/73/96/eb739679-21eb-8a31-78b9-c80e6d31ecfe/00602537409242.rgb.jpg/600x600bb.jpg",
  "disclosure|||f for you": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/eb/73/96/eb739679-21eb-8a31-78b9-c80e6d31ecfe/00602537409242.rgb.jpg/600x600bb.jpg",
  "disclosure|||omen": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/55/72/65/55726594-1866-b9aa-0c66-35e0b3a6a48a/00602547310125.rgb.jpg/600x600bb.jpg",
  "flume|||never be like you": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/70/ea/a6/70eaa64e-f9e7-c57b-5e88-59b55f5f4352/0602547850706.rgb.jpg/600x600bb.jpg",
  "flume|||say it": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/70/ea/a6/70eaa64e-f9e7-c57b-5e88-59b55f5f4352/0602547850706.rgb.jpg/600x600bb.jpg",
  "flume|||holdin on": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/ab/77/ce/ab77cede-0f81-92af-cadf-c6d1bffa2a4a/857710005363.jpg/600x600bb.jpg",
  "illenium|||good things fall apart": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/d7/6e/a9/d76ea9e9-7e54-9cbe-8f5a-0ba68b24d6f8/075679847775.jpg/600x600bb.jpg",
  "illenium|||takeaway": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/d7/6e/a9/d76ea9e9-7e54-9cbe-8f5a-0ba68b24d6f8/075679847775.jpg/600x600bb.jpg",
  "illenium|||feel good": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/2b/a3/68/2ba36895-fa6e-b50b-9f2e-1abc90cf3cc3/075679785503.jpg/600x600bb.jpg",
  "seven lions|||strangers": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/50/88/03/508803ec-0a7f-e618-cde2-2ed2ef3a6af5/00602557067576.rgb.jpg/600x600bb.jpg",
  "seven lions|||don't leave": "https://is1-ssl.mzstatic.com/image/thumb/Music7/v4/0b/f3/69/0bf369a9-7c93-5c80-dae7-c3e6d6b4ff00/00602547244895.rgb.jpg/600x600bb.jpg",
  "major lazer|||lean on": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/3a/ec/92/3aec927a-e0a9-01b5-17f6-8bfa2e05d4f2/075679913593.jpg/600x600bb.jpg",
  "major lazer|||cold water": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/51/85/11/518511de-98b9-cde7-88bc-d7b5ee5e1a24/00602557024883.rgb.jpg/600x600bb.jpg",
  "major lazer|||light it up": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/3a/ec/92/3aec927a-e0a9-01b5-17f6-8bfa2e05d4f2/075679913593.jpg/600x600bb.jpg",
  "major lazer|||powerful": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/3a/ec/92/3aec927a-e0a9-01b5-17f6-8bfa2e05d4f2/075679913593.jpg/600x600bb.jpg",
  "darude|||sandstorm": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/cc/1a/8a/cc1a8a41-ef4c-1f80-8b51-db12bf2e6ca0/5050459020320.jpg/600x600bb.jpg",
  "robert miles|||children": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/8f/40/a7/8f40a76d-ca7e-aebc-4c1e-04b8e2cd46cf/mzi.sfxjkqog.jpg/600x600bb.jpg",
  "gigi d'agostino|||l'amour toujours": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/8c/1d/14/8c1d1486-0a1b-4a9a-3a66-7ab96cd0c3ab/mzi.mafmfvwm.jpg/600x600bb.jpg",
  "alice deejay|||better off alone": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/d5/ae/91/d5ae91b6-3c58-84a8-ead5-d29dc3ef27f6/5053105995530.jpg/600x600bb.jpg",
  "eiffel 65|||blue": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/d5/81/b1/d581b11c-f6bc-8afa-09a8-e37492bf5d1a/BlottoBlotto_Logo.jpg/600x600bb.jpg",
  "pendulum|||watercolour": "https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/dc/6c/b5/dc6cb5b8-f43a-3faa-f534-50e3d25f5b9c/825646844173.jpg/600x600bb.jpg",
  "pendulum|||the island": "https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/dc/6c/b5/dc6cb5b8-f43a-3faa-f534-50e3d25f5b9c/825646844173.jpg/600x600bb.jpg",
  "bassnectar|||bass head": "https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/5d/db/07/5ddb075d-8abd-67b8-f11b-fdb2e0f93e2a/Cover.jpg/600x600bb.jpg",
  "the xx|||intro": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/c9/4c/5b/c94c5bdf-fc9b-55b7-c0a4-ba5f2f9b7c16/634904015268.jpg/600x600bb.jpg",
  "massive attack|||teardrop": "https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/3e/f8/05/3ef8055c-e64e-3bb7-c1a5-b1fa1d88db22/5099995180922.jpg/600x600bb.jpg",
  "moby|||porcelain": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/18/0d/f9/180df9dc-c0ca-f1cb-7b75-1e6e9d0d6c1f/724384839420.jpg/600x600bb.jpg",
  "m83|||midnight city": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/c7/34/61/c7346196-3f93-be22-8e07-7f4c5f4c02f7/dj.cbmlxjzn.jpg/600x600bb.jpg"
}

def update_covers():
    with app.app_context():
        tracks = Track.query.all()
        updated = 0

        for track in tracks:
            # 构建查询键
            artist_lower = track.artist.lower() if track.artist else ""
            title_lower = track.title.lower() if track.title else ""

            # 尝试精确匹配
            key = f"{artist_lower}|||{title_lower}"
            if key in cover_mapping:
                track.cover_url = cover_mapping[key]
                updated += 1
                continue

            # 尝试模糊匹配
            for map_key, cover_url in cover_mapping.items():
                map_artist, map_title = map_key.split("|||")
                if map_artist in artist_lower or artist_lower in map_artist:
                    if map_title in title_lower or title_lower in map_title:
                        track.cover_url = cover_url
                        updated += 1
                        break

        db.session.commit()
        print(f"Updated {updated} track covers")
        print(f"Total tracks: {Track.query.count()}")

if __name__ == "__main__":
    update_covers()
