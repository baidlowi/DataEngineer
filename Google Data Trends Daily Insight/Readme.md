# Google Data Trends Daily Insight

## Problem Definition

Google Data Trends is a tool provided by Google that allows users to explore and analyze search data. With Google Data Trends, users can enter a search term or topic and see how frequently that term has been searched for over a specified time period, as well as the geographic locations where it has been searched most frequently. This tool can be useful for understanding the popularity of a particular topic over time, identifying trends and patterns in search behavior, and conducting market research. Users can also compare the search volume of multiple terms and topics, and view related queries and topics.


***

## Solution Overview

![Google Data Trends](https://user-images.githubusercontent.com/79616397/230936031-9929d991-d18f-4474-8549-55c25e9b3a13.png)

This project wanna get data daily trends in country Indonesia and get insigths dashboard frfom trending topics in this country


### Tools
Google Cloud Platform (GCP): Cloud-based auto-scaling platform by Google
Google Cloud Storage (GCS): Data Lake
BigQuery: Data Warehouse
Terraform: Infrastructure-as-Code (IaC)
Docker: Containerization
Prefect: Workflow Orchestration

***

## Step-by-step Guide

### Part 1: Infrastructure as Code Cloud Resource with Terraform

1. Install `gcloud SDK`, `terraform`, and create a GCP project. 

2. Create a service account with **Storage Admin**, **Storage Pbject Admin**, **BigQuery Admin** role. 

3. Create and Download the JSON credential and store it on `.google/credentials/google_credential.json`

4. Edit `1-terraform/main.tf` in a text editor, and change `de-1199` with GCP's project id.

5. Move directory to `1-terraform` by executing
    ```
    cd 1-terraform
    ```

6. Initialize Terraform (set up environment and install Google provider)
    ```
    terraform init
    ```
7. Plan Terraform infrastructure creation
    ```
    terraform plan
    ```
8. Create new infrastructure by applying Terraform plan
    ```
    terraform apply
    ```
9. Check GCP console to see newly-created resource `GCS Bucket`, `Big Query Dataset`, and `Virtual Machine`.
<br>
### Part 2: Run Prefect to Scrape, Ingest, and Warehouse Data
1. Go to source directory
    ```
    cd ..
    ```
Then, replace `de-1199` in `.env` file to project ID.

2. Build Prefect docker images
    ```
    docker-compose build
    ```
3. Run Prefect docker containers
    ```
    docker-compose up
    ```
or for daemonized run
    ```
    docker-compose up -d
    ```
4. Access the Prefect webserver through web browser on `localhost:4200` and create block `GCS Bucket` (with name GCS Bucket) and `GCS Credentials`(from file key-account.json)
   
![image](https://user-images.githubusercontent.com/79616397/230938723-e6147a2e-9486-4b94-b4c9-50c70d4a0a41.png)

![image](https://user-images.githubusercontent.com/79616397/230938893-49026aa4-20cc-4153-9922-49849426003b.png)

![image](https://user-images.githubusercontent.com/79616397/230939493-28038092-c69e-45a9-8fe5-da3f52a99ed7.png)

5. Run Workflow `parent-workflow.py` and schedule it in every night
    ```
    prefect deployment build parent-workflow.py:etl_parent_flow -n "Parameterized ETL"
    ```
    ![image](https://user-images.githubusercontent.com/79616397/230938319-f8cab849-eb08-4fa4-8c43-86b6c89b4b73.png)
    ![image](https://user-images.githubusercontent.com/79616397/230939662-a4a37bd5-58af-4ff3-9625-8de1f5aebb14.png)

6. Run prefect agent to start queue schedule
    ```
    prefect agent start --work-queue "default" 
    ```

6. After done, check GCP Console, both in Google Cloud Storage and BigQuery to check the data.

![image](https://user-images.githubusercontent.com/79616397/230939956-b3e6e358-26d0-4a67-80a0-6962915dda46.png)

![Uploading image.png…]()

### Part 3: Visualize Data
1. Open Looker Studio or Tableau Desktop, and connect to BigQuery.
2. Authorize credentials service aaccount from `account-key.json`
2. Visualize the dashboard, publish to Public.

![Dashboard](docs/dashboard-sample.png)

### Part 4: Stopping Project
1. To shut down the project, just stop the docker container
```
docker-compose down
```

### Data Engineering Zoomcamp by DataTalksClub
https://github.com/DataTalksClub/data-engineering-zoomcamp
