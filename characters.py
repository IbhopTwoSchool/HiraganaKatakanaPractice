"""
Japanese character data for Hiragana and Katakana practice.
"""

# Hiragana characters with romanji mappings
HIRAGANA_DATA = [
    # Basic vowels
    ('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'),
    # K sounds
    ('か', 'ka'), ('き', 'ki'), ('く', 'ku'), ('け', 'ke'), ('こ', 'ko'),
    # S sounds
    ('さ', 'sa'), ('し', 'shi'), ('す', 'su'), ('せ', 'se'), ('そ', 'so'),
    # T sounds
    ('た', 'ta'), ('ち', 'chi'), ('つ', 'tsu'), ('て', 'te'), ('と', 'to'),
    # N sounds
    ('な', 'na'), ('に', 'ni'), ('ぬ', 'nu'), ('ね', 'ne'), ('の', 'no'),
    # H sounds
    ('は', 'ha'), ('ひ', 'hi'), ('ふ', 'fu'), ('へ', 'he'), ('ほ', 'ho'),
    # M sounds
    ('ま', 'ma'), ('み', 'mi'), ('む', 'mu'), ('め', 'me'), ('も', 'mo'),
    # Y sounds
    ('や', 'ya'), ('ゆ', 'yu'), ('よ', 'yo'),
    # R sounds
    ('ら', 'ra'), ('り', 'ri'), ('る', 'ru'), ('れ', 're'), ('ろ', 'ro'),
    # W sounds and N
    ('わ', 'wa'), ('を', 'wo'), ('ん', 'n'),
    # Dakuten (voiced) - G sounds
    ('が', 'ga'), ('ぎ', 'gi'), ('ぐ', 'gu'), ('げ', 'ge'), ('ご', 'go'),
    # Z sounds
    ('ざ', 'za'), ('じ', 'ji'), ('ず', 'zu'), ('ぜ', 'ze'), ('ぞ', 'zo'),
    # D sounds
    ('だ', 'da'), ('ぢ', 'ji'), ('づ', 'zu'), ('で', 'de'), ('ど', 'do'),
    # B sounds
    ('ば', 'ba'), ('び', 'bi'), ('ぶ', 'bu'), ('べ', 'be'), ('ぼ', 'bo'),
    # Handakuten - P sounds
    ('ぱ', 'pa'), ('ぴ', 'pi'), ('ぷ', 'pu'), ('ぺ', 'pe'), ('ぽ', 'po'),
    # Combination characters (ya, yu, yo combinations)
    ('きゃ', 'kya'), ('きゅ', 'kyu'), ('きょ', 'kyo'),
    ('しゃ', 'sha'), ('しゅ', 'shu'), ('しょ', 'sho'),
    ('ちゃ', 'cha'), ('ちゅ', 'chu'), ('ちょ', 'cho'),
    ('にゃ', 'nya'), ('にゅ', 'nyu'), ('にょ', 'nyo'),
    ('ひゃ', 'hya'), ('ひゅ', 'hyu'), ('ひょ', 'hyo'),
    ('みゃ', 'mya'), ('みゅ', 'myu'), ('みょ', 'myo'),
    ('りゃ', 'rya'), ('りゅ', 'ryu'), ('りょ', 'ryo'),
    ('ぎゃ', 'gya'), ('ぎゅ', 'gyu'), ('ぎょ', 'gyo'),
    ('じゃ', 'ja'), ('じゅ', 'ju'), ('じょ', 'jo'),
    ('びゃ', 'bya'), ('びゅ', 'byu'), ('びょ', 'byo'),
    ('ぴゃ', 'pya'), ('ぴゅ', 'pyu'), ('ぴょ', 'pyo'),
]

# Katakana characters with romanji mappings
KATAKANA_DATA = [
    # Basic vowels
    ('ア', 'a'), ('イ', 'i'), ('ウ', 'u'), ('エ', 'e'), ('オ', 'o'),
    # K sounds
    ('カ', 'ka'), ('キ', 'ki'), ('ク', 'ku'), ('ケ', 'ke'), ('コ', 'ko'),
    # S sounds
    ('サ', 'sa'), ('シ', 'shi'), ('ス', 'su'), ('セ', 'se'), ('ソ', 'so'),
    # T sounds
    ('タ', 'ta'), ('チ', 'chi'), ('ツ', 'tsu'), ('テ', 'te'), ('ト', 'to'),
    # N sounds
    ('ナ', 'na'), ('ニ', 'ni'), ('ヌ', 'nu'), ('ネ', 'ne'), ('ノ', 'no'),
    # H sounds
    ('ハ', 'ha'), ('ヒ', 'hi'), ('フ', 'fu'), ('ヘ', 'he'), ('ホ', 'ho'),
    # M sounds
    ('マ', 'ma'), ('ミ', 'mi'), ('ム', 'mu'), ('メ', 'me'), ('モ', 'mo'),
    # Y sounds
    ('ヤ', 'ya'), ('ユ', 'yu'), ('ヨ', 'yo'),
    # R sounds
    ('ラ', 'ra'), ('リ', 'ri'), ('ル', 'ru'), ('レ', 're'), ('ロ', 'ro'),
    # W sounds and N
    ('ワ', 'wa'), ('ヲ', 'wo'), ('ン', 'n'),
    # Dakuten (voiced) - G sounds
    ('ガ', 'ga'), ('ギ', 'gi'), ('グ', 'gu'), ('ゲ', 'ge'), ('ゴ', 'go'),
    # Z sounds
    ('ザ', 'za'), ('ジ', 'ji'), ('ズ', 'zu'), ('ゼ', 'ze'), ('ゾ', 'zo'),
    # D sounds
    ('ダ', 'da'), ('ヂ', 'ji'), ('ヅ', 'zu'), ('デ', 'de'), ('ド', 'do'),
    # B sounds
    ('バ', 'ba'), ('ビ', 'bi'), ('ブ', 'bu'), ('ベ', 'be'), ('ボ', 'bo'),
    # Handakuten - P sounds
    ('パ', 'pa'), ('ピ', 'pi'), ('プ', 'pu'), ('ペ', 'pe'), ('ポ', 'po'),
    # Combination characters
    ('キャ', 'kya'), ('キュ', 'kyu'), ('キョ', 'kyo'),
    ('シャ', 'sha'), ('シュ', 'shu'), ('ショ', 'sho'),
    ('チャ', 'cha'), ('チュ', 'chu'), ('チョ', 'cho'),
    ('ニャ', 'nya'), ('ニュ', 'nyu'), ('ニョ', 'nyo'),
    ('ヒャ', 'hya'), ('ヒュ', 'hyu'), ('ヒョ', 'hyo'),
    ('ミャ', 'mya'), ('ミュ', 'myu'), ('ミョ', 'myo'),
    ('リャ', 'rya'), ('リュ', 'ryu'), ('リョ', 'ryo'),
    ('ギャ', 'gya'), ('ギュ', 'gyu'), ('ギョ', 'gyo'),
    ('ジャ', 'ja'), ('ジュ', 'ju'), ('ジョ', 'jo'),
    ('ビャ', 'bya'), ('ビュ', 'byu'), ('ビョ', 'byo'),
    ('ピャ', 'pya'), ('ピュ', 'pyu'), ('ピョ', 'pyo'),
]

# Legacy lists for backward compatibility
HIRAGANA = [char for char, _ in HIRAGANA_DATA]
KATAKANA = [char for char, _ in KATAKANA_DATA]

# Educational information about each character
# Format: character -> {history, usage, notes, common_words}
CHARACTER_INFO = {
    # Hiragana vowels
    'あ': {
        'origin': 'Derived from cursive 安 (an, "peace"). The kanji 安 shows woman (女) under roof (宀), representing safety.',
        'usage': 'First character in gojūon order. Essential particle in ああ (aa, "ah, yes"). Used as indefinite prefix: あの人 (ano hito, "that person"). Appears in verb conjugations and many core words.',
        'notes': 'Pronounced with an open mouth, like "ah" in "father". The stroke order starts with the left hook. Memory tip: Looks like a lowercase "a" with extra flourish. Essential for beginners as it starts the entire syllabary system.',
        'words': ['愛 (あい, ai) - love', '赤 (あか, aka) - red', 'ある (aru) - to exist/have', 'あなた (anata) - you', 'あさ (asa) - morning', 'あした (ashita) - tomorrow']
    },
    'い': {
        'origin': 'Derived from cursive 以 (i, "by means of"). The radical means "to use" or "by means of".',
        'usage': 'Common in adjective endings: all -i adjectives end with い (大きい ookii - big, 小さい chiisai - small). Essential for conjugation. Also used in いい (ii, "good") - one of the most common words.',
        'notes': 'Pronounced like "ee" in "see", but shorter. Two simple strokes. Memory tip: Looks like two vertical lines standing side by side, like "ii" (two i\'s). Critical for adjective system - all Japanese adjectives end in い.',
        'words': ['犬 (いぬ, inu) - dog', '家 (いえ, ie) - house', 'いい (ii) - good', 'いる (iru) - to exist (animate)', 'いく (iku) - to go', '石 (いし, ishi) - stone']
    },
    'う': {
        'origin': 'Derived from cursive 宇 (u, "universe"). Character originally meant space/eaves, representing vastness.',
        'usage': 'Used in verb endings - う段 (u-dan) is crucial for dictionary form verbs: 食べる (taberu) → 食べます (tabemasu). The う sound marks polite negative: 行かない (ikanai, "don\'t go"). Long vowel marker after o-sounds.',
        'notes': 'Lips rounded less than English "oo", more compressed. Looks like a smiling face. Memory tip: The curve resembles a smile - think "oooh!" Critical for verb conjugation patterns.',
        'words': ['馬 (うま, uma) - horse', '海 (うみ, umi) - sea', 'うえ (ue) - above', 'うち (uchi) - home/inside', 'うた (uta) - song', 'うし (ushi) - cow']
    },
    'え': {
        'origin': 'Derived from cursive 衣 (e, "clothing"). The radical represents garments and covering.',
        'usage': 'Common in potential form verbs: 食べられる (taberareru) uses え段. Direction particle へ is written with this but pronounced "e". Used in many question words: 何 (なに/なん, nani/nan) becomes なんですか (nandesuka).',
        'notes': 'Pronounced like "eh" in "get", between "eh" and "ay". Two strokes. Memory tip: Looks like exotic bird or hieroglyph. Important for potential verb forms.',
        'words': ['駅 (えき, eki) - station', '絵 (え, e) - picture', 'えん (en) - yen/circle', 'えいが (eiga) - movie', 'えんぴつ (enpitsu) - pencil']
    },
    'お': {
        'origin': 'Derived from cursive 於 (o, "at/in"). The kanji 於 originally meant "to be at" or "in/at" location.',
        'usage': 'Polite prefix お～ (o~) for honorifics: お茶 (ocha, tea), お金 (okane, money). Direction/object particle を is written with this but pronounced "o". Shows respect when added to nouns.',
        'notes': 'Pronounced with rounded lips, like "oh" in "go". Three strokes forming distinctive shape. Memory tip: Looks like "o" with tail. Essential for politeness - adding お shows respect.',
        'words': ['男 (おとこ, otoko) - man', 'お茶 (おちゃ, ocha) - tea', 'おおきい (ookii) - big', 'おかあさん (okaasan) - mother', 'おとうと (otouto) - younger brother']
    },
    
    # K-row hiragana
    'か': {
        'origin': 'Derived from cursive 加 (ka, "add"). The kanji combines 力 (power) and 口 (mouth), suggesting forceful speech.',
        'usage': 'Question particle か (ka) marks yes/no questions - THE most important particle for beginners. 行きますか (ikimasu ka, "Will you go?"). Also marks alternatives: AかB (A ka B, "A or B"). Essential for question formation.',
        'notes': 'か is one of the most common particles in Japanese. Unvoiced /k/ sound. Memory tip: Looks like someone raising hand to ask question. RULE: か at sentence end always makes it a question.',
        'words': ['顔 (かお, kao) - face', '風 (かぜ, kaze) - wind', 'かく (kaku) - to write', 'かう (kau) - to buy', 'かみ (kami) - paper/hair/god', 'からだ (karada) - body']
    },
    'き': {
        'origin': 'Derived from cursive 幾 (ki, "how many"). The kanji relates to counting and quantity.',
        'usage': 'Used in many common words and verb stems. The verb 来る (kuru, "to come") uses き in conjugation: 来ます (kimasu). Essential counter suffix: 木 (ki) for trees. Appears in directional words.',
        'notes': 'The /k/ sound before /i/ is slightly palatalized (softer than "key"). Three strokes. Memory tip: Looks like a KEY. Critical for verbs of motion and coming/going.',
        'words': ['木 (き, ki) - tree/wood', '聞く (きく, kiku) - to listen', 'きれい (kirei) - pretty/clean', 'きた (kita) - north', 'きのう (kinou) - yesterday', 'きもの (kimono) - kimono']
    },
    'く': {
        'origin': 'Derived from cursive 久 (ku, "long time"). The character originally represented duration.',
        'usage': 'Verb ending -ku conjugation: 大きく (ookiku, "in a big way"). Adverb form for i-adjectives. Common verb 来る (kuru, "come") uses this sound. Direction: 北 (kita, north) contains く sound.',
        'notes': 'Simple shape - one stroke. Memory tip: Looks like a less-than sign "<". Essential for adverb formation from adjectives. RULE: い adjectives → く for adverb.',
        'words': ['口 (くち, kuchi) - mouth', '靴 (くつ, kutsu) - shoes', 'くに (kuni) - country', 'くる (kuru) - to come', 'くろい (kuroi) - black', 'くすり (kusuri) - medicine']
    },
    'け': {
        'origin': 'Derived from cursive 計 (kei, "measure/count"). Related to calculation and planning.',
        'usage': 'Imperative form ending for verbs. Common in casual commands. Appears in question words and exclamations. Used in だけ (dake, "only") - important limiting particle.',
        'notes': 'Three strokes forming distinctive shape. Memory tip: Looks like someone kicking (ke-kick). Important for casual/masculine speech patterns.',
        'words': ['毛 (け, ke) - hair/fur', 'けっこう (kekkou) - quite/fine', 'けさ (kesa) - this morning', 'けしゴム (keshigomu) - eraser', 'けっか (kekka) - result']
    },
    'こ': {
        'origin': 'Derived from cursive 己 (ko, "self"). The kanji represents oneself or one\'s own.',
        'usage': 'Demonstrative pronoun これ (kore, "this"). Child: 子 (ko). Small: 小さい (chiisai) uses こ sound. Essential for pointing and demonstrating objects near speaker.',
        'notes': 'Two simple strokes. Memory tip: Looks like two lines, represents "this" (close to speaker). RULE: これ (this), それ (that), あれ (that over there) pattern.',
        'words': ['子 (こ, ko) - child', 'ここ (koko) - here', 'これ (kore) - this', 'こえ (koe) - voice', 'こころ (kokoro) - heart', 'こたえ (kotae) - answer']
    },
    
    # S-row hiragana
    'さ': {
        'origin': 'Derived from cursive 左 (sa, "left")',
        'usage': 'Common in many nouns and verb stems.',
        'notes': 'さ is pronounced as clear /sa/, not /sha/.',
        'words': ['魚 (さかな, sakana) - fish', '桜 (さくら, sakura) - cherry blossom']
    },
    'し': {
        'origin': 'Derived from cursive 之 (shi)',
        'usage': 'Verb ます (masu) form ending. Death (死) reading.',
        'notes': 'Romanized as "shi", not "si". Avoid number 4.',
        'words': ['白 (しろ, shiro) - white', '下 (した, shita) - below']
    },
    'す': {
        'origin': 'Derived from cursive 寸 (sun, "inch")',
        'usage': 'Common in verb stems and する (suru, "to do").',
        'notes': 'する is one of only two irregular verbs.',
        'words': ['好き (すき, suki) - to like', '寿司 (すし, sushi) - sushi']
    },
    'せ': {
        'origin': 'Derived from cursive 世 (se, "world")',
        'usage': 'Imperative verb ending and various compounds.',
        'notes': 'Part of 先生 (sensei, teacher).',
        'words': ['世界 (せかい, sekai) - world', '背 (せ, se) - back']
    },
    'そ': {
        'origin': 'Derived from cursive 曽 (so)',
        'usage': 'Demonstrative それ (sore) means "that".',
        'notes': 'Middle-distance demonstrative in こ/そ/あ.',
        'words': ['空 (そら, sora) - sky', 'そば (soba) - buckwheat noodles']
    },
    
    # T-row hiragana
    'た': {
        'origin': 'Derived from cursive 太 (ta, "big/thick")',
        'usage': 'Past tense verb ending: 食べた (tabeta, "ate").',
        'notes': 'た indicates completed actions.',
        'words': ['食べる (たべる, taberu) - to eat', '高い (たかい, takai) - expensive']
    },
    'ち': {
        'origin': 'Derived from cursive 知 (chi, "know")',
        'usage': 'Common in many words. Part of 血 (chi, blood).',
        'notes': 'Romanized as "chi", not "ti".',
        'words': ['父 (ちち, chichi) - father', '小さい (ちいさい, chiisai) - small']
    },
    'つ': {
        'origin': 'Derived from cursive 川 (sen, "river")',
        'usage': 'Counter for items: 一つ (hitotsu, one thing).',
        'notes': 'Small っ (sokuon) indicates gemination.',
        'words': ['月 (つき, tsuki) - moon', '机 (つくえ, tsukue) - desk']
    },
    'て': {
        'origin': 'Derived from cursive 天 (ten, "heaven")',
        'usage': 'て-form connects verbs and creates commands.',
        'notes': 'Most versatile verb form in Japanese.',
        'words': ['手 (て, te) - hand', 'テスト (tesuto) - test']
    },
    'と': {
        'origin': 'Derived from cursive 止 (to, "stop")',
        'usage': 'Particle と (to) means "and" or "with".',
        'notes': 'Used for quotations: 〜と言う (to iu).',
        'words': ['友達 (ともだち, tomodachi) - friend', '所 (ところ, tokoro) - place']
    },
    
    # N-row hiragana
    'な': {
        'origin': 'Derived from cursive 奈 (na)',
        'usage': 'Negative imperative: するな (suruna, "don\'t do").',
        'notes': 'な-adjectives use な to modify nouns.',
        'words': ['名前 (なまえ, namae) - name', '夏 (なつ, natsu) - summer']
    },
    'に': {
        'origin': 'Derived from cursive 仁 (ni, "benevolence")',
        'usage': 'Particle に (ni) for time, location, indirect object.',
        'notes': 'One of most important particles in Japanese.',
        'words': ['肉 (にく, niku) - meat', '日本 (にほん, nihon) - Japan']
    },
    'ぬ': {
        'origin': 'Derived from cursive 奴 (nu)',
        'usage': 'Archaic negative: 知らぬ (shiranu, "don\'t know").',
        'notes': 'Less common in modern Japanese.',
        'words': ['犬 (いぬ, inu) - dog', '布 (ぬの, nuno) - cloth']
    },
    'ね': {
        'origin': 'Derived from cursive 祢 (ne)',
        'usage': 'Sentence-ending particle ね (ne) seeks agreement.',
        'notes': 'Similar to "right?" or "isn\'t it?" in English.',
        'words': ['猫 (ねこ, neko) - cat', '寝る (ねる, neru) - to sleep']
    },
    'の': {
        'origin': 'Derived from cursive 乃 (no)',
        'usage': 'Possessive particle の (no): 私の本 (my book).',
        'notes': 'Most common particle, marks possession/relation.',
        'words': ['飲む (のむ, nomu) - to drink', '野菜 (やさい, yasai) - vegetables']
    },
    
    # H-row hiragana
    'は': {
        'origin': 'Derived from cursive 波 (ha, "wave")',
        'usage': 'Topic marker は is pronounced "wa" as particle.',
        'notes': 'は vs. が is fundamental to Japanese grammar.',
        'words': ['花 (はな, hana) - flower', '母 (はは, haha) - mother']
    },
    'ひ': {
        'origin': 'Derived from cursive 比 (hi, "compare")',
        'usage': 'Common in time words: 一日 (ichi-nichi, one day).',
        'notes': 'Fire (火, hi) and day (日, hi) have same sound.',
        'words': ['人 (ひと, hito) - person', '左 (ひだり, hidari) - left']
    },
    'ふ': {
        'origin': 'Derived from cursive 不 (fu, "not")',
        'usage': 'Unusual romanization: "fu" not "hu".',
        'notes': 'Pronounced between /hu/ and /fu/.',
        'words': ['冬 (ふゆ, fuyu) - winter', '船 (ふね, fune) - ship']
    },
    'へ': {
        'origin': 'Derived from cursive 部 (he)',
        'usage': 'Direction particle へ pronounced "e".',
        'notes': 'Points toward destination: 東京へ (to Tokyo).',
        'words': ['部屋 (へや, heya) - room', '蛇 (へび, hebi) - snake']
    },
    'ほ': {
        'origin': 'Derived from cursive 保 (ho, "protect")',
        'usage': 'Common in various compounds and words.',
        'notes': 'ほ sound is common in daily vocabulary.',
        'words': ['本 (ほん, hon) - book', '欲しい (ほしい, hoshii) - to want']
    },
    
    # M-row hiragana
    'ま': {
        'origin': 'Derived from cursive 末 (ma, "end")',
        'usage': 'Used in the polite ます (masu) verb ending.',
        'notes': 'ます form is most basic polite verb form.',
        'words': ['町 (まち, machi) - town', '窓 (まど, mado) - window']
    },
    'み': {
        'origin': 'Derived from cursive 美 (mi, "beauty")',
        'usage': 'Nominalizer: 読み (yomi, reading).',
        'notes': 'Turns verbs into nouns.',
        'words': ['耳 (みみ, mimi) - ear', '水 (みず, mizu) - water']
    },
    'む': {
        'origin': 'Derived from cursive 武 (mu, "military")',
        'usage': 'Volitional う→む shift in classical Japanese.',
        'notes': 'Less common in modern vocabulary.',
        'words': ['昔 (むかし, mukashi) - old times', '虫 (むし, mushi) - insect']
    },
    'め': {
        'origin': 'Derived from cursive 女 (me, "woman")',
        'usage': 'Common in body parts and abstract concepts.',
        'notes': 'め can indicate ordinal numbers.',
        'words': ['目 (め, me) - eye', '女 (おんな, onna) - woman']
    },
    'も': {
        'origin': 'Derived from cursive 毛 (mo, "hair")',
        'usage': 'Particle も (mo) means "also" or "too".',
        'notes': 'Inclusive particle, adds items to list.',
        'words': ['桃 (もも, momo) - peach', '文字 (もじ, moji) - character']
    },
    
    # Y-row hiragana
    'や': {
        'origin': 'Derived from cursive 也 (ya)',
        'usage': 'Used in compound syllables: きゃ、しゃ、ちゃ.',
        'notes': 'Small version ゃ combines with i-column kana.',
        'words': ['山 (やま, yama) - mountain', '野菜 (やさい, yasai) - vegetable']
    },
    'ゆ': {
        'origin': 'Derived from cursive 由 (yu, "reason")',
        'usage': 'Small version ゅ forms compound sounds.',
        'notes': 'Common in compound syllables throughout Japanese.',
        'words': ['雪 (ゆき, yuki) - snow', '夢 (ゆめ, yume) - dream']
    },
    'よ': {
        'origin': 'Derived from cursive 与 (yo, "give")',
        'usage': 'Sentence-ending particle よ adds emphasis.',
        'notes': 'Small version ょ completes many compounds.',
        'words': ['夜 (よる, yoru) - night', '四 (よん, yon) - four']
    },
    
    # R-row hiragana
    'ら': {
        'origin': 'Derived from cursive 良 (ra, "good")',
        'usage': 'Japanese /r/ is between English /r/ and /l/.',
        'notes': 'Tap the alveolar ridge with tongue tip.',
        'words': ['来年 (らいねん, rainen) - next year', 'ラーメン (ramen) - ramen']
    },
    'り': {
        'origin': 'Derived from cursive 利 (ri, "profit")',
        'usage': 'Common in many verbs and adjectives.',
        'notes': 'り is one of more frequent kana.',
        'words': ['料理 (りょうり, ryouri) - cooking', '緑 (みどり, midori) - green']
    },
    'る': {
        'origin': 'Derived from cursive 留 (ru, "stay")',
        'usage': 'Dictionary form ending for many verbs.',
        'notes': 'Verb groups: 五段 (godan) vs 一段 (ichidan).',
        'words': ['昼 (ひる, hiru) - daytime', '〜いる/える (iru/eru) verbs']
    },
    'れ': {
        'origin': 'Derived from cursive 礼 (rei, "courtesy")',
        'usage': 'Potential and passive form component.',
        'notes': 'Important in advanced verb conjugations.',
        'words': ['例 (れい, rei) - example', '歴史 (れきし, rekishi) - history']
    },
    'ろ': {
        'origin': 'Derived from cursive 呂 (ro)',
        'usage': 'Seen in imperative and various compounds.',
        'notes': 'ろ sound appears in many place names.',
        'words': ['黒 (くろ, kuro) - black', '六 (ろく, roku) - six']
    },
    
    # W-row hiragana and N
    'わ': {
        'origin': 'Derived from cursive 和 (wa, "harmony")',
        'usage': 'Topic particle は is pronounced as わ.',
        'notes': 'わ represents Japanese harmony (和).',
        'words': ['私 (わたし, watashi) - I', '若い (わかい, wakai) - young']
    },
    'を': {
        'origin': 'Derived from cursive 遠 (wo/o)',
        'usage': 'Direct object marker を, pronounced "o".',
        'notes': 'ONLY used as particle, never in words.',
        'words': ['本を読む (hon wo yomu) - read a book', 'Particle only']
    },
    'ん': {
        'origin': 'Derived from cursive 无 (n)',
        'usage': 'Moraic nasal, adapts to following sound.',
        'notes': 'Cannot start a word. Game しりとり loses with ん.',
        'words': ['本 (ほん, hon) - book', '先生 (せんせい, sensei) - teacher']
    },
    
    # Dakuten (voiced) - G, Z, D, B
    'が': {
        'origin': 'か + dakuten (゛)',
        'usage': 'Subject marker particle が distinguishes subjects.',
        'notes': 'が vs は is crucial for emphasis.',
        'words': ['学校 (がっこう, gakkou) - school', '画家 (がか, gaka) - painter']
    },
    'ぎ': {
        'origin': 'き + dakuten (゛)',
        'usage': 'Voiced velar stop before /i/.',
        'notes': 'Can become velar nasal [ŋ] in some dialects.',
        'words': ['銀 (ぎん, gin) - silver', '牛乳 (ぎゅうにゅう, gyuunyuu) - milk']
    },
    'ぐ': {
        'origin': 'く + dakuten (゛)',
        'usage': 'Voiced version of く.',
        'notes': 'Often reduced to velar fricative between vowels.',
        'words': ['口 (くち, kuchi) - mouth', '具 (ぐ, gu) - ingredient']
    },
    'げ': {
        'origin': 'け + dakuten (゛)',
        'usage': 'Voiced ke sound.',
        'notes': 'Common in modern borrowed words.',
        'words': ['元気 (げんき, genki) - healthy', 'ゲーム (geemu) - game']
    },
    'ご': {
        'origin': 'こ + dakuten (゛)',
        'usage': 'Polite prefix ご〜 for Sino-Japanese words.',
        'notes': 'お〜 for native words, ご〜 for Chinese origin.',
        'words': ['ご飯 (ごはん, gohan) - rice/meal', '五 (ご, go) - five']
    },
    
    'ざ': {
        'origin': 'さ + dakuten (゛)',
        'usage': 'Voiced sibilant, can be [za] or [dza].',
        'notes': 'Varies between fricative and affricate.',
        'words': ['雑誌 (ざっし, zasshi) - magazine', '座る (すわる, suwaru) - to sit']
    },
    'じ': {
        'origin': 'し + dakuten (゛)',
        'usage': 'Same sound as ぢ but more common.',
        'notes': 'Usually written じ, not ぢ (except compounds).',
        'words': ['時間 (じかん, jikan) - time', '字 (じ, ji) - character']
    },
    'ず': {
        'origin': 'す + dakuten (゛)',
        'usage': 'More common than づ for /zu/ sound.',
        'notes': 'Used except in compounds with rendaku.',
        'words': ['頭 (あたま, atama) - head', '図書館 (としょかん, toshokan) - library']
    },
    'ぜ': {
        'origin': 'せ + dakuten (゛)',
        'usage': 'Voiced version of せ.',
        'notes': 'Common in emphatic expressions.',
        'words': ['全部 (ぜんぶ, zenbu) - all', 'ぜひ (zehi) - by all means']
    },
    'ぞ': {
        'origin': 'そ + dakuten (゛)',
        'usage': 'Emphatic masculine particle ぞ.',
        'notes': 'Adds strong assertion to statements.',
        'words': ['象 (ぞう, zou) - elephant', '増える (ふえる, fueru) - to increase']
    },
    
    'だ': {
        'origin': 'た + dakuten (゛)',
        'usage': 'Copula だ (da): plain form of です.',
        'notes': 'Essential for casual speech.',
        'words': ['誰 (だれ, dare) - who', '大学 (だいがく, daigaku) - university']
    },
    'ぢ': {
        'origin': 'ち + dakuten (゛)',
        'usage': 'Rare; same sound as じ but used in compounds.',
        'notes': 'Only in rendaku: 鼻血 (はなぢ, hanaji).',
        'words': ['鼻血 (はなぢ, hanaji) - nosebleed', 'Rare except compounds']
    },
    'づ': {
        'origin': 'つ + dakuten (゛)',
        'usage': 'Rare; same as ず but used in compounds.',
        'notes': 'Rendaku: 続く (つづく, tsuduku) to continue.',
        'words': ['続く (つづく, tsuduku) - to continue', 'Used mainly in rendaku']
    },
    'で': {
        'origin': 'て + dakuten (゛)',
        'usage': 'Location particle で marks where action occurs.',
        'notes': 'Also copula: です (desu) polite form.',
        'words': ['出る (でる, deru) - to exit', '電話 (でんわ, denwa) - telephone']
    },
    'ど': {
        'origin': 'と + dakuten (゛)',
        'usage': 'Question word stem: どこ (where), どれ (which).',
        'notes': 'ど- forms interrogatives with demonstratives.',
        'words': ['土曜日 (どようび, doyoubi) - Saturday', 'どう (dou) - how']
    },
    
    'ば': {
        'origin': 'は + dakuten (゛)',
        'usage': 'Conditional は→ば: 行けば (ikeba, "if you go").',
        'notes': 'ば-conditional is formal/written style.',
        'words': ['場所 (ばしょ, basho) - place', '馬 (うま, uma) - horse']
    },
    'び': {
        'origin': 'ひ + dakuten (゛)',
        'usage': 'Common in beauty/art words.',
        'notes': '美 (beauty) reading is び.',
        'words': ['美しい (うつくしい, utsukushii) - beautiful', '鼻 (はな, hana) - nose']
    },
    'ぶ': {
        'origin': 'ふ + dakuten (゛)',
        'usage': 'Common suffix for departments/divisions.',
        'notes': '部 (bu) means section/part.',
        'words': ['部屋 (へや, heya) - room', '運ぶ (はこぶ, hakobu) - to carry']
    },
    'べ': {
        'origin': 'へ + dakuten (゛)',
        'usage': 'Imperative べ in casual commands.',
        'notes': 'Rough masculine speech: 食べろ (tabero).',
        'words': ['勉強 (べんきょう, benkyou) - study', '別 (べつ, betsu) - separate']
    },
    'ぼ': {
        'origin': 'ほ + dakuten (゛)',
        'usage': 'Common in various everyday words.',
        'notes': 'ぼ appears frequently in vocabulary.',
        'words': ['僕 (ぼく, boku) - I (male)', '坊 (ぼう, bou) - boy/monk']
    },
    
    # Handakuten - P sounds
    'ぱ': {
        'origin': 'は + handakuten (゜)',
        'usage': 'Handakuten (゜) creates /p/ sound.',
        'notes': 'P-sound is not voiced, unlike B.',
        'words': ['パン (pan) - bread', 'ぱっと (patto) - suddenly']
    },
    'ぴ': {
        'origin': 'ひ + handakuten (゜)',
        'usage': 'P-sound before /i/.',
        'notes': 'Common in onomatopoeia and loanwords.',
        'words': ['ぴかぴか (pikapika) - shiny', 'ピンク (pinku) - pink']
    },
    'ぷ': {
        'origin': 'ふ + handakuten (゜)',
        'usage': 'P-sound, common in sound effects.',
        'notes': 'Puff sound, used in manga frequently.',
        'words': ['プール (puuru) - pool', 'ぷんぷん (punpun) - angry']
    },
    'ぺ': {
        'origin': 'へ + handakuten (゜)',
        'usage': 'Less common P-sound.',
        'notes': 'Appears mainly in loanwords.',
        'words': ['ペン (pen) - pen', 'ページ (peeji) - page']
    },
    'ぽ': {
        'origin': 'ほ + handakuten (゜)',
        'usage': 'P-sound, often in sound effects.',
        'notes': 'ぽん (pon) is common popping sound.',
        'words': ['ポスト (posuto) - mailbox', 'ぽかぽか (pokapoka) - warm']
    },
    
    # Katakana vowels
    'ア': {
        'origin': 'From 阿 (a), angular script',
        'usage': 'Katakana used for foreign words, emphasis, onomatopoeia.',
        'notes': 'More angular than hiragana.',
        'words': ['アメリカ (amerika) - America', 'アイス (aisu) - ice']
    },
    'イ': {
        'origin': 'From 伊 (i), angular script',
        'usage': 'Katakana for loanwords from European languages.',
        'notes': 'Looks like two strokes meeting.',
        'words': ['イギリス (igirisu) - England', 'インク (inku) - ink']
    },
    'ウ': {
        'origin': 'From 宇 (u), angular script',
        'usage': 'Extended sounds in loanwords: ウー (uu).',
        'notes': 'Top part looks like katakana ワ.',
        'words': ['ウイスキー (uisukii) - whiskey', 'ウール (uuru) - wool']
    },
    'エ': {
        'origin': 'From 江 (e), angular script',
        'usage': 'Common in English loanwords.',
        'notes': 'Similar to hiragana エ but more angular.',
        'words': ['エネルギー (enerugii) - energy', 'エレベーター (erebeetaa) - elevator']
    },
    'オ': {
        'origin': 'From 於 (o), angular script',
        'usage': 'Long vowel オー common in loanwords.',
        'notes': 'Three strokes forming box-like shape.',
        'words': ['オレンジ (orenji) - orange', 'オフィス (ofisu) - office']
    },
    
    # Additional katakana K-row
    'カ': {
        'origin': 'From 加 (ka), angular version',
        'usage': 'Katakana for foreign words and emphasis.',
        'notes': 'Force (力) and add (加) both read カ.',
        'words': ['カメラ (kamera) - camera', 'カード (kaado) - card']
    },
    'キ': {
        'origin': 'From 幾 (ki), angular version',
        'usage': 'Common in borrowed words.',
        'notes': 'Looks similar to hiragana き but straighter.',
        'words': ['キー (kii) - key', 'キロ (kiro) - kilo']
    },
    'ク': {
        'origin': 'From 久 (ku), angular version',
        'usage': 'Very short sound in katakana.',
        'notes': 'Looks like a mouth saying "ku".',
        'words': ['クラス (kurasu) - class', 'クイズ (kuizu) - quiz']
    },
    'ケ': {
        'origin': 'From 介 (ke), angular version',
        'usage': 'Used in cake, case, etc.',
        'notes': 'Three strokes, distinctive shape.',
        'words': ['ケーキ (keeki) - cake', 'ケース (keesu) - case']
    },
    'コ': {
        'origin': 'From 己 (ko), angular version',
        'usage': 'Simple two-stroke character.',
        'notes': 'Looks like two lines, easiest katakana.',
        'words': ['コーヒー (koohii) - coffee', 'コピー (kopii) - copy']
    },
    
    # Katakana S-row
    'サ': {
        'origin': 'From 散 (san), angular version',
        'usage': 'Service, size, etc in loanwords.',
        'notes': 'Three distinct strokes.',
        'words': ['サービス (saabisu) - service', 'サイズ (saizu) - size']
    },
    'シ': {
        'origin': 'From 之 (shi), angular version',
        'usage': 'Very common katakana. System, sheet, etc.',
        'notes': 'Looks like smile face: シ',
        'words': ['システム (shisutemu) - system', 'シャツ (shatsu) - shirt']
    },
    'ス': {
        'origin': 'From 須 (su), angular version',
        'usage': 'Speed, space, etc.',
        'notes': 'Looks like hiragana す but angular.',
        'words': ['スピード (supiido) - speed', 'スポーツ (supootsu) - sports']
    },
    'セ': {
        'origin': 'From 世 (se), angular version',
        'usage': 'Set, center, etc.',
        'notes': 'Looks similar to hiragana せ.',
        'words': ['セット (setto) - set', 'センター (sentaa) - center']
    },
    'ソ': {
        'origin': 'From 曽 (so), angular version',
        'usage': 'Soft, socks, etc.',
        'notes': 'Two strokes, looks like ン but different angle.',
        'words': ['ソフト (sofuto) - soft', 'ソース (soosu) - sauce']
    },
}

