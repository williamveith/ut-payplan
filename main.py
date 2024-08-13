import requests
import json
import pathlib

OUTPUT_PATH = pathlib.Path("ut-austin_pay-plan.json")
KEYS = [
    "Job Title",
    "Job ID (Job Code)",
    "Job Category",
    "Effective Date",
    "Annual Min - Max",
    "Monthly Min - Max",
]


def generate_get_url(query_params={}):
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
        "order[0][dir]": query_params.get("order_dir", "job_title"),
        "start": query_params.get("start", 0),
        "length": query_params.get("length", 1),
        "search[value]": "",
        "search[regex]": "false",
    }

    return requests.get(base_url, params=params)


def get_payment_plan():
    if not OUTPUT_PATH.exists():
        query_params = {"length": 1}

        initial_request = generate_get_url(query_params)
        response_data = initial_request.json()
        total_number_of_records = response_data.get("recordsTotal", None)

        if total_number_of_records is None:
            print(
                f"Response object property recordsTotal does not exist. Response data was: {response_data}"
            )
            print(f"Request Response: {initial_request}")

        else:
            query_params["length"] = total_number_of_records
            response = generate_get_url(query_params)
            response_data = response.json()

            payment_plan_data = []
            for job in response_data["data"]:
                payment_plan_data.append(dict(zip(KEYS, job)))

            response_data["data"] = payment_plan_data

            with open(OUTPUT_PATH, "w") as file:
                json.dump(response_data, file, indent=4)
                print(f"Response data saved to: {OUTPUT_PATH}")

    with open(OUTPUT_PATH, "r") as file:
        pay_plan_data = json.load(file)
        return pay_plan_data


if __name__ == "__main__":
    data = get_payment_plan()
