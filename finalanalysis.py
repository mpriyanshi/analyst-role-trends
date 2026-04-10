import pandas as pd
import matplotlib.pyplot as plt

"""
Objective:
Analyze the evolving role of analysts in IT services by comparing demand,
salary trends, and experience distribution across roles.
Also evaluate India-specific trends to understand localized hiring patterns.
"""

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("ds_salaries.csv")

# -------------------------------
# DATA CLEANING
# -------------------------------
df = df.drop(columns=['Unnamed: 0'])
df = df.dropna()
df['job_title'] = df['job_title'].str.lower()

print("Cleaned Data Shape:", df.shape)

# -------------------------------
# ROLE CLASSIFICATION
# -------------------------------
def classify_role(title):
    if "analyst" in title:
        return "Analyst"
    elif "engineer" in title:
        return "Engineer"
    elif "scientist" in title:
        return "Scientist"
    else:
        return "Other"

df['role_category'] = df['job_title'].apply(classify_role)

# -------------------------------
# GLOBAL ROLE DISTRIBUTION
# -------------------------------
role_counts = df['role_category'].value_counts()
role_percent = df['role_category'].value_counts(normalize=True) * 100

print("\nGlobal Role Distribution:\n", role_counts)
print("\nGlobal Role Percentage (%):\n", role_percent)

# Insight:
# Engineering (~38%) and Scientist (~32%) roles dominate globally,
# while Analyst roles (~20%) form a smaller but important segment.

# Visualization
role_counts.plot(kind='bar')
plt.title("Global Role Distribution")
plt.xlabel("Role Category")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.savefig("global_role_distribution.png")
plt.show()

# -------------------------------
# SALARY ANALYSIS (GLOBAL)
# -------------------------------
salary_by_role = df.groupby('role_category')['salary_in_usd'].mean().sort_values(ascending=False)
median_salary = df.groupby('role_category')['salary_in_usd'].median()

print("\nAverage Salary by Role:\n", salary_by_role)
print("\nMedian Salary by Role:\n", median_salary)

# Insight:
# Analyst roles (~$93K) have lower salaries compared to Engineer (~$110K)
# and Scientist (~$115K), highlighting a premium on technical specialization.

# Visualization
salary_by_role.plot(kind='bar')
plt.title("Average Salary by Role (Global)")
plt.xlabel("Role Category")
plt.ylabel("Salary (USD)")
plt.xticks(rotation=0)
plt.savefig("salary_comparison.png")
plt.show()

# -------------------------------
# EXPERIENCE LEVEL ANALYSIS (GLOBAL)
# -------------------------------
exp_dist = df.groupby(['role_category', 'experience_level']).size()

exp_percent = df.groupby(['role_category', 'experience_level']).size().groupby(level=0).apply(
    lambda x: 100 * x / float(x.sum())
)

print("\nExperience Distribution:\n", exp_dist)
print("\nExperience % Distribution:\n", exp_percent)

# Insight:
# Analyst roles are not purely entry-level, with ~80% positions at mid/senior levels,
# indicating increasing expectations for experience and domain expertise.

# -------------------------------
# INDIA-SPECIFIC ANALYSIS (KEY DIFFERENTIATOR)
# -------------------------------
india_df = df[df['company_location'] == 'IN']

print("\nIndia Dataset Size:", india_df.shape)

if not india_df.empty:
    india_role_percent = india_df['role_category'].value_counts(normalize=True) * 100
    print("\nIndia Role Distribution (%):\n", india_role_percent)

    india_salary = india_df.groupby('role_category')['salary_in_usd'].mean()
    print("\nIndia Average Salary by Role:\n", india_salary)

    # Insight:
    # India-specific trends help understand localized hiring patterns
    # in outsourcing-driven IT services markets.

    # Visualization
    india_role_percent.plot(kind='bar')
    plt.title("Role Distribution in India")
    plt.xlabel("Role Category")
    plt.ylabel("Percentage")
    plt.xticks(rotation=0)
    plt.savefig("india_role_distribution.png")
    plt.show()
else:
    print("\nNo sufficient India-specific data available.")