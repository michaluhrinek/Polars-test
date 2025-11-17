#Cyber Security - data generation 

import polars as pl
import random
from datetime import datetime, timedelta

# Function to generate random start and closed dates
def generate_dates(opened_date, state):
    """Generate start and closed dates based on the state."""
    if state == "Closed":
        # Start date comes a few hours after creation, and the ticket closes shortly afterward
        start_date = opened_date + timedelta(hours=random.randint(1, 3))
        closed_date = start_date + timedelta(hours=random.randint(1, 4))
        return start_date, closed_date
    elif state == "In Progress":
        # Only the start date exists; no completion yet
        start_date = opened_date + timedelta(hours=random.randint(1, 3))
        return start_date, None
    elif state in ["New", "On Hold"]:
        # No start or closed date for these states
        return None, None
    else:  # for Canceled
        start_date = opened_date + timedelta(hours=random.randint(1, 3))
        closed_date = start_date + timedelta(hours=random.randint(1, 4))
        return start_date, closed_date

# Define the number of records to generate
num_records = 3750  

# Define categories for Change Environment and State
change_environments = [
    "Access", "Complaint", "Hardware", "Software", 
    "Network", "Failure", "Facilities", "Data", "SLA Breach"
]

states = [
    "New", "Closed", "In Progress", "On Hold", "Resolved", "Canceled"
]

# Extended list of short descriptions
short_descriptions = [
    "Failed Healthcheck - ID: 111-222-333-444-555 Host: ",
    "Failed Workflow - ID: 0000",
    "User login failed: Account locked due to excessive login attempts.",
    "Service outage detected - No connection to database.",
    "Suspicious activity detected on account: User A.",
    "Network issue: Unable to connect to external API.",
    "Critical alert: Database server overload detected.",
    "Security patch applied: Monitoring for any issues.",
    "Data breach notification sent to affected users.",
    "Performance report: Sluggish response times on application.",
    "Security alert: Unauthorized access attempt detected.",
    "Routine check: All systems operational - No issues detected.",
    "Service unavailable due to maintenance",
]

# Generate synthetic data spanning the last two years
data = []

# Set the range for two years
start_date_2_years_ago = datetime.now() - timedelta(days=730)
end_date = datetime.now()

# Generate a record for each day across the two-year range
for i in range(num_records):
    # Randomly choose a day within the past 730 days (2 years)
    random_days_in_past_2_years = random.randint(0, 730)
    opened_date = start_date_2_years_ago + timedelta(days=random_days_in_past_2_years)
    
    # Randomly choose state
    state = random.choice(states)
    
    # Generate start and closed dates based on the chosen state
    start_date, closed_date = generate_dates(opened_date, state)

    # Add each row of data
    data.append({
        "Number": f"CR-{i + 1}",
        "Short description": random.choice(short_descriptions),
        "Change Environment": random.choice(change_environments),
        "Opened by": random.choice(["User A", "User B", "User C", "User D"]),
        "Assigned to": random.choice(["User A", "User B", "User C", "User D", ""]),
        "Assignment group": random.choice(["Group A", "Group B", "Group C"]),
        "Service": random.choice(["Service A", "Service B", "Service C"]),
        "State": state,
        "Risk": random.choice(["High", "Medium", "Low"]),
        "Priority": random.choice(["P1", "P2", "P3"]),
        "Urgency": random.choice(["High", "Medium", "Low"]),
        "Impact": random.choice(["High", "Medium", "Low"]),
        "Model": random.choice(["Model A", "Model B", "Model C"]),
        "Created": opened_date,  # Creation date
        "Start Date": start_date,  # Work Start Date
        "Closed": closed_date,  # Work End Date
    })

# Create the DataFrame
df = pl.DataFrame(data)

# Format datetime format (YYYY-MM-DD HH:MM:SS)
formatted_df = df.with_columns([
    pl.col("Created").dt.strftime("%Y-%m-%d %H:%M:%S").alias("Created"),
    pl.col("Start Date").dt.strftime("%Y-%m-%d %H:%M:%S").alias("Start Date"),
    pl.col("Closed").dt.strftime("%Y-%m-%d %H:%M:%S").alias("Closed")
])

# Save to a CSV file for later use
output_file_path = r"C:\Users\HA2UHRI\Downloads\synthetic_change_requests_cybersecurity.csv"
formatted_df.write_csv(output_file_path)

print("Synthetic data generated and saved successfully.")
print(f"Generated DataFrame shape: {formatted_df.shape}")
print(formatted_df.head())