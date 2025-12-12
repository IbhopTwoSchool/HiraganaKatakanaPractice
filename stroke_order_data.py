"""
Comprehensive stroke order data for Japanese Hiragana and Katakana characters.
Each character maps to a list of strokes, where each stroke is a list of (x, y) coordinate tuples.
Coordinates are relative to the character center and should be scaled appropriately.

Format: character -> [stroke1, stroke2, ...] where each stroke is [(x1, y1), (x2, y2), ...]
Coordinates represent relative positions from center, typically in the range -50 to 50.
"""

# Hiragana stroke order data
HIRAGANA_STROKES = {
    # Basic vowels あ行
    'あ': [  # a - 3 strokes
        [(-30, -50), (-25, -30), (-20, -10)],  # Stroke 1: Left curve
        [(20, -60), (15, -40), (10, 0), (5, 30)],  # Stroke 2: Right vertical
        [(-15, 0), (-5, 15), (10, 25), (25, 30)]  # Stroke 3: Bottom sweep
    ],
    'い': [  # i - 2 strokes
        [(-5, -60), (-3, -30), (0, 0)],  # Stroke 1: Left short stroke
        [(5, -50), (7, -20), (10, 10), (12, 40)]  # Stroke 2: Right long stroke
    ],
    'う': [  # u - 2 strokes
        [(-30, -40), (-20, -35), (0, -30), (20, -30)],  # Stroke 1: Top horizontal dash
        [(-20, -10), (-10, 10), (5, 25), (20, 35)]  # Stroke 2: Bottom curve with tail
    ],
    'え': [  # e - 2 strokes
        [(-35, -30), (-10, -25), (15, -22), (35, -20)],  # Stroke 1: Top horizontal
        [(-30, 15), (-15, 20), (5, 25), (25, 30), (15, 50)]  # Stroke 2: Bottom curve with turn
    ],
    'お': [  # o - 3 strokes
        [(-35, -50), (-25, -45), (0, -40), (25, -40)],  # Stroke 1: Top horizontal
        [(20, -50), (20, -20), (20, 10)],  # Stroke 2: Right vertical
        [(-20, 0), (-10, 15), (10, 30), (30, 35)]  # Stroke 3: Bottom left-to-right curve
    ],
    
    # K sounds か行
    'か': [  # ka - 3 strokes
        [(-35, -50), (-25, -45), (0, -40), (20, -38)],  # Stroke 1: Top horizontal
        [(15, -50), (15, -20), (15, 10)],  # Stroke 2: Vertical stroke
        [(-25, 0), (-15, 15), (5, 30), (25, 35)]  # Stroke 3: Bottom curve
    ],
    'き': [  # ki - 4 strokes
        [(-15, -60), (-10, -30), (-5, 0), (0, 30)],  # Stroke 1: Left curve
        [(10, -55), (15, -25), (20, 5)],  # Stroke 2: Right vertical
        [(-25, -15), (0, -10), (25, -5)],  # Stroke 3: Middle horizontal
        [(-10, 10), (5, 20), (20, 30)]  # Stroke 4: Bottom right sweep
    ],
    'く': [  # ku - 1 stroke
        [(0, -50), (-10, -20), (-15, 10), (-10, 40), (5, 50)]  # Single diagonal curve
    ],
    'け': [  # ke - 3 strokes
        [(-35, -45), (-20, -40), (0, -35), (20, -32)],  # Stroke 1: Top horizontal
        [(-5, -50), (-5, -20), (-5, 10), (-5, 35)],  # Stroke 2: Vertical
        [(15, 0), (20, 15), (25, 30), (28, 45)]  # Stroke 3: Right diagonal
    ],
    'こ': [  # ko - 2 strokes
        [(-40, -40), (-20, -35), (10, -30), (30, -28)],  # Stroke 1: Top horizontal
        [(-35, 10), (-15, 15), (15, 20), (35, 22)]  # Stroke 2: Bottom horizontal
    ],
    
    # S sounds さ行
    'さ': [  # sa - 3 strokes
        [(-30, -50), (-20, -45), (0, -40), (20, -38)],  # Stroke 1: Top horizontal
        [(10, -50), (10, -20), (10, 10)],  # Stroke 2: Vertical
        [(-25, 0), (-10, 15), (10, 30), (30, 35)]  # Stroke 3: Bottom curve
    ],
    'し': [  # shi - 1 stroke
        [(0, -60), (-5, -30), (-10, 0), (-5, 30), (10, 50)]  # Single flowing curve
    ],
    'す': [  # su - 2 strokes
        [(-30, -40), (-15, -35), (10, -30), (25, -28)],  # Stroke 1: Top horizontal
        [(0, -10), (-5, 10), (0, 30), (15, 45), (35, 50)]  # Stroke 2: Curving diagonal
    ],
    'せ': [  # se - 3 strokes
        [(-35, -40), (-15, -35), (10, -32), (30, -30)],  # Stroke 1: Top horizontal
        [(-5, -45), (-5, -15), (-5, 15), (-5, 40)],  # Stroke 2: Vertical
        [(0, 20), (10, 30), (25, 38), (35, 42)]  # Stroke 3: Bottom right
    ],
    'そ': [  # so - 1 stroke
        [(-25, -45), (-15, -40), (5, -35), (15, -15), (10, 10), (0, 35), (-10, 50)]  # Single stroke
    ],
    
    # T sounds た行
    'た': [  # ta - 4 strokes
        [(-30, -50), (-15, -45), (10, -40), (25, -38)],  # Stroke 1: Top horizontal
        [(15, -50), (15, -20), (15, 10)],  # Stroke 2: Vertical
        [(-20, 0), (-5, 10), (15, 20)],  # Stroke 3: Middle horizontal
        [(-15, 20), (0, 30), (20, 35), (35, 38)]  # Stroke 4: Bottom horizontal
    ],
    'ち': [  # chi - 2 strokes
        [(-5, -55), (-5, -25), (-5, 5), (-3, 30)],  # Stroke 1: Vertical
        [(0, 5), (10, 15), (20, 30), (25, 45)]  # Stroke 2: Curved hook
    ],
    'つ': [  # tsu - 1 stroke
        [(-30, -30), (-15, -25), (5, -20), (20, 0), (25, 25), (20, 45)]  # Single curve
    ],
    'て': [  # te - 1 stroke
        [(-30, -35), (-15, -30), (5, -25), (20, -20), (20, 0), (15, 20), (5, 38)]  # Single stroke
    ],
    'と': [  # to - 2 strokes
        [(-5, -55), (-5, -25), (-5, 5)],  # Stroke 1: Short vertical
        [(0, 5), (10, 0), (20, -10), (25, -25), (20, -40), (5, -50), (-10, -45), (-20, -30), (-15, -10), (0, 5), (15, 20), (25, 38)]  # Stroke 2: Loop
    ],
    
    # N sounds な行
    'な': [  # na - 4 strokes
        [(-25, -50), (-15, -45), (5, -40), (20, -38)],  # Stroke 1: Top horizontal
        [(15, -50), (15, -20), (15, 10)],  # Stroke 2: Right vertical
        [(-30, -15), (-15, -10), (5, -5), (20, -3)],  # Stroke 3: Middle horizontal
        [(-20, 10), (-10, 20), (5, 30), (20, 38)]  # Stroke 4: Bottom curve
    ],
    'に': [  # ni - 2 strokes
        [(-35, -20), (-15, -15), (10, -10), (30, -8)],  # Stroke 1: Top horizontal
        [(-30, 15), (-10, 20), (15, 25), (35, 28)]  # Stroke 2: Bottom horizontal
    ],
    'ぬ': [  # nu - 2 strokes
        [(-30, -40), (-15, -35), (5, -30), (20, -28)],  # Stroke 1: Top horizontal
        [(0, -30), (-5, -10), (-10, 10), (-5, 30), (10, 45), (28, 50)]  # Stroke 2: Curving loop
    ],
    'ね': [  # ne - 2 strokes
        [(-25, -45), (-15, -40), (0, -35), (15, -15), (10, 10), (0, 30), (-10, 40)],  # Stroke 1: Curve
        [(10, 0), (20, 10), (30, 25), (35, 40)]  # Stroke 2: Right diagonal
    ],
    'の': [  # no - 1 stroke
        [(-10, -40), (0, -45), (15, -40), (30, -25), (35, 0), (30, 25), (15, 40), (-5, 45), (-20, 35), (-25, 15), (-20, -5), (-5, -20)]  # Single spiral
    ],
    
    # H sounds は行
    'は': [  # ha - 3 strokes
        [(-35, -45), (-20, -40), (0, -35), (20, -32)],  # Stroke 1: Top horizontal
        [(-5, -50), (-5, -20), (-5, 10)],  # Stroke 2: Left vertical
        [(10, -45), (15, -15), (20, 15), (25, 40)]  # Stroke 3: Right diagonal
    ],
    'ひ': [  # hi - 1 stroke
        [(-30, -30), (-20, -25), (-5, -20), (5, -10), (0, 10), (-10, 30), (-15, 45), (-5, 50), (10, 45), (20, 30)]  # Single curve
    ],
    'ふ': [  # fu - 4 strokes
        [(-10, -55), (-8, -30), (-5, 0)],  # Stroke 1: Small vertical
        [(5, -60), (8, -35), (10, -5)],  # Stroke 2: Small vertical
        [(-30, -10), (-10, -5), (15, 0), (35, 3)],  # Stroke 3: Middle horizontal
        [(0, 5), (5, 20), (10, 35), (12, 50)]  # Stroke 4: Bottom vertical
    ],
    'へ': [  # he - 1 stroke
        [(-35, -10), (-15, 5), (10, 15), (30, 20)]  # Single diagonal
    ],
    'ほ': [  # ho - 4 strokes
        [(-30, -50), (-15, -45), (5, -40), (25, -38)],  # Stroke 1: Top horizontal
        [(-5, -50), (-5, -20), (-5, 10)],  # Stroke 2: Left vertical
        [(10, -45), (10, -15), (10, 15)],  # Stroke 3: Right vertical
        [(-10, 20), (0, 30), (15, 38), (30, 42)]  # Stroke 4: Bottom curve
    ],
    
    # M sounds ま行
    'ま': [  # ma - 3 strokes
        [(-5, -55), (-5, -25), (-5, 5)],  # Stroke 1: Vertical
        [(-30, -20), (-10, -15), (15, -10), (35, -8)],  # Stroke 2: Horizontal
        [(0, 0), (-5, 20), (-10, 35), (0, 48), (15, 50), (30, 45)]  # Stroke 3: Bottom loop
    ],
    'み': [  # mi - 2 strokes
        [(-25, -35), (-15, -30), (0, -25), (15, -22)],  # Stroke 1: Top horizontal
        [(0, -20), (-5, 0), (-10, 20), (-5, 40), (10, 50), (28, 48)]  # Stroke 2: Curve
    ],
    'む': [  # mu - 3 strokes
        [(-10, -50), (-8, -25), (-5, 0)],  # Stroke 1: Small vertical
        [(-30, -15), (-10, -10), (15, -5), (35, -3)],  # Stroke 2: Horizontal
        [(0, 0), (-5, 20), (-10, 35), (0, 48), (15, 50), (30, 45)]  # Stroke 3: Bottom loop
    ],
    'め': [  # me - 2 strokes
        [(-20, -40), (-10, -35), (5, -30), (15, -10), (10, 10), (0, 30), (-10, 40)],  # Stroke 1: Curve
        [(10, -5), (20, 0), (30, 15), (35, 35)]  # Stroke 2: Right diagonal
    ],
    'も': [  # mo - 3 strokes
        [(-35, -35), (-15, -30), (10, -25), (30, -23)],  # Stroke 1: Top horizontal
        [(-5, -40), (-5, -10), (-5, 20)],  # Stroke 2: Vertical
        [(0, 20), (-5, 35), (5, 48), (20, 50), (35, 45)]  # Stroke 3: Bottom curve
    ],
    
    # Y sounds や行
    'や': [  # ya - 3 strokes
        [(-35, -40), (-15, -35), (10, -30), (30, -28)],  # Stroke 1: Top horizontal
        [(-5, -45), (-5, -15), (-5, 15)],  # Stroke 2: Vertical
        [(0, 15), (-5, 30), (5, 43), (20, 48), (35, 45)]  # Stroke 3: Bottom curve
    ],
    'ゆ': [  # yu - 2 strokes
        [(-30, -35), (-15, -30), (5, -25), (20, -23)],  # Stroke 1: Top horizontal
        [(0, -20), (-5, 0), (-10, 20), (-5, 38), (10, 48), (28, 45)]  # Stroke 2: Curve
    ],
    'よ': [  # yo - 2 strokes
        [(-35, -30), (-15, -25), (10, -20), (30, -18)],  # Stroke 1: Top horizontal
        [(-30, 10), (-10, 15), (15, 20), (35, 22)]  # Stroke 2: Bottom horizontal
    ],
    
    # R sounds ら行
    'ら': [  # ra - 2 strokes
        [(-5, -55), (-5, -25), (-5, 5)],  # Stroke 1: Vertical
        [(0, 5), (10, 15), (20, 30), (25, 45)]  # Stroke 2: Curved hook
    ],
    'り': [  # ri - 2 strokes
        [(-5, -60), (-3, -30), (0, 0), (2, 25)],  # Stroke 1: Short vertical curve
        [(5, -5), (15, 10), (25, 30), (28, 50)]  # Stroke 2: Diagonal
    ],
    'る': [  # ru - 1 stroke
        [(-25, -40), (-15, -35), (0, -30), (10, -10), (5, 10), (-5, 30), (-15, 40), (-5, 48), (10, 45), (25, 35)]  # Single loop
    ],
    'れ': [  # re - 2 strokes
        [(-30, -35), (-15, -30), (5, -25), (20, -23)],  # Stroke 1: Top horizontal
        [(0, -20), (-5, 0), (0, 20), (10, 38), (25, 45)]  # Stroke 2: Curve down
    ],
    'ろ': [  # ro - 3 strokes
        [(-30, -40), (-15, -35), (5, -30), (20, -28)],  # Stroke 1: Top horizontal
        [(10, -40), (10, -10), (10, 20)],  # Stroke 2: Vertical
        [(0, 20), (-5, 33), (5, 45), (20, 48), (35, 43)]  # Stroke 3: Bottom curve
    ],
    
    # W sounds and N わ行 + ん
    'わ': [  # wa - 2 strokes
        [(-35, -35), (-15, -30), (10, -25), (30, -23)],  # Stroke 1: Top horizontal
        [(0, -20), (-10, 0), (-15, 20), (-10, 38), (5, 48), (25, 45)]  # Stroke 2: Curve
    ],
    'を': [  # wo - 3 strokes
        [(-35, -40), (-15, -35), (10, -30), (30, -28)],  # Stroke 1: Top horizontal
        [(-5, -45), (-5, -15), (-5, 15)],  # Stroke 2: Vertical
        [(0, 15), (-5, 30), (5, 43), (20, 48), (35, 45)]  # Stroke 3: Bottom curve
    ],
    'ん': [  # n - 1 stroke
        [(0, -50), (-10, -20), (-15, 10), (-5, 40), (15, 50)]  # Single curve
    ],
}

# Katakana stroke order data
KATAKANA_STROKES = {
    # Basic vowels ア行
    'ア': [  # a - 3 strokes
        [(-10, -55), (0, -15), (5, 15)],  # Stroke 1: Vertical
        [(-35, 20), (-15, 25), (15, 30), (35, 32)],  # Stroke 2: Bottom horizontal
        [(25, -10), (30, 10), (32, 30)]  # Stroke 3: Right diagonal
    ],
    'イ': [  # i - 2 strokes
        [(-20, -50), (-10, -30), (0, 0), (5, 30)],  # Stroke 1: Left diagonal
        [(10, -55), (15, -25), (20, 5), (22, 35)]  # Stroke 2: Right diagonal
    ],
    'ウ': [  # u - 3 strokes
        [(-30, -45), (-15, -40), (10, -35), (25, -33)],  # Stroke 1: Top horizontal
        [(-20, -15), (0, -10), (20, -8)],  # Stroke 2: Middle horizontal
        [(0, 5), (10, 20), (20, 35), (30, 45)]  # Stroke 3: Bottom diagonal curve
    ],
    'エ': [  # e - 2 strokes
        [(-35, -30), (-10, -25), (15, -22), (35, -20)],  # Stroke 1: Top horizontal
        [(-30, 20), (-10, 25), (15, 28), (35, 30)]  # Stroke 2: Bottom horizontal
    ],
    'オ': [  # o - 3 strokes
        [(-30, -50), (-15, -45), (5, -40), (20, -38)],  # Stroke 1: Top horizontal
        [(10, -50), (10, -20), (10, 10)],  # Stroke 2: Vertical
        [(-35, 20), (-15, 25), (15, 30), (35, 32)]  # Stroke 3: Bottom horizontal
    ],
    
    # K sounds カ行
    'カ': [  # ka - 3 strokes
        [(-30, -50), (-15, -45), (5, -40), (20, -38)],  # Stroke 1: Top horizontal
        [(10, -50), (10, -20), (10, 10), (10, 35)],  # Stroke 2: Long vertical
        [(-30, 10), (-10, 15), (15, 20), (35, 22)]  # Stroke 3: Bottom horizontal
    ],
    'キ': [  # ki - 3 strokes
        [(-30, -35), (-10, -30), (15, -25), (35, -23)],  # Stroke 1: Top diagonal
        [(-25, 15), (-5, 20), (20, 25), (40, 27)],  # Stroke 2: Bottom diagonal
        [(10, -50), (10, -20), (10, 10), (10, 40)]  # Stroke 3: Vertical
    ],
    'ク': [  # ku - 2 strokes
        [(-25, -45), (-10, -30), (10, -10), (25, 5)],  # Stroke 1: Diagonal down
        [(0, 10), (10, 25), (20, 38), (30, 48)]  # Stroke 2: Diagonal up
    ],
    'ケ': [  # ke - 3 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (10, -15), (10, 15), (10, 40)],  # Stroke 2: Vertical
        [(-25, 20), (-5, 25), (20, 30), (40, 32)]  # Stroke 3: Bottom horizontal
    ],
    'コ': [  # ko - 2 strokes
        [(-35, -35), (-15, -30), (10, -25), (30, -23)],  # Stroke 1: Top horizontal
        [(-30, 20), (-10, 25), (15, 28), (35, 30)]  # Stroke 2: Bottom horizontal
    ],
    
    # S sounds サ行
    'サ': [  # sa - 3 strokes
        [(-30, -45), (-10, -40), (15, -35), (35, -33)],  # Stroke 1: Top horizontal
        [(-25, -10), (-5, -5), (20, 0), (40, 2)],  # Stroke 2: Middle horizontal
        [(-20, 25), (0, 30), (25, 33), (45, 35)]  # Stroke 3: Bottom horizontal
    ],
    'シ': [  # shi - 3 strokes
        [(-25, -30), (-15, -10), (-5, 10)],  # Stroke 1: Left diagonal
        [(0, -35), (5, -15), (10, 5)],  # Stroke 2: Middle diagonal
        [(15, -40), (20, -20), (25, 0), (28, 20)]  # Stroke 3: Right diagonal
    ],
    'ス': [  # su - 2 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(0, -5), (10, 10), (20, 25), (30, 40)]  # Stroke 2: Diagonal
    ],
    'セ': [  # se - 3 strokes
        [(-35, -35), (-15, -30), (10, -25), (30, -23)],  # Stroke 1: Top horizontal
        [(-30, 5), (-10, 10), (15, 13), (35, 15)],  # Stroke 2: Middle horizontal
        [(10, -40), (10, -10), (10, 20), (10, 45)]  # Stroke 3: Vertical
    ],
    'ソ': [  # so - 2 strokes
        [(-20, -40), (-10, -20), (0, 0)],  # Stroke 1: Left diagonal
        [(10, -45), (15, -25), (20, -5), (23, 15)]  # Stroke 2: Right diagonal
    ],
    
    # T sounds タ行
    'タ': [  # ta - 3 strokes
        [(-30, -45), (-10, -40), (15, -35), (35, -33)],  # Stroke 1: Top horizontal
        [(-25, 15), (-5, 20), (20, 23), (40, 25)],  # Stroke 2: Bottom horizontal
        [(10, -50), (10, -20), (10, 10), (10, 40)]  # Stroke 3: Vertical
    ],
    'チ': [  # chi - 3 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (10, -15), (10, 15)],  # Stroke 2: Short vertical
        [(0, 20), (10, 30), (25, 38), (40, 42)]  # Stroke 3: Diagonal
    ],
    'ツ': [  # tsu - 3 strokes
        [(-25, -30), (-15, -10), (-5, 10)],  # Stroke 1: Left diagonal
        [(0, -35), (5, -15), (10, 5)],  # Stroke 2: Middle diagonal
        [(15, -40), (20, -20), (25, 0)]  # Stroke 3: Right diagonal
    ],
    'テ': [  # te - 3 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (10, -15), (10, 15), (10, 40)],  # Stroke 2: Vertical
        [(-25, 20), (-5, 25), (20, 28), (40, 30)]  # Stroke 3: Bottom horizontal
    ],
    'ト': [  # to - 2 strokes
        [(0, -55), (0, -25), (0, 5), (0, 30)],  # Stroke 1: Vertical
        [(-30, 15), (-10, 20), (15, 23), (35, 25)]  # Stroke 2: Horizontal
    ],
    
    # N sounds ナ行
    'ナ': [  # na - 2 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (8, -15), (5, 15), (0, 40)]  # Stroke 2: Diagonal down-left
    ],
    'ニ': [  # ni - 2 strokes
        [(-35, -20), (-15, -15), (10, -12), (30, -10)],  # Stroke 1: Top horizontal
        [(-30, 20), (-10, 25), (15, 28), (35, 30)]  # Stroke 2: Bottom horizontal
    ],
    'ヌ': [  # nu - 2 strokes
        [(-25, -40), (-10, -25), (10, -5), (25, 10)],  # Stroke 1: Diagonal
        [(0, 15), (5, 30), (10, 43), (12, 55)]  # Stroke 2: Vertical down
    ],
    'ネ': [  # ne - 4 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (10, -15), (10, 15)],  # Stroke 2: Short vertical
        [(-25, 5), (-5, 10), (20, 13), (40, 15)],  # Stroke 3: Middle horizontal
        [(15, 18), (20, 30), (25, 42), (28, 52)]  # Stroke 4: Diagonal down
    ],
    'ノ': [  # no - 1 stroke
        [(-15, -50), (-5, -25), (5, 0), (15, 30), (20, 50)]  # Single diagonal
    ],
    
    # H sounds ハ行
    'ハ': [  # ha - 2 strokes
        [(-20, -40), (-10, -20), (0, 5), (5, 30)],  # Stroke 1: Left diagonal
        [(10, -45), (15, -25), (20, 0), (22, 35)]  # Stroke 2: Right diagonal
    ],
    'ヒ': [  # hi - 2 strokes
        [(-30, -30), (-10, -25), (15, -22), (35, -20)],  # Stroke 1: Top horizontal
        [(-25, 20), (-5, 25), (20, 28), (40, 30)]  # Stroke 2: Bottom horizontal
    ],
    'フ': [  # fu - 2 strokes
        [(-35, -30), (-15, -25), (10, -22), (30, -20)],  # Stroke 1: Top horizontal
        [(25, -25), (20, 0), (15, 25), (12, 45)]  # Stroke 2: Vertical down
    ],
    'ヘ': [  # he - 1 stroke
        [(-35, -10), (-15, 5), (10, 15), (30, 20)]  # Single diagonal
    ],
    'ホ': [  # ho - 4 strokes
        [(0, -55), (0, -25), (0, 5), (0, 35)],  # Stroke 1: Vertical center
        [(-35, -20), (-10, -15), (15, -12), (35, -10)],  # Stroke 2: Top horizontal
        [(-30, 20), (-10, 25), (15, 28), (35, 30)],  # Stroke 3: Bottom horizontal
        [(20, -30), (20, 0), (20, 30)]  # Stroke 4: Right vertical
    ],
    
    # M sounds マ行
    'マ': [  # ma - 2 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (8, -15), (5, 15), (0, 40)]  # Stroke 2: Diagonal down
    ],
    'ミ': [  # mi - 3 strokes
        [(-30, -30), (-15, -15), (0, 0)],  # Stroke 1: Top diagonal
        [(-20, 5), (-5, 15), (10, 25)],  # Stroke 2: Middle diagonal
        [(-10, 30), (5, 40), (20, 48)]  # Stroke 3: Bottom diagonal
    ],
    'ム': [  # mu - 2 strokes
        [(0, -50), (-10, -20), (-15, 10), (-10, 35)],  # Stroke 1: Left curve
        [(0, -50), (10, -20), (15, 10), (10, 35)]  # Stroke 2: Right curve
    ],
    'メ': [  # me - 2 strokes
        [(-30, -40), (-10, -15), (10, 15), (25, 40)],  # Stroke 1: Diagonal down-right
        [(30, -35), (10, -10), (-10, 20), (-25, 45)]  # Stroke 2: Diagonal down-left
    ],
    'モ': [  # mo - 3 strokes
        [(-30, -35), (-10, -30), (15, -27), (35, -25)],  # Stroke 1: Top horizontal
        [(-25, 5), (-5, 10), (20, 13), (40, 15)],  # Stroke 2: Middle horizontal
        [(10, -40), (10, -10), (10, 20), (10, 45)]  # Stroke 3: Vertical
    ],
    
    # Y sounds ヤ行
    'ヤ': [  # ya - 3 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(-25, 15), (-5, 20), (20, 23), (40, 25)],  # Stroke 2: Bottom horizontal
        [(10, -45), (10, -15), (10, 15), (10, 40)]  # Stroke 3: Vertical
    ],
    'ユ': [  # yu - 2 strokes
        [(-35, -20), (-15, -15), (10, -12), (30, -10)],  # Stroke 1: Top horizontal
        [(0, 10), (10, 25), (20, 38), (30, 48)]  # Stroke 2: Diagonal
    ],
    'ヨ': [  # yo - 3 strokes
        [(-35, -30), (-15, -25), (10, -22), (30, -20)],  # Stroke 1: Top horizontal
        [(-30, 5), (-10, 10), (15, 13), (35, 15)],  # Stroke 2: Middle horizontal
        [(-25, 30), (-5, 35), (20, 38), (40, 40)]  # Stroke 3: Bottom horizontal
    ],
    
    # R sounds ラ行
    'ラ': [  # ra - 2 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (10, -15), (10, 15), (10, 40)]  # Stroke 2: Vertical
    ],
    'リ': [  # ri - 2 strokes
        [(-10, -55), (-8, -25), (-5, 5), (-3, 30)],  # Stroke 1: Left vertical
        [(10, -50), (12, -20), (15, 10), (17, 35)]  # Stroke 2: Right vertical
    ],
    'ル': [  # ru - 2 strokes
        [(-25, -45), (-10, -30), (10, -10), (25, 5)],  # Stroke 1: Diagonal
        [(0, 10), (5, 25), (10, 40), (12, 52)]  # Stroke 2: Vertical down
    ],
    'レ': [  # re - 1 stroke
        [(-30, -40), (-10, -25), (10, -5), (30, 20), (35, 40)]  # Single diagonal
    ],
    'ロ': [  # ro - 3 strokes
        [(-30, -40), (-10, -35), (15, -32), (35, -30)],  # Stroke 1: Top
        [(-35, -40), (-35, -10), (-35, 20), (-35, 45)],  # Stroke 2: Left vertical
        [(35, -30), (35, 0), (35, 30), (35, 50)],  # Stroke 3: Right vertical (box shape)
    ],
    
    # W sounds and N ワ行 + ン
    'ワ': [  # wa - 2 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(10, -45), (8, -15), (5, 15), (0, 40)]  # Stroke 2: Diagonal down
    ],
    'ヲ': [  # wo - 3 strokes
        [(-30, -40), (-10, -35), (15, -30), (35, -28)],  # Stroke 1: Top horizontal
        [(-25, 15), (-5, 20), (20, 23), (40, 25)],  # Stroke 2: Bottom horizontal
        [(10, -45), (10, -15), (10, 15), (10, 40)]  # Stroke 3: Vertical
    ],
    'ン': [  # n - 2 strokes
        [(-25, -40), (-10, -25), (10, -5), (25, 10)],  # Stroke 1: Diagonal
        [(0, 15), (5, 30), (10, 43), (12, 55)]  # Stroke 2: Vertical down
    ],
}

def get_stroke_data(char):
    """Get stroke order data for a given character.
    
    Args:
        char: Japanese character (hiragana or katakana)
    
    Returns:
        List of strokes, where each stroke is a list of (x, y) coordinate tuples.
        Returns None if character not found.
    """
    if char in HIRAGANA_STROKES:
        return HIRAGANA_STROKES[char]
    elif char in KATAKANA_STROKES:
        return KATAKANA_STROKES[char]
    else:
        return None
