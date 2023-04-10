import pandas as pd
from pathlib import Path
from datetime import timedelta
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)
    return df

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out as parquet file"""
    data_dir = f'destination/'
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    path = Path(f'{data_dir}/{dataset_file}.parquet')
    df.to_parquet(path, compression='gzip')
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-data-trends")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=path)

@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    dataset_file = f'tourism_with_id'
    dataset_url = f'tourism_with_id.csv'
    df = fetch(dataset_url)
#    df = clean(df)
    path = write_local(df, dataset_file)
    write_gcs(path)
    
###############################################################################
"""FLOW FOR BIG QUERY"""

@task(retries=3)
def extract_from_gcs() -> Path:
    """Data Extract from Google Cloud Storage"""
    dataset_file = f'tourism_with_id'
    gcs_path = f"{dataset_file}.parquet"
    gcs_block = GcsBucket.load("gcs-data-trends")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"destination/")
    print(gcs_path)
    return Path(f"destination/{gcs_path}")

@task()
def transform(path) -> pd.DataFrame:
    """Data Cleaning"""
    df = pd.read_parquet(path)
#    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
#    df['passenger_count'].fillna(0, inplace=True)
#    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df

@task()
def write_bq(df) -> None:
    """Write DataFrame to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("data-rends-creds")

#    df = df.astype(str)
    df.to_gbq(
        destination_table="data_trends.tourism",
        project_id="de-1199",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow()
def etl_gcs_to_bq():
#    dataset_url = f'tourism_with_id.parquet'
    path = extract_from_gcs()
    df = transform(path)
    write_bq(df)

##################################################################################
"""PARENT FLOW"""

@flow()
def etl_parent_flow() -> None:
#    for month in months:
    etl_web_to_gcs()
    etl_gcs_to_bq()

if __name__ == '__main__':
    etl_parent_flow()