import pandas as pd

list_of_states = [
    'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
    'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
                  ]


# combine acceptance data from 2001 to 2021
def combine_acceptance_data():
    combined_acceptance_data = {}
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

            if id not in combined_acceptance_data:
                combined_acceptance_data[id] = {}
                combined_acceptance_data[id]['name'] = name
                combined_acceptance_data[id]['state'] = state

            combined_acceptance_data[id][year] = admit_rate if admit_rate != 1 else None

        print(f"Finished Combining Acceptance Rates {year}")

    # write to a new csv
    df = pd.DataFrame.from_dict(combined_acceptance_data, orient='index')
    df.to_csv('combined_acceptance_data.csv')


# process average difference data per state from 2002 to 2021
def process_acceptance_data():
    data = pd.read_csv("combined_acceptance_data.csv")

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

        print(f"Finished Processing Acceptance Rates {year}")

    df = pd.DataFrame.from_dict(avg, orient='index')
    df.to_csv('avg_acceptance_diff_data.csv')


# combine SAT data from 2001 to 2021
def combine_sat_data():
    combined_sat_data = {}
    for year in range(2001, 2022):
        data = pd.read_csv(f"./MERGED{year}.csv")

        # get a column's data and put into combined_data
        for index, row in data.iterrows():
            state = row['STABBR']

            if state not in list_of_states:
                continue

            id = row['UNITID']
            name = row['INSTNM']
            sat_avg = row['SAT_AVG_ALL']

            if id not in combined_sat_data:
                combined_sat_data[id] = {}
                combined_sat_data[id]['name'] = name
                combined_sat_data[id]['state'] = state

            combined_sat_data[id][year] = sat_avg if sat_avg != 1 else None

        print(f"Finished Combining SAT {year}")

    # write to a new csv
    df = pd.DataFrame.from_dict(combined_sat_data, orient='index')
    df.to_csv('combined_sat_data.csv')


# process average difference in SAT score per state from 2002 to 2021
def process_sat_data():
    data = pd.read_csv("combined_sat_data.csv")

    avg = {}
    for year in range(2002, 2022):
        for index, row in data.iterrows():
            state = row["state"]
            name = row["name"]
            current_sat = row[str(year)] if not pd.isna(row[str(year)]) else None
            prev_sat = row[str(year - 1)] if not pd.isna(row[str(year - 1)]) else None
            diff = current_sat - prev_sat if current_sat is not None and prev_sat is not None else None

            if diff is None:
                continue

            if state not in avg:
                avg[state] = {}

            if year not in avg[state]:
                avg[state][year] = []

            avg[state][year].append(diff)

        for state in avg:
            try:
                avg[state][year] = sum(avg[state][year]) / len(avg[state][year])
            except KeyError:
                pass

        print(f"Finished Processing SAT {year}")

    df = pd.DataFrame.from_dict(avg, orient='index')
    df.to_csv('avg_sat_diff_data.csv')


# find the avg acceptance rate and sat of all schools in the US per year
def us_avg():
    data_ar = pd.read_csv("combined_acceptance_data.csv")
    data_sat = pd.read_csv("combined_sat_data.csv")

    avg = {}

    for year in range(2001, 2022):
        avg[year] = {}
        avg[year]['ar'] = 0
        avg[year]['sat'] = 0

    for year in range(2001, 2022):
        total_ar = 0
        count_ar = 0
        total_sat = 0
        count_sat = 0
        for index, row in data_ar.iterrows():
            current_ar = row[str(year)] if not pd.isna(row[str(year)]) else None

            if current_ar is not None:
                total_ar += current_ar
                count_ar += 1

        avg[year]['ar'] = total_ar / count_ar

        for index, row in data_sat.iterrows():
            current_sat = row[str(year)] if not pd.isna(row[str(year)]) else None

            if current_sat is not None:
                total_sat += current_sat
                count_sat += 1

        avg[year]['sat'] = total_sat / count_sat

        print(f"Finished Averaging {year}")

    df = pd.DataFrame.from_dict(avg, orient='index')
    df.to_csv('us_avg_data.csv')


# find the average change in acceptance rate and sat scores per year of the top 20 schools from 2002 to 2021
def top20_avg_diff():
    data_ar = pd.read_csv("top20_acceptance.csv")
    data_sat = pd.read_csv("top20_sat.csv")

    avg = {}

    for year in range(2002, 2022):
        avg[year] = {}
        avg[year]['ar'] = []
        avg[year]['sat'] = []

    for year in range(2002, 2022):
        for index, row in data_ar.iterrows():
            current_ar = row[str(year)] if not pd.isna(row[str(year)]) else None
            prev_ar = row[str(year - 1)] if not pd.isna(row[str(year - 1)]) else None
            diff = current_ar - prev_ar if current_ar is not None and prev_ar is not None else None

            if diff is None:
                continue

            avg[year]['ar'].append(diff)

        avg[year]['ar'] = sum(avg[year]['ar']) / len(avg[year]['ar'])

        for index, row in data_sat.iterrows():
            current_sat = row[str(year)] if not pd.isna(row[str(year)]) else None
            prev_sat = row[str(year - 1)] if not pd.isna(row[str(year - 1)]) else None
            diff = current_sat - prev_sat if current_sat is not None and prev_sat is not None else None

            if diff is None:
                continue

            avg[year]['sat'].append(diff)

        avg[year]['sat'] = sum(avg[year]['sat']) / len(avg[year]['sat'])

        print(f"Finished Averaging T20 {year}")

    df = pd.DataFrame.from_dict(avg, orient='index')
    df.to_csv('top20_avg_diff_data.csv')


if __name__ == '__main__':
    # combine_acceptance_data()
    # process_acceptance_data()

    # combine_sat_data()
    # process_sat_data()

    # us_avg()

    top20_avg_diff()

    pass
