import pandas as pd


def split_csv(input_file, output_prefix='output', num_parts=10):
    # Read the CSV file into a pandas DataFrame, skipping the header
    df = pd.read_csv(input_file, header=None, skiprows=1)

    # Calculate the number of rows in each part, ensuring no rows are lost
    rows_per_part = (len(df) + num_parts - 1) // num_parts

    # Split the DataFrame into parts
    parts = [df.iloc[i:i + rows_per_part] for i in range(0, len(df), rows_per_part)]

    # Save each part to a separate CSV file
    for i, part in enumerate(parts, start=1):  # Start the enumeration from 1
        output_file = f'{output_prefix}_{i}.csv'  # Adjusted the output file naming
        part.to_csv(output_file, index=False, header=False)  # Skip writing headers
        print(f'Part {i} saved to {output_file}')


if __name__ == '__main__':
    split_csv('../data/csv/pytania_edustrefa.csv', output_prefix='../data/csv/pytania')
