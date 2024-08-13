import csv
import subprocess
import platform
import os
import pandas as pd
from typing import List, Union
from pathlib import Path
from configs import OUTPUT_PATH

def open_file(file_path: Union[str, Path]) -> None:
    """
    Opens a file using the default application associated with its type.

    Args:
        file_path (str): The path to the file to be opened.

    Returns:
        None
    """
    if os.path.exists('/.dockerenv'):
        print(f"Excel file saved at: {OUTPUT_PATH.with_suffix('.xlsx')}")
        return

        
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(['open', file_path])
    elif platform.system() == 'Linux':  # Linux
        subprocess.call(['xdg-open', file_path])
    else:  # Windows
        os.startfile(file_path)
        

def write_delim_file(path: Union[str, Path], data: List[List[str]], delim: str) -> None:
    """
    Writes a list of lists (data) to a file using a specified delimiter.

    Args:
        path (str or Path): The path where the file will be written.
        data (list of lists): The data to be written to the file.
        delim (str): The delimiter to use for separating entries in the file.

    Returns:
        None

    Example:
        write_delim_file("output.csv", data, ",")
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=delim)
        writer.writerows(data)

def format_job_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the columns of a DataFrame containing job data.

    This function performs the following operations:
    1. Converts the 'Job Title', 'Job ID (Job Code)', and 'Job Category' columns to string type.
    2. Converts the 'Effective Date' column to a datetime object with the format 'MM/DD/YYYY'.
    3. Converts the 'Annual Min', 'Annual Max', 'Monthly Min', and 'Monthly Max' columns from currency strings to float type by removing dollar signs and commas.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing job data with the following columns:
            - 'Job Title'
            - 'Job ID (Job Code)'
            - 'Job Category'
            - 'Effective Date'
            - 'Annual Min'
            - 'Annual Max'
            - 'Monthly Min'
            - 'Monthly Max'

    Returns:
        pd.DataFrame: The formatted DataFrame with appropriate data types for each column.
    """
    df['Job Title'] = df['Job Title'].astype(str)
    df['Job ID (Job Code)'] = df['Job ID (Job Code)'].astype(str)
    df['Job Category'] = df['Job Category'].astype(str)
    
    df['Effective Date'] = pd.to_datetime(df['Effective Date'], format='%m/%d/%Y')

    currency_columns = ['Annual Min', 'Annual Max', 'Monthly Min', 'Monthly Max']
    for column in currency_columns:
        df[column] = df[column].replace(r'[\$,]', '', regex=True).astype(float)
    return df

def write_spreadsheet(csv_file_path: Union[str, Path], excel_file_path: Union[str, Path]) -> None:
    """
    Converts a CSV file into an Excel spreadsheet and saves it.

    Args:
        csv_file_path (str): The path to the input CSV file.
        excel_file_path (str): The path where the output Excel file should be saved.

    Returns:
        None
    """
    df = pd.read_csv(csv_file_path)
    df = format_job_data(df)
    df.to_excel(excel_file_path, index=False)