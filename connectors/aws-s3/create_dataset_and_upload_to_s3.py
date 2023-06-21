import random
import time
from datetime import datetime, timedelta

import boto3
import numpy as np
import pandas as pd
from rich.progress import Progress


def create_dataset(file_name, num_rows, start_date, end_date):
    """Create a dataset"""
    with Progress() as progress:
        task = progress.add_task("[cyan]Creating dataset...", total=num_rows)

        # Generate dates from the specified start date to the specified end date
        date_range = pd.date_range(start_date, end_date).tolist()

        # Generate dates
        dates = [random.choice(date_range) for _ in range(num_rows)]

        # Generate random tickers
        tickers = np.random.choice(['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB'], num_rows)

        # Generate random open, high, low, close prices and volumes
        opens = np.random.uniform(100, 200, num_rows)
        highs = opens + np.random.uniform(0, 10, num_rows)
        lows = opens - np.random.uniform(0, 10, num_rows)
        closes = np.random.uniform(lows, highs, num_rows)
        volumes = np.random.randint(5000, 10000, num_rows)

        # Create a DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Ticker': tickers,
            'Open': opens,
            'High': highs,
            'Low': lows,
            'Close': closes,
            'Volume': volumes
        })

        # Write the DataFrame to a CSV file
        df.to_csv(file_name, index=False)

        progress.update(task, advance=num_rows)


def upload_dataset_to_s3(file_name):
    """Uploads a dataset to S3 bucket"""
    with Progress() as progress:
        task = progress.add_task("[green]Uploading dataset to S3...", total=100)

        # Create a session using your AWS credentials
        session = boto3.Session(
            aws_access_key_id="YOUR_ACCESS_KEY",
            aws_secret_access_key="YOUR_SECRET_KEY",
            region_name="YOUR_REGION",  # e.g. 'us-west-2'
        )

        # Create an S3 client using the session
        s3 = session.client("s3")

        # Name of the bucket
        bucket_name = "your-bucket-name"

        # Upload the file
        s3.upload_file(
            file_name, bucket_name, "stock_data_monthly/" + file_name
        )  # Updated to upload to 'stock_data_monthly' folder

        progress.update(task, advance=100)


if __name__ == "__main__":
    file_name = (
        input(f"Enter the file name (default: stock_data_monthly.csv): ")
        or "stock_data_monthly.csv"
    )
    if not file_name.endswith(".csv"):
        file_name += ".csv"
    num_rows = int(input(f"Enter the number of rows (default: 10000000): ") or 10000000)

    while True:
        start_year = int(input(f'Enter the start year (default: 2022): ') or 2022)
        start_month = int(input(f'Enter the start month (1-12, default: 1): ') or 1)
        end_year = int(input(f'Enter the end year (default: 2024): ') or 2024)
        end_month = int(input(f'Enter the end month (1-12, default: 1): ') or 1)

        start_date = datetime(start_year, start_month, 1)
        end_date = datetime(end_year, end_month, 1) - timedelta(days=1)

        if start_date >= end_date:
            print("End date must be later than start date. Please try again.")
        else:
            break


    start_time = time.time()
    create_dataset(file_name=file_name, num_rows=num_rows, start_date=start_date, end_date=end_date)
    end_time = time.time()
    print(f'Execution time of create_dataset: {end_time - start_time:.2f} seconds')

    start_time = time.time()
    upload_dataset_to_s3(file_name=file_name)
    end_time = time.time()
    print(
        f"Execution time of upload_dataset_to_s3: {end_time - start_time:.2f} seconds"
    )
