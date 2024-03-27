import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset and display initial statistics
file_path = 'new_pullreq.csv'
data = pd.read_csv(file_path)

print(f"Total number of pull requests before filtering: {data.size}\n"
      f"Number of unique project IDs before filtering: {data['project_id'].nunique()}")

# Finding the maximum team size for each project to identify small teams
project_team_sizes = data.groupby('project_id')['team_size'].max().reset_index()
threshold = project_team_sizes['team_size'].quantile(0.33)  # Threshold for small teams

# Identifying and filtering small team projects
small_teams_project_ids = project_team_sizes[project_team_sizes['team_size'] <= threshold]['project_id']
small_teams_data = data[data['project_id'].isin(small_teams_project_ids)]

print(f"Threshold for small teams: {threshold}\n"
      f"Number of projects considered small: {small_teams_project_ids.size}\n"
      f"Number of pull requests made by small teams: {small_teams_data.size}")

# Categorizing projects
global_collab_projects = set()
non_global_collab_projects = set()

for project_id in small_teams_project_ids:
    project_data = small_teams_data[small_teams_data['project_id'] == project_id]
    if any(project_data['same_country'] == False):
        global_collab_projects.add(project_id)
    else:
        non_global_collab_projects.add(project_id)

# Filtering data
global_collab_small_teams = small_teams_data[small_teams_data['project_id'].isin(global_collab_projects)]
non_global_collab_small_teams = small_teams_data[small_teams_data['project_id'].isin(non_global_collab_projects)]

print(f"Number of small team projects with global collaboration: {len(global_collab_projects)}\n"
      f"Number of small team projects with non-global collaboration: {len(non_global_collab_projects)}")

def analyze_correlation(data, title):
    # Calculating correlations
    corr_pr_comments = data['first_response_time'].corr(data['pr_comment_num'])
    corr_participants = data['first_response_time'].corr(data['num_participants'])

    print(f"{title} Correlations:\n"
          f"First Response Time vs. PR Comments: {corr_pr_comments}\n"
          f"First Response Time vs. Number of Participants: {corr_participants}")

    # Setting up plots
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # PR Comments plot
    sns.scatterplot(x='first_response_time', y='pr_comment_num', data=data, ax=ax[0])
    ax[0].set_title(f"{title} - First Response Time vs. PR Comments")

    # Participants plot
    sns.scatterplot(x='first_response_time', y='num_participants', data=data, ax=ax[1])
    ax[1].set_title(f"{title} - First Response Time vs. Number of Participants")

    plt.tight_layout()

    # Saving the plots as PNG images
    figure_filename = title.replace(" ", "_").lower() + '_correlation_plots.png'
    plt.savefig(figure_filename)
    plt.show()

print("Analyzing Global Collaboration within Small Teams:")
analyze_correlation(global_collab_small_teams, "Global Collaboration")

print("Analyzing Non-Global Collaboration within Small Teams:")
analyze_correlation(non_global_collab_small_teams, "Non-Global Collaboration")
