# Week 1 Homework Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string`
- `--idimage string`
- `--idfile string`

``` 
$ docker build --help | grep "Write the image ID to the file"
      --iidfile string          Write the image ID to the file
```
>Answer: `--iidfile string`

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3
- 7

``` 
$ docker run -it python:3.9 pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```
>Answer: `  3 `

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

`wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz`

You will also need the dataset with zones:

`wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv`

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

```
SELECT COUNT(*)
FROM green_taxi
WHERE lpep_pickup_datetime::date = '2019-01-15'
	AND lpep_dropoff_datetime::date = '2019-01-15'
```
>Answer: ` 20530`

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

```
SELECT lpep_pickup_datetime::date
FROM green_taxi
GROUP BY lpep_pickup_datetime::date
ORDER BY MAX(trip_distance) DESC
LIMIT 1
```
>Answer: ` 2019-01-15`

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274

```
SELECT passenger_count, COUNT(*)
FROM green_taxi
WHERE lpep_pickup_datetime::date = '2019-01-01'
	AND (passenger_count = 2 OR passenger_count = 3)
GROUP BY passenger_count
```
>Answer: ` 2: 1282 ; 3: 254`
## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza
```
SELECT Zone
FROM taxi_zone_lookup
WHERE LocationID = (
	SELECT DOLocationID
	FROM green_taxi
	WHERE PULocationID = (
		SELECT LocationID
		FROM taxi_zone_lookup
		WHERE Zone = 'Astoria'
	)
	GROUP BY DOLocationID
	ORDER BY MAX(tip_amount) DESC
	LIMIT 1
)
```
>Answer: `Long Island City/Queens Plaza`

<br></br>
# Week 1 Homework Terraform

In this homework we'll prepare the environment by creating resources in GCP with Terraform.
In your VM on GCP install Terraform. Copy the files from the course repo here to your VM.

## Requirement pre-run
1. Install Terrform.
	```
	$ pip install terraform
	```
2. Install Google Cloud SDK.
3. Create GCP Account with googleskillsboost in 5 hour.
4. Create a **service account** with additional roles for created service account: BigQuery Admin, Storage Admin, Storage Object Admin.
5. Generate private JSON key and download it.
6. Enable following APIs:
	- IAM Service Account Credentials API
	- Identity and Access Management (IAM) API
7. Import file JSON key to our VM directory
8. Login to GCP in our VM
	```
	$ export GOOGLE_APPLICATION_CREDENTIALS="<path our import JSON key>"
	$ gcloud auth application-default login
	```

9. Modify the files as necessary to create a GCP Bucket and Big Query Dataset.
	- [main.tf](../1.%20Introduction%20GCP%2C%20Docker%2C%20Postgre%2C%20Terraform/terraform/main.tf)
	- [variables.tf](../1.%20Introduction%20GCP%2C%20Docker%2C%20Postgre%2C%20Terraform/terraform/variables.tf)

## Question 1. 
### Creating Resources After updating the main.tf and variable.tf files run:
```
	$ terraform init 
```
```
  $ terraform apply
```
    
Paste the output of this command into the homework submission form.
>Answer: 
```
var.project
  Our Project ID

  Enter a value: qwiklabs-gcp-04-73a4af44af08


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "us-central1"
      + project                    = "qwiklabs-gcp-04-73a4af44af08"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US-CENTRAL1"
      + name                        = "de_data_lake_qwiklabs-gcp-04-73a4af44af08"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/qwiklabs-gcp-04-73a4af44af08/datasets/trips_data_all]
google_storage_bucket.data-lake-bucket: Creation complete after 4s [id=de_data_lake_qwiklabs-gcp-04-73a4af44af08]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```