# TERRAFORM

## Installation Requirement
1. Install Terrform.
	```
	$ pip install terraform
	```
2. Install Google Cloud SDK.
3. Create GCP Account with googleskillsboost in 5 hour.
4. Create a `Service Account` with additional roles for created service account: BigQuery Admin, Storage Admin, Storage Object Admin.
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
	- [main.tf](https://github.com/baidlowi/DataEngineer/blob/main/1.%20Introduction%20GCP%2C%20Docker%2C%20Postgre%2C%20Terraform/main.tf)
	- [variables.tf](https://github.com/baidlowi/DataEngineer/blob/main/1.%20Introduction%20GCP%2C%20Docker%2C%20Postgre%2C%20Terraform/variables.tf)

## Run Terraform
- we can only 1 to run it 

    ```
    $ terraform init
    ```
    ```
    $ terraform apply
    var.project
    Our Project ID
    Enter a value: qwiklabs-gcp-04-73a4af44af08
    ```
    Enter our value Project ID

- output will be
    ```
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