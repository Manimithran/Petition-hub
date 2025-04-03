def unicode_to_bamini(unicode_text):
    # Mapping of Unicode Tamil to Bamini encoding
    unicode_to_bamini_map = {
        'அ': 'm',
        'ஆ': 'M',
        'இ': ',',
        'ஈ': '<',
        'உ': 'c',
        'ஊ': 'C',
        'எ': 'v',
        'ஏ': 'V',
        'ஐ': 'I',
        'ஒ': 'x',
        'ஓ': 'X',
        'ஔ': 'xs',
        'க்': 'f;',
        'ங்': 'q;',
        'ச்': 'r;',
        'ஞ்': 'Q;',
        'ட்': 'l;',
        'ண்': 'z;',
        'த்': 'j;',
        'ந்': 'e;',
        'ப்': 'g;',
        'ம்': 'k;',
        'ய்': 'a;',
        'ர்': 'u;',
        'ல்': 'y;',
        'வ்': 't;',
        'ழ்': 'o;',
        'ள்': 's;',
        'ற்': 'w;',
        'ன்': 'd;',
        'க': 'f',
        'ங': 'q',
        'ச': 'r',
        'ஞ': 'Q',
        'ட': 'l',
        'ண': 'z',
        'த': 'j',
        'ந': 'e',
        'ப': 'g',
        'ம': 'k',
        'ய': 'a',
        'ர': 'u',
        'ல': 'y',
        'வ': 't',
        'ழ': 'o',
        'ள': 's',
        'ற': 'w',
        'ன': 'd',
        'ா': 'h',
        'ி': 'p',
        'ீ': 'P',
        'ு': 'U',
        'ூ': '\\+',
        'ெ': 'n',
        'ே': 'N',
        'ை': 'i',
        'ொ': 'nh',
        'ோ': 'Nh',
        'ௌ': 'ns',
        '்': ';',
        # Add more mappings as needed
    }
    
    result = ''
    i = 0
    while i < len(unicode_text):
        found = False
        # Try to match longer sequences first
        for length in range(2, 0, -1):
            if i + length <= len(unicode_text):
                substr = unicode_text[i:i+length]
                if substr in unicode_to_bamini_map:
                    result += unicode_to_bamini_map[substr]
                    i += length
                    found = True
                    break
        if not found:
            # If no mapping found, keep the original character
            result += unicode_text[i]
            i += 1
    
    return result 