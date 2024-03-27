# Overview

## Objectives
This part of the project investigates the relationship between the speed of code review and two specific metrics: social interaction among team members and the expression of positive emotions in comments left on pull requests. The aim is to research the following hypothesis: "If code review speed increases, then social interaction increases, as well as the amount of positive emotions, more so in local teams than to global teams." Looking at the social interaction of contributors, but also the emotion in the comments they leave on pull requests, gives us an insight on the interaction and satisfaction of contributors. More interaction between team members, but also contributors leaving positive comments, can foster a good and healthy relationship within a team. 

## Summary of Findings
The results of the analysis of hypothesis two suggest that in both same-country and global project settings, longer mean first response times correlate with lower social strength. This implies that quick responses in code review processes may contribute to stronger social bonds among team members. The same is true for non-global projects, however the relationship is weaker than that of global projects, meaning the correlation is less significant. <br />
<br />
Additionally, the correlation between mean first response time and overall emotion distribution suggests that slower response times might foster a more positive emotional atmosphere within the team, regardless of the project's geographical scope. <br />
<br />
These findings show that an efficient code review speed may correlate with stronger social bonds in teams, which corresponds with what we expected with our hypothesis. On the other hand, there may be a slightly smaller distribution in comment emotions, which we did not particularly expect. This could mean that with a faster review process, team members are more critical of each other’s work or that they try to be more efficient by not particularly conveying emotions. However, the scope of this research is too small to properly provide any reasoning.

# Methodology

## Data Acquisition
This hypothesis also makes use of the Xunhui Zhang, Ayushi Rastogi, and Yue Yu “On the Shoulders of Giants” dataset, which contains information of pull requests from a large number of software development projects on Github. This dataset can be found here: https://zenodo.org/records/3922907. Next to this, we also collected data from Github itself, using their API. With Python code we looked at all the projects in the dataset, and collected how many contributors worked on each project, as this was missing from the original dataset. 

## Data Preparation

### Team Size Definition: 
In this hypothesis, we defined a ‘small team’ as having 12 or less contributors to the project. This corresponds with the definition used in “On the Shoulders of Giants”.

### Global Collaboration Definition: 
We looked at global collaboration from two different angles: by looking purely at the contributors of the pull requests of a project, and by looking at the contributor and reviewer of a pull request. For the former metric we looked at the country of the contributors: if there were at least two different countries, we considered a project global. If all contributors in a project were from the same country, the project was seen as local. Moreover, we also compared whether a contributor and reviewer were from the same country to see whether this has any impact.

## Statistical Analysis
The mean first response time per project was calculated as a measure of review speed. Prior to this, we filtered the dataset to remove any pull requests where the first response time had a negative value, as these were considered outliers. <br />
<br />
General emotions per pull request were calculated by subtracting the percentage of negative emotions (perc_neg_emotion) from the percentage of positive emotions (perc_pos_emotion) observed in the comments. Social interaction was defined by the social_strength metric, which represents the fraction of team members that interacted with the contributor in the last three months. <br />
<br />
To investigate the relationship between the review speed and the additional metrics, we performed Pearson correlation tests. This was done for both the global and local groups, as well as the same country and non same country groups. 

# How to replicate the study

## Prepare Necessary Files
Download the dataset from https://zenodo.org/records/3922907 and place the file in the same folder as the Python files. To skip the collection of the project contributors, ensure that `project_contributor_count.csv` is also downloaded and present in the same folder.

## Contributor Count 
The file `contributor.py` contains the script used to retrieve the contributor count for each of the projects. It is defined such that it can be run in batches, only making requests for a subset of the data. This was done because the GitHub API has a rate limit of 5000 when using an authentication token. Moreover, the GET request only returns the first page of contributors of a repository, which has 30 contributors at most. This was not a problem for our scenario, as we only want to filter for projects with 12 or less contributors, but this should be changed if the requirements are different.

## Analysis
The file `hypothesis.py` is the file used to do the statistical analysis. It first filters the dataset to keep only the small projects using the results of `contributor.py` and then filters the dataset to only keep needed columns. Next, we ensure that rows with missing values or outliers in response time are removed. Afterwards, we obtain the needed additional metrics such as mean_project_first_response_time and global. This gives us our final dataset on which we perform the statistics. 