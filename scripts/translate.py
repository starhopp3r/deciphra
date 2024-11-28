import re
import pandas as pd


# Load xlit map from xlits.csv
def load_xlitmap(filepath):
    xlits_df = pd.read_csv(filepath, dtype=str, keep_default_na=False)
    xlitmap = {}
    for _, row in xlits_df.iterrows():
        sign = row.get('sign')
        xlitmap[sign] = {
            'xlit': row.get('xlit'),
            'canonical': row.get('canonical'),
            'regex': row.get('regex')
        }
    return xlitmap


# Transliterate text based on xlit map
def xlitize(text, xlitmap):
    re_digits = re.compile(r'(\d+)')
    # Reverse the order
    results = re_digits.findall(text)[::-1]
    str_xlit = ''
    for idx, digit in enumerate(results):
        sign = xlitmap.get(digit)
        if idx == 0:
            str_xlit = sign['xlit']
            continue
        if re.match(r'^.*([iu]|an|as)$', str_xlit) is None and \
           re.match(r'^[aiu]$', sign['xlit']) is None and not str_xlit.endswith('.'):
            str_xlit += 'a'
        str_xlit += '-' + sign['xlit']
    # Finalize xlit
    if re.match(r'.*([iu]|an|as)$', str_xlit) is None:
        str_xlit += 'a'
    str_xlit = '-'.join(str_xlit.split('-')[::-1])
    return str_xlit


# Process inscriptions and translate text
def translate_data(data_filepath, xlit_filepath, output_filepath):
    processed_data = []
    xlitmap = load_xlitmap(xlit_filepath)
    df = pd.read_csv(data_filepath, dtype=str, keep_default_na=False)
    for _, row in df.iterrows():
        id = row.get('id')
        text = row.get('text')
        xlit = xlitize(text, xlitmap)
        plaintext = ''.join(xlit.split('-')[::-1])
        processed_data.append({'id': id, 'text': text, 'xlit': xlit, 'plaintext': plaintext})
    translated_df = pd.DataFrame(processed_data)
    translated_df.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    translate_data(
        data_filepath='../data/indus-inscriptions.csv',
        xlit_filepath='../data/xlits.csv',
        output_filepath='../data/indus-translated.csv'
    )