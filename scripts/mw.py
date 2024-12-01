import re
import iast_ipa
import pandas as pd
from tqdm import tqdm
from aksharamukha import transliterate


def mw_to_iast_ipa(xml_file, output_csv):
    try:
        # Read the file
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()
        # Find all matches between <key1> and </key1>
        sanskrit_vocab = set()
        pattern = r'<key1>(.*?)</key1>'
        matches = re.findall(pattern, content)
        # Add all matches to the set
        for match in tqdm(matches, desc="Reading dictionary entry"):
            # Convert SLP1 to IAST before adding to set
            sanskrit_vocab.add(transliterate.process('SLP1', 'IAST', match))
        # Create a dataframe with IAST and IPA representations
        result_dict = {word: iast_ipa.transcribe(word) for word in tqdm(sanskrit_vocab, desc="Converting to IPA")}
        # Inform user of count of unique vocab
        print(f"{len(result_dict)} unique words found in the dictionary")
        df = pd.DataFrame(list(result_dict.items()), columns=['IAST', 'IPA'])
        # Sort the dataframe alphabetically
        print("Sorting the dataset by alphabetical order...")
        df = df.sort_values(by='IAST')
        # Export the dataframe to a csv
        df.to_csv(output_csv, index=False)
        print(f"Dataset saved at {output_csv}")
    except FileNotFoundError:
        print(f"File not found: {xml_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
if __name__ == "__main__":
    file_path = "../data/mw.xml"
    output_csv = "../data/mw_iast_ipa.csv"
    mw_to_iast_ipa(file_path, output_csv)