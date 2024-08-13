import pathlib

# Define the output path where the payment plan data will be saved.
# The data will be saved in JSON format at this location.
OUTPUT_PATH = pathlib.Path("data/ut-austin_pay-plan.json")

# KEYS represent the fields that will be extracted from the raw job data obtained from the API.
# These keys correspond to the data fields within the API response.
KEYS = [
    "Job Title",
    "Job ID (Job Code)",
    "Job Category",
    "Effective Date",
    "Annual Min - Max",
    "Monthly Min - Max",
]

# HEADERS represent the column names that will be used when writing the job data to a CSV file.
# These headers correspond to the processed data fields that will be output in the CSV.
HEADERS = [
    "Job Title",
    "Job ID (Job Code)",
    "Job Category",
    "Effective Date",
    "Annual Min",
    "Annual Max",
    "Monthly Min",
    "Monthly Max",
]