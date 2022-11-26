import re

range_latin = "\u0000-\u007F\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF"
re_latin = re.compile("[{}]+".format(range_latin))

range_cyrylic = "\u0400-\u04FF\u0500-\u052F"
re_cyrylic = re.compile("[{}]+".format(range_cyrylic), re.UNICODE)

range_korean = "\u1100-\u11FF"
re_korean = re.compile("[{}]+".format(range_korean), re.UNICODE)

range_ja = "\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u3000-\u303F\uFF00-\uFFEF\u3300-\u33FF\uFE30-\uFE4F"
re_ja = re.compile("[{}]+".format(range_ja), re.UNICODE)


ranges = [
    range(int("0530", 16), int("058F", 16)),  # Armenian
    range(int("0590", 16), int("05FF", 16)),  # Hebrew
    range(int("0600", 16), int("06FF", 16)),  # Arabic
    range(int("0700", 16), int("074F", 16)),  # Syriac
    range(int("0900", 16), int("097F", 16)),  # Devanagari
    range(int("0980", 16), int("09FF", 16)),  # Bengali/Assamese
    range(int("0A00", 16), int("0A7F", 16)),  # Gurmukhi
    range(int("0A80", 16), int("0AFF", 16)),  # Gujarati
    range(int("0B00", 16), int("0B7F", 16)),  # Oriya
    range(int("0B80", 16), int("0BFF", 16)),  # Tamil
    range(int("0C00", 16), int("0C7F", 16)),  # Telugu
    range(int("0C80", 16), int("0CFF", 16)),  # Kannada
    range(int("0D00", 16), int("0DFF", 16)),  # Malayalam
    range(int("0D80", 16), int("0DFF", 16)),  # Sinhala
    range(int("0D00", 16), int("0D7F", 16)),  # Malayalam
    range(int("0E00", 16), int("0E7F", 16)),  # Thai
    range(int("0E80", 16), int("0EFF", 16)),  # Lao
    range(int("0F00", 16), int("0FFF", 16)),  # Tibetan
    range(int("1000", 16), int("109F", 16)),  # Myanmar
    range(int("10A0", 16), int("10FF", 16)),  # Georgian
    range(int("1100", 16), int("11FF", 16)),  # Hangul Jamo
    range(int("1200", 16), int("137F", 16)),  # Ethiopic
    range(int("13A0", 16), int("13FF", 16)),  # Cherokee
    range(int("1400", 16), int("167F", 16)),  # Unified Canadian Aboriginal Syllabics
    range(int("1680", 16), int("169F", 16)),  # Ogham
    range(int("1700", 16), int("171F", 16)),  # Tagalog
    range(int("1720", 16), int("173F", 16)),  # Hanunoo
    range(int("1740", 16), int("175F", 16)),  # Buhid
    range(int("1760", 16), int("177F", 16)),  # Tagbanwa
    range(int("1780", 16), int("17FF", 16)),  # Khmer
    range(int("1800", 16), int("18AF", 16)),  # Mongolian
    range(int("1900", 16), int("194F", 16)),  # Limbu
    range(int("1950", 16), int("197F", 16)),  # Tai Le
    range(int("19E0", 16), int("19FF", 16)),  # Khmer Symbols
    range(int("2400", 16), int("243F", 16)),  # Control Pictures
    range(int("2440", 16), int("245F", 16)),  # Optical Character Recognition
    range(int("2500", 16), int("257F", 16)),  # Box Drawing
    range(int("2580", 16), int("259F", 16)),  # Block Elements
    range(int("2800", 16), int("28FF", 16)),  # Braille Patterns
    range(int("2F00", 16), int("2FDF", 16)),  # Kangxi Radicals
    range(int("2FF0", 16), int("2FFF", 16)),  # Ideographic Description Characters
    range(int("3100", 16), int("312F", 16)),  # Bopomofo
    range(int("3130", 16), int("318F", 16)),  # Hangul Compatibility Jamo
    range(int("3190", 16), int("319F", 16)),  # Kanbun (Kunten)
    range(int("31A0", 16), int("31BF", 16)),  # Bopomofo Extended
    range(int("4DC0", 16), int("4DFF", 16)),  # Yijing Hexagram Symbols
    range(int("A000", 16), int("A48F", 16)),  # Yi Syllables
    range(int("A490", 16), int("A4CF", 16)),  # Yi Radicals
    range(int("AC00", 16), int("D7AF", 16)),  # Hangul Syllables
    range(int("D800", 16), int("DBFF", 16)),  # High Surrogate Area
    range(int("DC00", 16), int("DFFF", 16)),  # Low Surrogate Area
    range(int("FB00", 16), int("FB4F", 16)),  # Alphabetic Presentation Forms
    range(int("FB50", 16), int("FDFF", 16)),  # Arabic Presentation Forms-A
    range(int("FE70", 16), int("FEFF", 16)),  # Arabic Presentation Forms-B
    range(int("FE00", 16), int("FE0F", 16)),  # Variation Selectors
    range(int("FE20", 16), int("FE2F", 16)),  # Combining Half Marks
    range(int("FE50", 16), int("FE6F", 16)),  # Small Form Variants
    range(int("FFF0", 16), int("FFFF", 16)),  # Specials
    range(int("10000", 16), int("1007F", 16)),  # Linear B Syllabary
    range(int("10080", 16), int("100FF", 16)),  # Linear B Ideograms
    range(int("10100", 16), int("1013F", 16)),  # Aegean Numbers
    range(int("10300", 16), int("1032F", 16)),  # Old Italic
    range(int("10330", 16), int("1034F", 16)),  # Gothic
    range(int("10380", 16), int("1039F", 16)),  # Ugaritic
    range(int("10400", 16), int("1044F", 16)),  # Deseret
    range(int("10450", 16), int("1047F", 16)),  # Shavian
    range(int("10480", 16), int("104AF", 16)),  # Osmanya
    range(int("10800", 16), int("1083F", 16)),  # Cypriot Syllabary
    range(int("1D000", 16), int("1D0FF", 16)),  # Byzantine Musical Symbols
    range(int("1D100", 16), int("1D1FF", 16)),  # Musical Symbols
    range(int("1D300", 16), int("1D35F", 16)),  # Tai Xuan Jing Symbols
    range(int("1D400", 16), int("1D7FF", 16)),  # Mathematical Alphanumeric Symbols
    range(int("E0000", 16), int("E007F", 16)),  # Tags
    range(int("E0100", 16), int("E01EF", 16)),  # Variation Selectors Supplement
    range(int("3400", 16), int("4DBF", 16)),  # CJK Unified Ideographs Extension A
    range(int("20000", 16), int("2A6DF", 16)),  # CJK Unified Ideographs Extension B
    range(int("2A700", 16), int("2B73F", 16)),  # CJK Unified Ideographs Extension C
    range(int("2B740", 16), int("2B81F", 16)),  # CJK Unified Ideographs Extension D
    range(int("2B820", 16), int("2CEAF", 16)),  # CJK Unified Ideographs Extension E
    range(int("F900", 16), int("FAFF", 16)),  # CJK Compatibility Ideographs
    range(int("2F800", 16), int("2FA1F", 16)),  # CJK Compatibility Ideographs Supl
    range(int("2E80", 16), int("2EFF", 16)),  # CJK Radicals Supplement
    range(int("0750", 16), int("077F", 16)),  # Undefined
    range(int("07C0", 16), int("08FF", 16)),  # Undefined
    range(int("18B0", 16), int("18FF", 16)),  # Undefined
    range(int("1980", 16), int("19DF", 16)),  # Undefined
    range(int("1A00", 16), int("1CFF", 16)),  # Undefined
    range(int("1D80", 16), int("1DFF", 16)),  # Undefined
    range(int("2C00", 16), int("2E7F", 16)),  # Undefined
    range(int("2FE0", 16), int("2EEF", 16)),  # Undefined
    range(int("31C0", 16), int("31EF", 16)),  # Undefined
    range(int("9FB0", 16), int("9FFF", 16)),  # Undefined
    range(int("A4D0", 16), int("ABFF", 16)),  # Undefined
    range(int("D7B0", 16), int("D7FF", 16)),  # Undefined
    range(int("E000", 16), int("F8FF", 16)),  # Private Use Area
    range(int("FE10", 16), int("FE1F", 16)),  # Undefined
    range(int("10140", 16), int("102FF", 16)),  # Undefined
    range(int("104B0", 16), int("107FF", 16)),  # Undefined
    range(int("10840", 16), int("1CFFF", 16)),  # Undefined
    range(int("1D200", 16), int("1D2FF", 16)),  # Undefined
    range(int("1D360", 16), int("1D3FF", 16)),  # Undefined
    range(int("2A6E0", 16), int("2F7FF", 16)),  # Undefined
    range(int("F0000", 16), int("FFFFD", 16)),  # Supplementary Private Use Area-A
    range(int("2FAB0", 16), int("DFFFF", 16)),  # Unused
    range(int("E0080", 16), int("E00FF", 16)),  # Unused
    range(int("FFFFE", 16), int("FFFFF", 16)),  # Unused
    range(int("100000", 16), int("10FFFD", 16)),  # Supplementary Private Use Area-B
    range(int("E01F0", 16), int("EFFFF", 16)),  # Unused
    # Big cleaning
    range(int("0080", 16), int("00FF", 16)),  # C1 Controls and Latin-1 Supplement
    range(int("02B0", 16), int("02FF", 16)),  # Spacing Modifier Letters
    range(int("0300", 16), int("036F", 16)),  # Combining Diacritical Marks
    range(int("1D00", 16), int("1D7F", 16)),  # Phonetic Extensions
    range(int("2070", 16), int("209F", 16)),  # Superscripts and Subscripts
    #
    range(int("0400", 16), int("04FF", 16)),  # Cyrillic
    range(int("0500", 16), int("052F", 16)),  # Cyrillic Supplement
    range(int("0370", 16), int("03FF", 16)),  # Greek/Coptic
    range(int("16A0", 16), int("16FF", 16)),  # Runic
    range(int("1F00", 16), int("1FFF", 16)),  # Greek Extended
    range(int("2150", 16), int("218F", 16)),  # Number Forms
    range(int("2190", 16), int("21FF", 16)),  # Arrows
    range(int("2200", 16), int("22FF", 16)),  # Mathematical Operators
    range(int("2300", 16), int("23FF", 16)),  # Miscellaneous Technical
    range(int("2460", 16), int("24FF", 16)),  # Enclosed Alphanumerics
    range(int("25A0", 16), int("25FF", 16)),  # Geometric Shapes
    range(int("2600", 16), int("26FF", 16)),  # Miscellaneous Symbols
    range(int("1F300", 16), int("1F5FF", 16)),  # Miscellaneous Symbols and Blocks
    range(int("1F900", 16), int("1F9FF", 16)),  # Supplemental Symbols and Pictographs
    range(int("1FA70", 16), int("1FAFF", 16)),  # Symbols and Pictographs Extended-A
    range(int("1F600", 16), int("1F64F", 16)),  # Emoticons
    range(int("1F3FB", 16), int("1F3FF", 16)),  # EMOJI MODIFIER FITZPATRICK
    range(int("1F680", 16), int("1F6FF", 16)),  # Transport and Map Symbols
    range(int("1F100", 16), int("1F1FF", 16)),  # Enclosed Alphanumeric Supplement
    range(int("2700", 16), int("27BF", 16)),  # Dingbats
    range(int("27C0", 16), int("27EF", 16)),  # Miscellaneous Mathematical Symbols-A
    range(int("2980", 16), int("29FF", 16)),  # Miscellaneous Mathematical Symbols-B
    range(int("27F0", 16), int("27FF", 16)),  # Supplemental Arrows-A
    range(int("2900", 16), int("297F", 16)),  # Supplemental Arrows-B
    range(int("2A00", 16), int("2AFF", 16)),  # Supplemental Mathematical Operators
    range(int("2B00", 16), int("2BFF", 16)),  # Miscellaneous Symbols and Arrows
    range(int("20A0", 16), int("20CF", 16)),  # Currency Symbols
    range(int("20D0", 16), int("20FF", 16)),  # Combining Diacritical Marks for Symbols
    range(int("2100", 16), int("214F", 16)),  # Letterlike Symbols
    # Required
    range(int("0000", 16), int("007F", 16)),  # Basic Latin
    range(int("0100", 16), int("017F", 16)),  # Latin Extended-A
    range(int("0180", 16), int("024F", 16)),  # Latin Extended-B
    range(int("1E00", 16), int("1EFF", 16)),  # Latin Extended Additional
    range(int("0250", 16), int("02AF", 16)),  # IPA Extensions
    range(int("2000", 16), int("206F", 16)),  # General Punctuation
    range(int("3040", 16), int("309F", 16)),  # Hiragana
    range(int("30A0", 16), int("30FF", 16)),  # Katakana
    range(int("31F0", 16), int("31FF", 16)),  # Katakana Phonetic Extensions
    range(int("3200", 16), int("32FF", 16)),  # Enclosed CJK Letters and Months
    range(int("3300", 16), int("33FF", 16)),  # CJK Compatibility
    range(int("FE30", 16), int("FE4F", 16)),  # CJK Compatibility Forms
    range(int("3000", 16), int("303F", 16)),  # CJK Symbols and Punctuation
    range(int("4E00", 16), int("9FAF", 16)),  # CJK Unified Ideographs
    range(int("FF00", 16), int("FFEF", 16)),  # Halfwidth and Fullwidth Forms
]
