import pandas as pd

# Read the CSV file into a DataFrame, ensuring 'sign' and 'canonical' are read as strings
df = pd.read_csv('../data/xlits.csv', dtype={'sign': str, 'canonical': str})

# Identify rows where 'xlit' is empty or NaN
empty_xlit_rows = df[df['xlit'].isnull() | (df['xlit'].astype(str).str.strip() == '')]

# Create a mapping from 'sign' to 'xlit' (treating 'sign' as a string)
sign_to_xlit = df.set_index('sign')['xlit'].to_dict()

# Function to compute 'xlit' from 'canonical' components
def compute_xlit(row):
    canonical = row['canonical']
    if pd.isnull(canonical) or canonical.strip() == '':
        return ''
    components = canonical.split('-')
    xlit_components = []
    for comp in components:
        comp = comp.strip()
        if comp == '':
            continue
        # Use the component as is, preserving leading zeros
        xlit = sign_to_xlit.get(comp, '')
        xlit_components.append(xlit)
    # Concatenate the xlits
    new_xlit = ''.join(xlit_components)
    return new_xlit

# Apply the function to 'empty_xlit_rows' and update 'xlit' in 'df'
df.loc[empty_xlit_rows.index, 'xlit'] = empty_xlit_rows.apply(compute_xlit, axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('../data/xlits.csv', index=False)
