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
