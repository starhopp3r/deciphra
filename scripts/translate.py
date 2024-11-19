import re
import pandas as pd


# Load xlitmap from xlits.csv
def load_xlitmap(filepath):
    xlits_df = pd.read_csv(filepath, dtype=str, keep_default_na=False)
    xlitmap = {}
    for _, row in xlits_df.iterrows():
        sign = row.get('sign', '')
        xlitmap[sign] = {
            'xlit': row.get('xlit', ''),
            'random': row.get('xlit', ''),
            'canonical': row.get('canonical', ''),
            'regex': row.get('regex', '')
        }
    return xlitmap


# Transliterate text based on xlitmap
def xlitize(text, xlitmap):
    re_digits = re.compile(r'(\d+)')
    # Reverse the order
    results = re_digits.findall(text)[::-1]
    if not results or results[0] not in xlitmap:
        print(f"Warning: Missing sign {results[0] if results else 'N/A'}")
        return None
    str_xlit, rnd, regex = '', '', ''
    fullrandom = False
    for idx, digit in enumerate(results):
        sign = xlitmap.get(digit)
        if not sign:
            print(f"Warning: Missing sign {digit}")
            continue
        if idx == 0:
            str_xlit = sign['xlit']
            rnd = sign['random']
            regex = sign['xlit']
            continue
        # Check and append 'a' for vowel transitions
        if re.match(r'^.*([iu]|an|as)$', str_xlit) is None and \
           re.match(r'^[aiu]$', sign['xlit']) is None and not str_xlit.endswith('.'):
            str_xlit += 'a'
            regex += 'a?'
        if not fullrandom and \
           re.match(r'^.*([iueofFxX]|an|as)$', rnd) is None and \
           re.match(r'^[aiu]$', sign['random']) is None and not rnd.endswith('.'):
            rnd += 'a'
        str_xlit += '-' + sign['xlit']
        rnd += '-' + sign['random']
        regex += sign['xlit']
    # Finalize xlit and regex
    if re.match(r'.*([iu]|an|as)$', str_xlit) is None:
        str_xlit += 'a'
        regex += 'a?'
    if not fullrandom and re.match(r'.*([iueo]|an|as)$', rnd) is None:
        rnd += 'a'
    str_xlit = '-'.join(str_xlit.split('-')[::-1])
    rnd = '-'.join(rnd.split('-')[::-1])
    description = '-'.join(str_xlit.split('-'))
    return {
        'str': str_xlit,
        'regex': regex,
        'description': description,
        'random': f"⚄ random: {rnd}"
    }


# Process DataFrame and translate text
def translate_data(data_filepath, xlit_filepath, output_filepath):
    xlitmap = load_xlitmap(xlit_filepath)
    df = pd.read_csv(data_filepath, dtype=str, keep_default_na=False)
    # Add columns to the DataFrame
    df['description'] = ''
    df['random'] = ''
    df['regex'] = ''
    df['textlength'] = 0
    df['sanskrit'] = ''
    total_len = total_count = deciphered_len = deciphered_count = 0
    for idx, row in df.iterrows():
        text = row.get('text', '')
        analyzed = xlitize(text, xlitmap)
        if analyzed is None:
            continue
        df.at[idx, 'description'] = analyzed['description']
        df.at[idx, 'random'] = analyzed['random']
        df.at[idx, 'regex'] = analyzed['regex']
        df.at[idx, 'textlength'] = int(row.get('text length', 0))
        if row.get('sanskrit'):
            df.at[idx, 'sanskrit'] = row['sanskrit'].replace('-', '—')
        # Accumulate statistics
        if row.get('complete') == 'Y':
            total_len += df.at[idx, 'textlength']
            total_count += 1
            if row.get('translation'):
                deciphered_len += df.at[idx, 'textlength']
                deciphered_count += 1
        # Reverse the transliterated string for 'sanskrit' field
        df.at[idx, 'sanskrit'] = ''.join(analyzed['str'].split('-')[::-1])
    # Reorganize columns for the output
    output_df = df[['id', 'text', 'description', 'sanskrit', 'translation']].copy()
    output_df.columns = ['id', 'text', 'canonical', 'inscription', 'translation']
    output_df.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    translate_data(
        data_filepath='../data/indus-inscriptions.csv',
        xlit_filepath='../data/xlits.csv',
        output_filepath='../data/indus-translated.csv'
    )
