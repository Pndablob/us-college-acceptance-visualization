import pandas as pd

list_of_states = [
    'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
    'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
                  ]


# combine data from 2001 to 2021
def combine_data():
    combined_data = {}
    for year in range(2001, 2022):
        data = pd.read_csv(f"./MERGED{year}.csv")

        # get a column's data and put into combined_data
        for index, row in data.iterrows():
            state = row['STABBR']

            if state not in list_of_states:
                continue

            id = row['UNITID']
            name = row['INSTNM']
            admit_rate = row['ADM_RATE_ALL']

            if id not in combined_data:
                combined_data[id] = {}
                combined_data[id]['name'] = name
                combined_data[id]['state'] = state

            combined_data[id][year] = admit_rate if admit_rate != 1 else None

        print(f"Finished Combining {year}")

    # write to a new csv
    df = pd.DataFrame.from_dict(combined_data, orient='index')
    df.to_csv('combined_data.csv')


# process average difference data per state from 2002 to 2021
def process_data():
    data = pd.read_csv("combined_data.csv")

    avg = {}
    for year in range(2002, 2022):
        for index, row in data.iterrows():
            state = row["state"]
            name = row["name"]
            current_ar = row[str(year)] if not pd.isna(row[str(year)]) else None
            prev_ar = row[str(year - 1)] if not pd.isna(row[str(year - 1)]) else None
            diff = current_ar - prev_ar if current_ar is not None and prev_ar is not None else None

            if diff is None:
                continue

            if state not in avg:
                avg[state] = {}

            if year not in avg[state]:
                avg[state][year] = []

            avg[state][year].append(diff)

        for state in avg:
            avg[state][year] = sum(avg[state][year]) / len(avg[state][year])

        print(f"Finished Processing {year}")

    df = pd.DataFrame.from_dict(avg, orient='index')
    df.to_csv('avg_diff_data.csv')


if __name__ == '__main__':
    # combine_data()

    process_data()
