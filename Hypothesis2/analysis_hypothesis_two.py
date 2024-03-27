import pandas as pd
from scipy.stats import pearsonr

pd.set_option('display.float_format', lambda x: '%.3f' % x)


# Filter the dataset to only keep small projects
def filter_dataset():
    data = pd.read_csv('new_pullreq.csv')

    # Dataset with project_ids and number of contributors
    contrib_list = pd.read_csv('project_contributor_count.csv')

    # Filter 'contrib_list' to keep only project_ids where 1 < contributor_count <= 12
    filtered_contrib_list = contrib_list[
        (contrib_list['contributor_count'] > 1) & (contrib_list['contributor_count'] <= 12)]

    # Merge 'filtered_df' with 'filtered_contrib_list' based on 'project_id'
    merged_df = pd.merge(data, filtered_contrib_list, on='project_id', how='inner')

    # Save the filtered DataFrame to a new CSV file
    merged_df.to_csv('merged_small_project_dataset.csv', index=False)


def calculate_project_stats(dataset):
    # Group the DataFrame by 'project_id' and calculate the mean of 'first_response_time' for each group
    grouped_dataset = dataset.groupby('project_id')['first_response_time'].mean().reset_index()
    grouped_dataset.rename(columns={'first_response_time': 'mean_project_first_response_time'}, inplace=True)

    # Calculate the unique number of 'contrib_country' for each 'project_id' in the dataset
    unique_contrib_country_counts = dataset.groupby('project_id')['contrib_country'].nunique().reset_index(
        name='unique_country_count')

    merged_dataset = pd.merge(grouped_dataset, unique_contrib_country_counts, on='project_id', how='left')

    # Add the 'global' column based on the condition whether 'unique_country_count' is equal to 1
    merged_dataset['global'] = merged_dataset['unique_country_count'].apply(lambda x: 0 if x == 1 else 1)
    merged_dataset.drop(columns=['unique_country_count'], inplace=True)

    # Merge the merged_dataset with the original dataset to get the other columns
    return pd.merge(merged_dataset, dataset, on='project_id', how='inner')


def hypothesis_two(dataset):
    print("\n### Hypothesis 2 ###")
    print("\n### Mean first response time correlated Social strength distribution depending on same_country\n")
    same_country = dataset[dataset['same_country'] == 1]
    non_same_country = dataset[dataset['same_country'] == 0]

    print("Same_country:", pearsonr(same_country['mean_project_first_response_time'], same_country['social_strength']))
    print("Non_same_country",
          pearsonr(non_same_country['mean_project_first_response_time'], non_same_country['social_strength']))

    print("\n### Mean first response time correlated with Social strength depending on if a project is global\n")
    global_ds = dataset[dataset['global'] == 1]
    non_global_ds = dataset[dataset['global'] == 0]

    print("Global:", pearsonr(global_ds['mean_project_first_response_time'], global_ds['social_strength']))
    print("Non_global", pearsonr(non_global_ds['mean_project_first_response_time'], non_global_ds['social_strength']))


def hypothesis_three(dataset):
    print("\n### Hypothesis 3 ###")
    # Overall emotion distribution, calculated by subtracting the negative emotion from the positive emotion
    dataset['overall_emotion'] = dataset['perc_pos_emotion'] - dataset['perc_neg_emotion']

    print("\n### Mean first response time correlated with overall emotion distribution depending on same_country\n")
    same_country = dataset[dataset['same_country'] == 1]
    non_same_country = dataset[dataset['same_country'] == 0]

    print("Same_country:", pearsonr(same_country['mean_project_first_response_time'], same_country['overall_emotion']))
    print("Non_same_country",
          pearsonr(non_same_country['mean_project_first_response_time'], non_same_country['overall_emotion']))

    print("\n### Mean first response time correlated with overall emotion depending on if a project is global\n")
    global_ds = dataset[dataset['global'] == 1]
    non_global_ds = dataset[dataset['global'] == 0]

    print("Global:", pearsonr(global_ds['mean_project_first_response_time'], global_ds['overall_emotion']))
    print("Non_global", pearsonr(non_global_ds['mean_project_first_response_time'], non_global_ds['overall_emotion']))


if __name__ == '__main__':
    # filter_dataset()

    columns_to_keep = ['id', 'project_id', 'reponame', 'perc_neg_emotion',
                       'perc_pos_emotion', 'perc_neu_emotion', 'first_response_time', 'same_country', 'contrib_country',
                       'social_strength']

    dataset = pd.read_csv('merged_small_project_dataset.csv')[columns_to_keep]

    print("Number of distinct project_ids:", dataset['project_id'].nunique())

    # Remove all the rows that are missing values in any of the columns
    dataset = dataset.dropna(axis=0, how='any')

    # Remove all the projects where 'first_response_time' is less than or equal to 0
    dataset = dataset[dataset['first_response_time'] > 0]

    # Add global and mean_project_first_response_time columns to the dataset per project
    dataset = calculate_project_stats(dataset)

    # Perform correlation tests
    hypothesis_two(dataset.copy())
    hypothesis_three(dataset.copy())

    # Print number of unique projects
    print(dataset['project_id'].nunique())
    print(len(dataset))
