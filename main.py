import requests
import json
from pathlib import Path
import math

from classes import JobListing
from configs import OUTPUT_PATH, KEYS, HEADERS
from utilities import write_delim_file, write_spreadsheet, open_file


def generate_get_url(query_params: dict = {}) -> requests.Response:
    """
    Generates and returns a GET request to the UT Austin Pay Plan data API.

    Args:
        query_params (dict): Dictionary containing query parameters for the API request.
                             Default is an empty dictionary.

    Returns:
        requests.Response: The response object from the GET request.

    Example:
        response = generate_get_url({"draw": 1, "length": 100, "start": 0})
    """
    base_url = (
        "https://utdirect.utexas.edu/apps/hr/payplan/nlogon/profiles/datatable/data/"
    )
    params = {
        "draw": query_params.get("draw", 0),
        "columns[0][data]": 0,
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "true",
        "columns[0][search][regex]": "false",
        "columns[1][data]": 1,
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][regex]": "false",
        "columns[2][data]": 2,
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][regex]": "false",
        "columns[3][data]": 3,
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "true",
        "columns[3][search][regex]": "false",
        "columns[4][data]": 4,
        "columns[4][searchable]": "true",
        "columns[4][orderable]": "false",
        "columns[4][search][regex]": "false",
        "columns[5][data]": 5,
        "columns[5][searchable]": "true",
        "columns[5][orderable]": "false",
        "columns[5][search][regex]": "false",
        "order[0][column]": query_params.get("order_column", 0),
        "order[0][dir]": query_params.get("order_dir", "asc"),
        "start": query_params.get("start", 0),
        "length": query_params.get("length", 100),
        "search[value]": "",
        "search[regex]": "false",
    }

    return requests.get(base_url, params=params)


def fetch_all_data(total_records: int) -> list:
    """
    Fetches all job data from the UT Austin Pay Plan data API, handling pagination.

    Args:
        total_records (int): The total number of records available in the API.

    Returns:
        list: A list of all job data records.

    Example:
        all_data = fetch_all_data(1000)
    """
    all_data = []
    for item in range(int(math.ceil(total_records / 100))):
        params = {"draw": item, "length": 100, "start": item * 100}
        response = generate_get_url(params)
        all_data.extend(response.json().get("data", []))
    return all_data


def save_payment_plan_data(data: list) -> None:
    """
    Saves the payment plan data to a JSON file.

    Args:
        data (list): A list of job data to be saved.

    Returns:
        None

    Example:
        save_payment_plan_data(all_data)
    """
    payment_plan_data = [dict(zip(KEYS, job)) for job in data]
    response_data = {"data": payment_plan_data}

    path = Path(OUTPUT_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w") as file:
        json.dump(response_data, file, indent=4)
        print(f"Response data saved to: {OUTPUT_PATH}")


def get_payment_plan() -> dict:
    """
    Retrieves the payment plan data, either from a local file or by making an API request.

    Returns:
        dict: The payment plan data.

    Example:
        payment_plan = get_payment_plan()
    """
    if not OUTPUT_PATH.exists():
        initial_request = generate_get_url({"length": 1})
        response_data = initial_request.json()
        total_records = response_data.get("recordsTotal")

        if total_records is None:
            print(
                f"Response object property 'recordsTotal' does not exist. Response data was: {response_data}"
            )
            print(f"Request Response: {initial_request}")
        else:
            all_data = fetch_all_data(total_records)
            save_payment_plan_data(all_data)

    with open(OUTPUT_PATH, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    return_value = [HEADERS]
    payment_plan = get_payment_plan()

    for data in payment_plan.get("data", []):
        job = JobListing(data)
        return_value.append(
            [
                job.title,
                job.id,
                job.category,
                job.date,
                job.annual_salary_min,
                job.annual_salary_max,
                job.monthly_salary_min,
                job.monthly_salary_max,
            ]
        )

    write_delim_file(OUTPUT_PATH.with_suffix(".csv"), return_value, ",")
    write_spreadsheet(
        csv_file_path=OUTPUT_PATH.with_suffix(".csv"),
        excel_file_path=OUTPUT_PATH.with_suffix(".xlsx"),
    )
    open_file(OUTPUT_PATH.with_suffix(".xlsx"))
