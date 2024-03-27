import pandas as pd
import requests
from collections import defaultdict
import csv
from datetime import datetime


# Make a GET request to the API to get the number of contributors for a repository
def get_contributor_count(owner, repo, access_token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contributors = response.json()
        return len(contributors), None  # Return the number of contributors and None for error
    else:
        print(f"Error fetching contributors for {owner}/{repo}: {response.status_code}")
        return None, response.status_code  # Return None for count and status code for error


# Function to get contributor count for each project
def get_project_contributor_count(dataset, start_index, batch_size):
    # Group dataset by projectid
    projects = defaultdict(set)  # Use set to store unique repositories for each project
    for index, row in dataset.iterrows():
        project_id = row["project_id"]
        owner = row["ownername"]
        repo = row["reponame"]
        projects[project_id].add((owner, repo))

    print("Number of items in projects:", len(projects))

    # Get contributor count for each project in the specified batch
    project_contributor_count = {}
    for idx, (project_id, repositories) in enumerate(projects.items()):
        total_contributors = 0
        if idx < start_index:
            continue
        if idx >= start_index + batch_size:
            break
        for owner, repo in repositories:
            contributor_count, error_code = get_contributor_count(owner, repo, "GH_Access_token")
            if contributor_count is not None:
                total_contributors += contributor_count
            else:
                # If timed out, return the progress and the error code
                if error_code == 403:  # 403 indicates rate limit exceeded
                    return project_contributor_count, idx, error_code
                elif error_code == 404:  # Repository could not be found, skip over it
                    continue
        project_contributor_count[project_id] = total_contributors

    return project_contributor_count, start_index, None


# Save the contributor_counts to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if the file is empty to write the header only once
            writer.writerow(['project_id', 'contributor_count'])
        for project_id, contributor_count in data.items():
            writer.writerow([project_id, contributor_count])


# Filter original dataset to only include id, project_id, owner, and repo
def filter_dataset():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('new_pullreq.csv')

    columns_to_keep = ['id', 'project_id', 'ownername', 'reponame']

    filtered_df = df[columns_to_keep]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv('filtered_dataset.csv', index=False)


if __name__ == '__main__':
    # Filter the original dataset. This reduces the filesize by a lot by only keeping the columns we will use for the contributor counting
    filter_dataset()

    # Load filtered dataset
    ds = pd.read_csv('filtered_dataset.csv')

    # Define batch size and start index -> With GH API token, a maximum of 5000 request per hour can be made
    batch_size = 5000
    start_index = 0

    print("Current Time =", datetime.now().strftime("%H:%M:%S"))

    project_contributor_count, processed_index, error_code = get_project_contributor_count(ds,
                                                                                           start_index,
                                                                                           batch_size)
    # If a rate limit was reached, print the amount of processed indices, to know where to resume
    if error_code is not None:
        print(f"Timed out at index {processed_index}.")

    save_to_csv(project_contributor_count, 'project_contributor_count.csv')

    print("Written to file")
    print("Current Time =", datetime.now().strftime("%H:%M:%S"))
