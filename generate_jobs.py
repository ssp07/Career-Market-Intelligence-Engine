import pandas as pd
import random
from datetime import date, timedelta

companies = [
    "Microsoft","Amazon","Google","TCS","Infosys",
    "Accenture","Cognizant","Wipro","Deloitte",
    "Capgemini","Adobe","Oracle","IBM","HCL",
    "Salesforce","JP Morgan","Goldman Sachs"
]

locations = [
    "Hyderabad","Bangalore","Pune","Mumbai",
    "Chennai","Delhi","Kolkata","Noida"
]

titles = {
    "Data Engineer":(1200000,2800000),
    "Data Analyst":(700000,1600000),
    "Analytics Engineer":(1200000,2400000),
    "BI Developer":(800000,1800000),
    "Data Scientist":(1400000,3000000),
    "Machine Learning Engineer":(1500000,3200000),
    "Fabric Engineer":(1800000,3500000),
    "Cloud Data Engineer":(1500000,3000000)
}

skills_map = {
    "Data Engineer":"Python,SQL,Azure,Spark",
    "Data Analyst":"SQL,Excel,Power BI",
    "Analytics Engineer":"Python,SQL,DBT,Power BI",
    "BI Developer":"Power BI,SQL,DAX",
    "Data Scientist":"Python,ML,SQL",
    "Machine Learning Engineer":"Python,ML,AWS,Spark",
    "Fabric Engineer":"Microsoft Fabric,SQL,Power BI",
    "Cloud Data Engineer":"Azure,Python,SQL,Fabric"
}

rows=[]

for i in range(1,501):

    title = random.choice(list(titles.keys()))
    salary = random.randint(
        titles[title][0],
        titles[title][1]
    )

    rows.append({
        "job_id":f"JOB{i:04d}",
        "title":title,
        "company":random.choice(companies),
        "location":random.choice(locations),
        "salary":salary,
        "experience":random.randint(1,10),
        "industry":"Technology",
        "skills":skills_map[title],
        "remote":random.choice([
            "Yes","No","Hybrid"
        ]),
        "posted_date":
        date.today()-timedelta(
            days=random.randint(0,30)
        )
    })

df = pd.DataFrame(rows)

df.to_csv(
    "jobs.csv",
    index=False
)

print("jobs.csv created")