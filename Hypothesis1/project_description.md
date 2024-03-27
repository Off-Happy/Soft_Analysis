## Project Description

### Overview

This project investigates the interplay between code review speed and team engagement in the context of global collaborations within small project teams. The primary goal is to understand how enhancing review speed may influence engagement levels, especially in globally distributed teams working on small-scale projects. We formulated a hypothesis that suggests that an increase in code review speed could lead to heightened engagement among team members, which is particularly pertinent to teams involved in global collaborations.

Key findings are expected to reveal patterns and strategies that could be employed to optimize review processes, thereby fostering more efficient and cohesive global collaborations in small project environments.

### Methodology

#### Data Acquisition

The study utilizes the dataset provided by Zhang, Xunhui, Ayushi Rastogi, and Yue Yu in their 2020 paper titled "On the shoulders of giants: A new dataset for pull-based development research." This dataset offers comprehensive insights into pull request activities across various projects, serving as a starting element for our analysis. You can download the data set using the following link: https://zenodo.org/records/3922907

#### Analysis Process

1. **Data Preparation**: Initial steps involved cleaning and segmenting the dataset to focus specifically on small projects, classified based on team size thresholds determined from the data. We isolated the projects with team sizes within the smallest third percentile to categorize them as small.

2. **Defining Global and Non-Global Collaboration**: Projects were then categorized into global and non-global collaborations based on the geographical diversity of the team members. This classification enabled targeted analysis of review speeds and engagement in distinct collaboration contexts.

3. **Statistical Analysis**:
   - We computed the first response time to pull requests as a proxy for review speed.
   - Engagement was assessed through metrics like the number of PR comments and the number of participants in the review process.
   - Correlation analysis helped identify the relationships between review speed and engagement indicators.

#### Replication Instructions

The repository includes:
- **Code**: Scripts for data extraction, cleaning, and analysis, clearly annotated to illustrate their function in the methodology.
- **Data**: Datasets are provided to ensure transparency and enable replication.
- **Analysis Scripts**: Detailed statistical analysis scripts are included, with annotations explaining their purpose and functionality.

### Objectives and Expected Outcomes

The project aims to uncover actionable insights that can help optimize review processes in software development, particularly in the context of small, globally distributed teams. By understanding the dynamics between review speed and team engagement, the study seeks to offer recommendations that could enhance both efficiency and collaboration in software development projects.

For results and a brief discussion please see results.md.