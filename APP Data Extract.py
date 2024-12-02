import pandas as pd

# Prompt user to enter Local Authority Code
local_authority_code = input("Enter the Local Authority Code: ")

#Hard-coded for debugging
#local_authority_code = "E07000223"

sites_columns = ['Closure Reason', 'Closed Date', 'Local Authority Code', 'Local Authority Name', 'Postcode', 'Town', 'Site Name', 'Thoroughfare Name', 'Ownership Type (Text)', 'Site ID']

full_sites_df = pd.read_csv('activeplacescsvs/sites.csv')

# Filter the DataFrame to include only the columns in sites_columns
sites_df = full_sites_df[full_sites_df.columns[full_sites_df.columns.isin(sites_columns)]]

# Create a dictionary to map Local Authority Name to Local Authority Code
name_to_code = sites_df.dropna(subset=["Local Authority Code"]).groupby("Local Authority Name")["Local Authority Code"].first().to_dict()

# Fill missing Local Authority Codes by looking them up in the dictionary
sites_df.loc[:, "Local Authority Code"] = sites_df.apply(
    lambda row: name_to_code.get(row["Local Authority Name"], row["Local Authority Code"]), axis=1
)

# Define the standard columns
standard_columns = ['Closure Reason', 'Closed Date', 'Site ID', 'Facility Type', 'Facility Subtype', 'Facility ID', 'Easting', 'Northing', 'Latitude', 'Longitude', 'Management Type (Text)', 'Accessibility Type (Text)']

# Define the columns to keep for each DataFrame
columns_to_keep = {
    'artificialgrasspitches': standard_columns + ['Pitches'],
    'athletics': standard_columns + ['Oval Track Lanes', 'Straight Track Lanes', 'Track Lanes'],
    'cycling': standard_columns,
    'golf': standard_columns + ['Holes', 'Bays'],
    'grasspitches': standard_columns + ['Pitches'],
    'healthandfitnessgym': standard_columns + ['Stations'],
    'icerinks': standard_columns,
    'indoorbowls': standard_columns + ['Rinks'],
    'indoortenniscentre': standard_columns + ['Courts'],
    'outdoortenniscourts': standard_columns + ['Courts'],
    'skislopes': standard_columns,
    'sportshalls': standard_columns + ['Badminton Courts'],
    'squashcourts': standard_columns + ['Courts'],
    'studios': standard_columns + ['Partitionable Spaces', 'Bike Stations'],
    'swimmingpools': standard_columns + ['Lanes'],
}

# Function to safely read and process CSV
def process_csv(filename, columns_to_keep):
    try:
        df = pd.read_csv(f'activeplacescsvs/{filename}.csv', low_memory=False)
        if df.empty:
            print(f"Warning: {filename}.csv is empty - skipping")
            return None
        # Filter columns
        df = df[df.columns[df.columns.isin(columns_to_keep[filename])]]
        # Check if resulting DataFrame is empty after filtering
        if df.empty:
            print(f"Warning: {filename}.csv has no relevant data after filtering - skipping")
            return None
        return df
    except Exception as e:
        print(f"Warning: Error processing {filename}.csv - {str(e)} - skipping")
        return None

# List to hold all DataFrames
all_dfs = []

# Process each CSV file
for facility_type in columns_to_keep.keys():
    df = process_csv(facility_type, columns_to_keep)
    if df is not None:
        # Check for missing columns
        missing_columns = [col for col in columns_to_keep[facility_type] if col not in df.columns]
        if missing_columns:
            print(f"Warning: The following columns are missing from {facility_type}.csv: {', '.join(missing_columns)}")
        all_dfs.append(df)

# Rest of your code remains the same, starting from here:
# Concatenate all DataFrames into one
if all_dfs:
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Merge combined_df with sites_df on 'Site ID'
    merged_df = pd.merge(combined_df, sites_df, on='Site ID', how='left')

    # Filter rows where both 'Closure Reason' and 'Closed Date' are blank
    merged_df = merged_df[(merged_df["Closure Reason_x"].isnull()) & (merged_df["Closed Date_y"].isnull() & (merged_df["Closure Reason_x"].isnull()) & (merged_df["Closed Date_y"].isnull()))]

    # Filter rows where Local Authority Code doesn't match
    merged_df = merged_df[(merged_df['Local Authority Code'] == local_authority_code)]

    # Convert address details to title case
    merged_df.loc[:, 'Site Name'] = merged_df['Site Name'].str.title()
    merged_df.loc[:, 'Thoroughfare Name'] = merged_df['Thoroughfare Name'].str.title()
    merged_df.loc[:, 'Town'] = merged_df['Town'].str.title()

    # Add new columns 'Unit' and 'Number'
    merged_df = merged_df.assign(Unit='', Number='')

    # Function to populate Unit and Number columns
    def populate_unit_number(row):
        #athletics
        if row['Facility Subtype'] in [1004, 1005, 1008]:
            row['Unit'] = 'Oval Track Lanes'
            row['Number'] = row['Oval Track Lanes']
        elif row['Facility Subtype'] == 1006:
            row['Unit'] = 'Track Lanes'
            row['Number'] = row['Track Lanes']
        elif row['Facility Subtype'] == 1007:
            row['Unit'] = 'n/a'
            row['Number'] = 'n/a'
        elif row['Facility Subtype'] == 1009:
            row['Unit'] = 'Straight Track Lanes'
            row['Number'] = row['Straight Track Lanes']

        #golf
        elif row['Facility Subtype'] == 9002:
            row['Unit'] = 'Holes'
            row['Number'] = row['Holes']
        elif row['Facility Subtype'] == 9001:
            row['Unit'] = 'Holes'
            row['Number'] = row['Holes']
        elif row['Facility Subtype'] == 9003:
            row['Unit'] = 'Bays'
            row['Number'] = row['Bays']

        #studios
        elif row['Facility Subtype'] == 12001:
            row['Unit'] = 'Partitionable Spaces'
            row['Number'] = row['Partitionable Spaces']
        elif row['Facility Subtype'] == 12002:
            row['Unit'] = 'Bike Stations'
            row['Number'] = row['Bike Stations']
    
        elif row['Facility Type'] == 2:
            row['Unit'] = 'Stations'
            row['Number'] = row['Stations']
        elif row['Facility Type'] == 3:
            row['Unit'] = 'Rinks'
            row['Number'] = row['Rinks']
        elif row['Facility Type'] == 4:
            row['Unit'] = 'Courts'
            row['Number'] = row['Courts']
        elif row['Facility Type'] == 5:
            row['Unit'] = 'Pitches'
            row['Number'] = row['Pitches']
        elif row['Facility Type'] == 6:
            row['Unit'] = 'Badminton Courts'
            row['Number'] = row['Badminton Courts']
        elif row['Facility Type'] == 7:
            row['Unit'] = 'Lanes'
            row['Number'] = row['Lanes']
        elif row['Facility Type'] == 8:
            row['Unit'] = 'Pitches'
            row['Number'] = row['Pitches']
        elif row['Facility Type'] == 13:
            row['Unit'] = 'Courts'
            row['Number'] = row['Courts']
        elif row['Facility Type'] == 17:
            row['Unit'] = 'Courts'
            row['Number'] = row['Courts']
        elif row['Facility Type'] in [11, 20, 33]:
            row['Unit'] = 'n/a'
            row['Number'] = 'n/a'
        else:
            row['Unit'] = None
            row['Number'] = None
        return row
    
    # Apply the function to populate the Unit and Number columns
    merged_df = merged_df.apply(populate_unit_number, axis=1)

    # Replace numbers in Facility Type column
    facility_type_dict = {
        1: 'Athletics',
        2: 'Health and Fitness Gym',
        3: 'Indoor Bowls',
        4: 'Indoor Tennis Centre',
        5: 'Grass Pitches',
        6: 'Sports Hall',
        7: 'Swimming Pool',
        8: 'Artificial Grass Pitch',
        9: 'Golf',
        10: 'Ice Rinks',
        11: 'Ski Slopes',
        12: 'Studio',
        13: 'Squash Courts',
        17: 'Outdoor Tennis Courts',
        20: 'Cycling',
        33: 'Gymnastics'
    }

    merged_df['Facility Type'] = merged_df['Facility Type'].replace(facility_type_dict)

    # Perform substitutions in Facility Subtype column
    substitutions = {
        1004: 'Standard Oval Outdoor',
        1005: 'Mini Outdoor',
        1006: 'Compact Outdoor',
        1007: 'Standalone Field',
        1008: 'Standalone Oval Indoor',
        1009: 'Indoor Training',
        2001: 'Health and Fitness Gym',
        3002: 'Indoor Bowls',
        4001: 'Airhall',
        4002: 'Airhall (seasonal)',
        4003: 'Framed Fabric',
        4004: 'Traditional',
        5001: 'Adult Football',
        5002: 'Junior Football 11v11',
        5003: 'Cricket',
        5004: 'Senior Rugby League',
        5005: 'Junior Rugby League',
        5006: 'Senior Rugby Union',
        5007: 'Junior Rugby Union',
        5008: 'Australian Rules Football',
        5009: 'American Football',
        5010: 'Hockey',
        5011: 'Lacrosse',
        5012: 'Rounders',
        5013: 'Baseball',
        5014: 'Softball',
        5015: 'Gaelic Football',
        5016: 'Shinty',
        5017: 'Hurling',
        5018: 'Polo',
        5019: 'Cycling Polo',
        5020: 'Mini Soccer 7v7',
        5021: 'Mini Rugby Union',
        5022: 'Junior Football 9v9',
        5023: 'Mini Soccer 5v5',
        5024: 'Mini Rugby League',
        6001: 'Main',
        6002: 'Activity Hall',
        6003: 'Barns',
        7001: 'Main/General',
        7002: 'Leisure Pool',
        7003: 'Learner/Teaching/Training',
        7004: 'Diving',
        7005: 'Lido',
        8001: 'Sand Filled',
        8002: 'Water Based',
        8003: 'Long Pile Carpet',
        8004: 'Sand Dressed',
        9001: 'Standard',
        9002: 'Par 3',
        9003: 'Driving Range',
        10001: 'Ice Rinks',
        11001: 'Outdoor Artificial',
        11002: 'Outdoor Natural',
        11003: 'Indoor',
        11004: 'Indoor Endless',
        12001: 'Fitness Studio',
        12002: 'Cycle Studio',
        13001: 'Glass-backed',
        13002: 'Normal',
        17001: 'Tennis Courts',
        20001: 'Track - Indoor Velodrome',
        20002: 'Track - Outdoor Velodrome',
        20003: 'BMX - Race Track',
        20004: 'BMX - Pump Track',
        20005: 'Mountain Bike - Trails',
        20006: 'Cycle Speedway - Track',
        20007: 'Road - Closed Road Cycling Circuit',
        33001: 'Gymnastics Hall'
    }

    merged_df['Facility Subtype'] = merged_df['Facility Subtype'].replace(substitutions)

    # Ensure that if Facility Type or Facility Subtype is missing, we populate it from the other column
    def populate_missing_values(row):
        if pd.isnull(row['Facility Type']) and not pd.isnull(row['Facility Subtype']):
            row['Facility Type'] = row['Facility Subtype']
        elif pd.isnull(row['Facility Subtype']) and not pd.isnull(row['Facility Type']):
            row['Facility Subtype'] = row['Facility Type']
        return row

    # Apply the function to the merged dataframe
    merged_df = merged_df.apply(populate_missing_values, axis=1)

    # Define the desired column order for merged dataframes
    desired_columns = [
        'Site Name', 'Thoroughfare Name', 'Town', 'Site ID', 'Postcode', 'Facility Type', 'Facility Subtype', 'Facility ID', 
        'Unit', 'Number', 'Management Type (Text)', 'Ownership Type (Text)', 'Accessibility Type (Text)', 'Local Authority Code', 
        'Local Authority Name', 'Easting', 'Northing', 'Latitude', 'Longitude'
    ]

    # Reorder columns in merged dataframes
    merged_df = merged_df.reindex(columns=desired_columns)

    # Save the filtered DataFrame to a single CSV file
    filtered_filename = (merged_df['Local Authority Name'].iat[0]) + " " + 'active_places.csv'
    merged_df.to_csv(filtered_filename, index=False)
    print(f"Filtered DataFrame saved to {filtered_filename}")
    
else:
    print("No valid files found to combine.")