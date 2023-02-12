Pre Installed in Linux
```
apt update
apt install python3-pip wget docker.io 
```

```
curl -L https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

```
nano requirements.txt
nano docker-compose.yaml
nano ingest_data.py
```

```
pip install -r requirements.txt
docker-compose up
python3 ingest_data.py
```