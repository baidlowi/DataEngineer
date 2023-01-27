# Docker and SQL

## Commands 

- ### Downloading the data

    ```bash
    wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
    ```

- ### Running Postgres with Docker

    ```bash
    docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
    ```

- ### CLI for Postgres

    Installing `pgcli`

    ```bash
    pip install pgcli
    ```

    Using `pgcli` to connect to Postgres

    ```bash
    pgcli -h localhost -p 5432 -u root -d ny_taxi
    ```

- ### pgAdmin

    Running pgAdmin

    ```bash
    docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
    ```

## Running Postgres and pgAdmin together

- Create a network

    ```bash
    docker network create pg-network
    ```

- Run Postgres (change the path)

    ```bash
    docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v c:/Users/alexe/git/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
    ```

- Run pgAdmin

    ```bash
    docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin-2 \
    dpage/pgadmin4
    ```


## Data ingestion

- create file [ingest_data.py](./ingest_data.py) to ingest data to postgresql

- install requirement
    ```
    pip install pandas sqlalchemy psycopg2
    ```
    ```
    python3 ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    ```

- Run the script with Docker

    ```bash
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

    docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
    ```

## Docker-Compose 

- Create file [docker-compose.yaml](./docker-compose.yaml)

- Run it:

    ```bash
    docker-compose up
    ```

- Shutting it down:

    ```bash
    docker-compose down
    ```

