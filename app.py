import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Career Market Intelligence Engine",
    page_icon="📊",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("jobs.csv")

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.header("🎯 Career Filters")

selected_locations = st.sidebar.multiselect(
    "Location",
    options=sorted(df["location"].unique()),
    default=sorted(df["location"].unique())
)

selected_work_modes = st.sidebar.multiselect(
    "Work Mode",
    options=sorted(df["remote"].unique()),
    default=sorted(df["remote"].unique())
)

salary_range = st.sidebar.slider(
    "Salary Range (₹)",
    min_value=int(df["salary"].min()),
    max_value=int(df["salary"].max()),
    value=(
        int(df["salary"].min()),
        int(df["salary"].max())
    )
)

selected_roles = st.sidebar.multiselect(
    "Job Role",
    options=sorted(df["title"].unique()),
    default=sorted(df["title"].unique())
)

selected_industries = st.sidebar.multiselect(
    "Industry",
    options=sorted(df["industry"].unique()),
    default=sorted(df["industry"].unique())
)

# =====================================
# APPLY FILTERS
# =====================================

filtered_df = df[
    (df["location"].isin(selected_locations))
    &
    (df["remote"].isin(selected_work_modes))
    &
    (df["title"].isin(selected_roles))
    &
    (df["industry"].isin(selected_industries))
    &
    (df["salary"] >= salary_range[0])
    &
    (df["salary"] <= salary_range[1])
]

# =====================================
# HEADER
# =====================================

st.title("📊 Career Market Intelligence Engine")

st.markdown("""
Transform job market data into actionable career intelligence.

### Dashboard Features

✅ Job Market Analytics

✅ Skill Demand Intelligence

✅ Salary Analytics

✅ Hiring Company Insights

✅ Location Intelligence

✅ Career Recommendations

✅ Interactive Filters
""")

st.divider()

# =====================================
# KPI SECTION
# =====================================

all_skills = []

for skills in filtered_df["skills"]:
    skill_list = [
        x.strip()
        for x in str(skills).split(",")
    ]
    all_skills.extend(skill_list)

unique_skills = len(set(all_skills))

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Jobs",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Companies",
        filtered_df["company"].nunique()
    )

with col3:
    avg_salary = (
        filtered_df["salary"].mean()
        if len(filtered_df) > 0
        else 0
    )

    st.metric(
        "Avg Salary",
        f"₹{avg_salary/100000:.1f}L"
    )

with col4:
    st.metric(
        "Unique Skills",
        unique_skills
    )

st.divider()

# =====================================
# TOP HIRING COMPANIES
# =====================================

st.subheader("🏢 Top Hiring Companies")

if len(filtered_df) > 0:

    company_count = (
        filtered_df["company"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    company_count.columns = [
        "Company",
        "Jobs"
    ]

    fig = px.bar(
        company_count,
        x="Company",
        y="Jobs",
        color="Jobs",
        title="Top Hiring Companies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# MOST DEMANDED SKILLS
# =====================================

st.subheader("🔥 Most Demanded Skills")

skills = []

for row in filtered_df["skills"]:
    skills.extend(
        [
            x.strip()
            for x in str(row).split(",")
        ]
    )

skill_df = pd.DataFrame(
    Counter(skills).most_common(15),
    columns=["Skill", "Count"]
)

if len(skill_df) > 0:

    fig2 = px.bar(
        skill_df,
        x="Count",
        y="Skill",
        orientation="h",
        color="Count",
        title="Top Skills in Demand"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================
# SALARY ANALYTICS
# =====================================

st.subheader("💰 Salary Intelligence")

if len(filtered_df) > 0:

    role_salary = (
        filtered_df
        .groupby("title")["salary"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        role_salary,
        x="title",
        y="salary",
        color="salary",
        title="Average Salary by Role"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    fig4 = px.histogram(
        filtered_df,
        x="salary",
        nbins=25,
        title="Salary Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================
# LOCATION ANALYTICS
# =====================================

st.subheader("📍 Location Intelligence")

if len(filtered_df) > 0:

    location_df = (
        filtered_df["location"]
        .value_counts()
        .reset_index()
    )

    location_df.columns = [
        "Location",
        "Jobs"
    ]

    fig5 = px.bar(
        location_df,
        x="Location",
        y="Jobs",
        color="Jobs",
        title="Jobs by Location"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# =====================================
# WORK MODE ANALYTICS
# =====================================

st.subheader("🏠 Work Mode Distribution")

if len(filtered_df) > 0:

    remote_df = (
        filtered_df["remote"]
        .value_counts()
        .reset_index()
    )

    remote_df.columns = [
        "Mode",
        "Count"
    ]

    fig6 = px.pie(
        remote_df,
        names="Mode",
        values="Count",
        hole=0.4,
        title="Remote vs Onsite vs Hybrid"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# =====================================
# INDUSTRY ANALYTICS
# =====================================

st.subheader("🏭 Industry Distribution")

if len(filtered_df) > 0:

    industry_df = (
        filtered_df["industry"]
        .value_counts()
        .reset_index()
    )

    industry_df.columns = [
        "Industry",
        "Jobs"
    ]

    fig7 = px.bar(
        industry_df,
        x="Industry",
        y="Jobs",
        color="Jobs",
        title="Jobs by Industry"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

# =====================================
# CAREER RECOMMENDATION ENGINE
# =====================================

st.subheader("🎯 Skill-Based Career Recommendation Engine")

all_skill_pool = []

for skills in df["skills"]:
    all_skill_pool.extend(
        [
            x.strip()
            for x in str(skills).split(",")
        ]
    )

selected_skill = st.selectbox(
    "Select Your Current Skill",
    sorted(set(all_skill_pool))
)

related_skills = []

matching_jobs = df[
    df["skills"].str.contains(
        selected_skill,
        case=False,
        na=False
    )
]

for skills in matching_jobs["skills"]:

    skill_list = [
        x.strip()
        for x in str(skills).split(",")
    ]

    for skill in skill_list:

        if skill != selected_skill:
            related_skills.append(skill)

recommended = Counter(
    related_skills
).most_common(5)

st.success(
    f"Recommended next skills after {selected_skill}"
)

for i, (skill, count) in enumerate(
    recommended,
    start=1
):
    st.write(
        f"{i}. {skill} ({count} related job matches)"
    )

# =====================================
# CAREER ROADMAP
# =====================================

st.subheader("🛣 Suggested Learning Roadmap")

career_paths = {

    "Python": [
        "SQL",
        "Azure",
        "Spark",
        "Databricks",
        "Machine Learning"
    ],

    "SQL": [
        "Power BI",
        "Azure",
        "Microsoft Fabric",
        "DBT",
        "Data Modeling"
    ],

    "Azure": [
        "Microsoft Fabric",
        "Databricks",
        "Spark",
        "Data Engineering",
        "Power BI"
    ],

    "Power BI": [
        "DAX",
        "SQL",
        "Microsoft Fabric",
        "Data Modeling",
        "Analytics Engineering"
    ],

    "Microsoft Fabric": [
        "Power BI",
        "Lakehouse",
        "Data Warehouse",
        "Spark",
        "Azure"
    ]
}

if selected_skill in career_paths:

    st.info(
        f"Suggested roadmap for becoming stronger in {selected_skill}"
    )

    for step, skill in enumerate(
        career_paths[selected_skill],
        start=1
    ):
        st.write(
            f"✅ Step {step}: {skill}"
        )

# =====================================
# JOB SEARCH
# =====================================

st.subheader("🔎 Job Search")

job_keyword = st.text_input(
    "Search Jobs"
)

if job_keyword:

    search_results = filtered_df[
        filtered_df["title"]
        .str.contains(
            job_keyword,
            case=False,
            na=False
        )
        |
        filtered_df["company"]
        .str.contains(
            job_keyword,
            case=False,
            na=False
        )
        |
        filtered_df["skills"]
        .str.contains(
            job_keyword,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        search_results,
        use_container_width=True
    )

else:

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================
# CAREER INSIGHTS
# =====================================

st.subheader("📈 Market Intelligence")

if len(skill_df) > 0:

    top_skill = skill_df.iloc[0]["Skill"]

    st.success(
        f"🔥 Hottest Skill: {top_skill}"
    )

if len(filtered_df) > 0:

    top_company = (
        filtered_df["company"]
        .value_counts()
        .idxmax()
    )

    st.info(
        f"🏢 Top Hiring Company: {top_company}"
    )

    top_role = (
        filtered_df
        .groupby("title")["salary"]
        .mean()
        .sort_values(
            ascending=False
        )
        .index[0]
    )

    st.warning(
        f"💰 Highest Paying Role: {top_role}"
    )

# =====================================
# DATA EXPLORER
# =====================================

with st.expander("📄 Dataset Explorer"):

    st.write(
        f"Showing {len(filtered_df)} rows"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )