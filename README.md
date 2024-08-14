# UT Austin Pay Plan Data Scraper

This project is a Python application designed to scrape, process, and store the UT Austin Pay Plan data from an online source. The data is fetched from an API, parsed into structured formats, and saved in JSON, CSV, and XLSX formats for further analysis or use.

## Table of Contents

- [Project Structure](#project-structure)
  - [classes.py](#classespy)
  - [configs.py](#configspy)
  - [main.py](#mainpy)
  - [utilities.py](#utilitiespy)
- [Usage](#usage)
- [Standard Quick Install](#standard-quick-install)
  - [Quick Install Video Demo](#quick-install-video-demo)
  - [Explanation of Installation Script](#explanation-of-installation-script)
- [Docker Quick Install](#docker-quick-install)
  - [Explanation of Docker Installation Script](#explanation-of-docker-installation-script)

## Project Structure

The project is organized into four main components:

1. **classes.py**: Contains the `JobListing` class, which is used to parse and manage job data.
2. **configs.py**: Defines constants such as the output file path and keys used for mapping and headers in the final output.
3. **main.py**: The main script that handles the data scraping, processing, and storage operations.
4. **utilities.py**: Contains utility functions like `format_job_data`, `open_file`, and `write_spreadsheet` for processing and formatting job data.

```txt
ut-payplan
├── Dockerfile
├── README.md
├── classes.py
├── configs.py
├── data
├── main.py
├── requirements.txt
├── setup.sh
└── utilities.py
```

### classes.py

```python
import re

class JobListing:
    """
    A class to represent a job listing and extract relevant information from a job dictionary.

    Attributes:
        job_dict (dict): A dictionary containing job details fetched from an API.

    Methods:
        _parse_salary(salary_str: str) -> tuple:
            Parses a salary string to extract the minimum and maximum salary values.
        
        title() -> str:
            Extracts the job title from the job dictionary.

        id() -> str:
            Returns the job ID from the job dictionary.

        date() -> str:
            Returns the effective date of the job listing from the job dictionary.

        category() -> str:
            Returns the job category from the job dictionary.

        annual_salary_min() -> float or None:
            Returns the minimum annual salary for the job, or None if not available.

        annual_salary_max() -> float or None:
            Returns the maximum annual salary for the job, or None if not available.

        monthly_salary_min() -> float or None:
            Returns the minimum monthly salary for the job, or None if not available.

        monthly_salary_max() -> float or None:
            Returns the maximum monthly salary for the job, or None if not available.
    """

    def __init__(self, job_dict):
        """
        Initializes a JobListing instance with a dictionary of job details.

        Args:
            job_dict (dict): A dictionary containing job details such as title, ID, category, effective date,
                             and salary ranges.
        """
        self.job_dict = job_dict
    
    def _parse_salary(self, salary_str):
        """
        Parses a salary string to extract the minimum and maximum salary values.

        Args:
            salary_str (str): A string containing the salary range, typically in the format "$min - $max".

        Returns:
            tuple: A tuple containing the minimum and maximum salary as floats. If the range is not available,
                   returns (None, None).
        """
        min_max = re.findall(r'\$([\d,]+\.\d{2})', salary_str)
        if len(min_max) == 2:
            return float(min_max[0].replace(',', '')), float(min_max[1].replace(',', ''))
        return None, None
    
    @property
    def title(self):
        """
        Extracts the job title from the job dictionary.

        Returns:
            str: The job title, or None if the title cannot be found.
        """
        title_match = re.search(r'>(.*?)<', self.job_dict["Job Title"])
        return title_match.group(1) if title_match else None
    
    @property
    def id(self):
        """
        Returns the job ID from the job dictionary.

        Returns:
            str: The job ID (Job Code).
        """
        return self.job_dict["Job ID (Job Code)"]

    @property
    def date(self):
        """
        Returns the effective date of the job listing from the job dictionary.

        Returns:
            str: The effective date of the job listing.
        """
        return self.job_dict["Effective Date"]
    
    @property
    def category(self):
        """
        Returns the job category from the job dictionary.

        Returns:
            str: The job category.
        """
        return self.job_dict["Job Category"]
    
    @property
    def annual_salary_min(self):
        """
        Returns the minimum annual salary for the job.

        Returns:
            float or None: The minimum annual salary, or None if not available.
        """
        annual_min, _ = self._parse_salary(self.job_dict["Annual Min - Max"])
        return annual_min
    
    @property
    def annual_salary_max(self):
        """
        Returns the maximum annual salary for the job.

        Returns:
            float or None: The maximum annual salary, or None if not available.
        """
        _, annual_max = self._parse_salary(self.job_dict["Annual Min - Max"])
        return annual_max
    
    @property
    def monthly_salary_min(self):
        """
        Returns the minimum monthly salary for the job.

        Returns:
            float or None: The minimum monthly salary, or None if not available.
        """
        monthly_min, _ = self._parse_salary(self.job_dict["Monthly Min - Max"])
        return monthly_min
    
    @property
    def monthly_salary_max(self):
        """
        Returns the maximum monthly salary for the job.

        Returns:
            float or None: The maximum monthly salary, or None if not available.
        """
        _, monthly_max = self._parse_salary(self.job_dict["Monthly Min - Max"])
        return monthly_max
```

The `JobListing` class is responsible for encapsulating the details of a job listing. It provides methods to extract and parse relevant information like job title, ID, category, effective date, and salary ranges (both annual and monthly).

### configs.py

```python
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
```

This file contains the configuration settings for the project, including:

- **`OUTPUT_PATH`**: The file path where the output JSON data will be saved. It uses `pathlib.Path` to handle file paths in an OS-independent way.
- **`KEYS`**: Lists the fields expected in the API response and used to extract relevant job data.
- **`HEADERS`**: Defines the column headers for the CSV output, mapping the extracted data fields to human-readable names.

### main.py

This is the main script that orchestrates the scraping, processing, and output generation. Below is a breakdown of the functions:

- **`generate_get_url(query_params: dict = {}) -> requests.Response`**: Generates and returns a GET request to the UT Austin Pay Plan data API, using the provided query parameters.

- **`fetch_all_data(total_records: int) -> list`**: Fetches all the data by making multiple requests to the API, accounting for pagination.

- **`save_payment_plan_data(data: list) -> None`**: Saves the processed payment plan data into a JSON file.

- **`get_payment_plan() -> dict`**: Main function to retrieve and process the payment plan data. It first checks if the data file exists locally; if not, it fetches the data from the API.

- **`write_delim_file(path: Union[str, Path], data: List[List[str]], delim: str) -> None`**: Writes the processed data to a CSV file using the specified delimiter.

### utilities.py

The `utilities.py` file includes functions to format and process the job data:

- **`format_job_data(df: pd.DataFrame) -> pd.DataFrame`**: Formats the columns of a DataFrame containing job data by converting text columns to strings, the 'Effective Date' column to datetime, and currency columns to float.
- **`open_file(file_path: Union[str, Path]) -> None`**: Opens the Excel file once it has been created.
- **`write_spreadsheet(csv_file_path: Union[str, Path], excel_file_path: Union[str, Path]) -> None`**: Converts a CSV file into an Excel spreadsheet, applying necessary formatting.

## Usage

To run the project, execute the `main.py` script. The script will check if the `ut-austin_pay-plan.json` file exists. If not, it will fetch the data from the UT Austin API, process it, and store it in JSON and CSV formats.

```bash
python main.py
```

The output files will be stored in the `data/` directory:

- `ut-austin_pay-plan.json`: Contains the raw data in JSON format.
- `ut-austin_pay-plan.csv`: Contains the processed data in CSV format.
- `ut-austin_pay-plan.xlsx`: Contains the processed data in XLSX format.

## Standard Quick Install

Copy and paste the following into the terminal to install, setup, and run program on MacOS:

```bash
git clone https://github.com/williamveith/ut-payplan.git
cd ut-payplan
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

### Quick Install Video Demo

[<img src="https://img.youtube.com/vi/03rc_4V4hnE/maxresdefault.jpg" width="100%">](https://www.youtube.com/watch?v=03rc_4V4hnE "Video Demo")

### Explanation of installation script

1. **Clone the repository:**

    ```bash
    git clone https://github.com/williamveith/ut-payplan.git
    cd ut-payplan
    ```

2. **Set up a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required Python packages:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Run the main script to fetch and process the data:**

    ```bash
    python main.py
    ```

## Docker Quick Install

A docker build was created to deal with any cross platform issues that may occur. Copy and paste this into your terminal to build and run the docker container. The excel data will then be generated and placed in the current folder under ut-payplan.

```bash
git clone https://github.com/williamveith/ut-payplan.git
cd ut-payplan
docker build -t ut-payplan .
docker run -v "$(pwd):/app/data" ut-payplan
```

### Explanation of docker installation script

1. **Clone the repository**:

   ```bash
   git clone https://github.com/williamveith/ut-payplan.git
   ```

2. **Navigate to the project directory**:

    ```bash
    cd ut-payplan
    ```

3. **Build the Docker image**:

    ```bash
    docker build -t ut-payplan .
    ```

4. **Run the Docker container with volume mounting**:

    ```bash
    docker run -v "$(pwd):/app/data" ut-payplan
    ```
