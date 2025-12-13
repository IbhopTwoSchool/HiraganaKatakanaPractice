# Stroke Order Resources

## Online Stroke Order Demonstrations

### 1. **KanjiVG Project**
- **URL**: https://github.com/KanjiVG/kanjivg
- **URL (Web Viewer)**: https://kanjivg.tagaini.net/
- **Description**: Vector graphics for kanji stroke orders. While primarily for kanji, this is the gold standard for stroke order data in SVG format.
- **Format**: SVG files with stroke path data
- **License**: Creative Commons Attribution-Share Alike 3.0

### 2. **Wiktionary Stroke Order Diagrams**
- **URL**: https://en.wiktionary.org/wiki/あ (example for hiragana "a")
- **Description**: Each hiragana/katakana character page on Wiktionary includes stroke order diagrams
- **Format**: Static images showing stroke order with numbers and arrows
- **Example URLs**:
  - あ: https://en.wiktionary.org/wiki/あ
  - か: https://en.wiktionary.org/wiki/か
  - さ: https://en.wiktionary.org/wiki/さ
  - た: https://en.wiktionary.org/wiki/た
  - な: https://en.wiktionary.org/wiki/な
  - は: https://en.wiktionary.org/wiki/は
  - ま: https://en.wiktionary.org/wiki/ま
  - や: https://en.wiktionary.org/wiki/や
  - ら: https://en.wiktionary.org/wiki/ら
  - わ: https://en.wiktionary.org/wiki/わ

### 3. **Wikipedia Hiragana Stroke Order Table**
- **URL**: https://en.wikipedia.org/wiki/Hiragana#Stroke_order_and_direction
- **Description**: Complete table showing stroke order for all hiragana characters
- **Format**: SVG image with all hiragana stroke orders
- **Direct Image**: https://en.wikipedia.org/wiki/File:Table_hiragana.svg

### 4. **Hiragana/Katakana Practice Sites with Animations**

#### A. **KanjiKana.com**
- **URL**: https://kanjikana.com/en/hiragana
- **Description**: Interactive stroke animations for each hiragana character
- **Features**: 
  - Animated stroke-by-stroke demonstrations
  - Shows stroke direction with arrows
  - Includes stroke order numbers

#### B. **Jisho.org**
- **URL**: https://jisho.org/
- **Description**: Japanese dictionary with drawing recognition
- **Features**: 
  - Draw characters to search
  - Shows proper stroke order when you look up characters
  - Has kanji/kana search with stroke animations

#### C. **NHK World Hiragana/Katakana Chart**
- **URL**: https://www.nhk.or.jp/lesson/english/syllabary/hiragana_english.pdf
- **Description**: Official NHK stroke order charts (PDF)
- **Format**: Downloadable PDF with stroke diagrams

### 5. **Wikimedia Commons**
- **URL**: https://commons.wikimedia.org/wiki/Category:Stroke_order_diagrams
- **Description**: Collection of stroke order diagram images
- **Format**: Static SVG/PNG images showing numbered strokes
- **License**: Various Creative Commons licenses

### 6. **YouTube Video Demonstrations**
Search for:
- "hiragana stroke order animation"
- "katakana stroke order writing"
- "how to write hiragana"

### 7. **Japanese Learning Apps with Animations**
- **Duolingo**: Has stroke animations in Japanese course
- **LingoDeer**: Includes stroke order animations
- **Drops**: Visual stroke-by-stroke animations

## Data Sources for Integration

### For Direct Integration into Code:

1. **KanjiVG SVG Data** (Best option)
   - Clone: `git clone https://github.com/KanjiVG/kanjivg.git`
   - Parse SVG path data from files
   - Convert to coordinate arrays for pygame rendering

2. **Wiktionary Images** (Alternative)
   - Download static stroke order images
   - Display alongside practice area
   - Example: https://commons.wikimedia.org/wiki/File:Hiragana_a_stroke_order_animation.gif

3. **Custom Data Entry**
   - Manually trace characters using stroke order guides
   - Record coordinate sequences from reference images
   - Store in stroke_order_data.py format

## Recommended Approach for This Program

### Option 1: Add Reference Image Display
- Download stroke order GIFs/PNGs from Wikimedia Commons
- Display reference animation in corner of screen
- Show one stroke at a time synchronized with user progress

### Option 2: Parse KanjiVG Data
- Extract hiragana/katakana from KanjiVG repository
- Convert SVG paths to pygame coordinate arrays
- Much more accurate than current manual data

### Option 3: Link to External Resources
- Add button to open character on Wiktionary/KanjiKana
- Let users reference proper stroke order externally
- Keep program lightweight

## Current Implementation Note

The stroke data in `stroke_order_data.py` appears to be manually created with coordinate ranges from -60 to +60. To improve accuracy:

1. Compare with authoritative sources (KanjiVG, Wiktionary)
2. Verify stroke directions match traditional calligraphy
3. Consider extracting data programmatically from SVG sources

## License Compatibility

Most resources use Creative Commons licenses compatible with open-source projects:
- **KanjiVG**: CC BY-SA 3.0 (requires attribution, share-alike)
- **Wikimedia**: Various CC licenses (check individual files)
- **Wikipedia content**: CC BY-SA 3.0 / GFDL

Be sure to include proper attribution if using these resources.
