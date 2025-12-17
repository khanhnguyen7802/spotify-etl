# Get started with Docker in Linux
For the Linux VM, we only need the `Docker Engine` (optimize as much as possible to reduce the RAM usage on this tiny VM).

For the installation guide, follow [Install using the `apt` repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). 

After having installed Docker, run the following command:
```bash
sudo usermod -a -G docker $your_username
# e.g., sudo usermod -a -G docker khanh 
``` 
👉 This command adds a user to the **docker group** so they can run Docker commands without `sudo`:
```bash
docker ps
docker compose up
```


# Get started with Airflow 
Since we already had Docker, we will be pulling the `Airflow image` from Docker. 

I have an article on Medium about [General picture of Airflow](https://medium.com/learning-data/apache-airflow-3-0-a-general-to-deep-picture-part-1-d09cee921cd7) that also includes installation guide. 

As the VM is only 4GB RAM, we need to reduce and tweak the services provided in Airflow (check [`docker-compose.yaml`](../docker-compose.yaml)). The minimum requirements include: `airflow-apiserver`, `airflow-dag-processor` and `airflow-scheduler`.


## The overall workflow 
1. Define the project using [`setup.py`](../setup.py). \
➡️ This transforms the folder structure into installable Python package (namely **spotify-wrapped**), which allows you to use absolute imports like 
```py
from src.models.SpotifyAlbum import SpotifyAlbum
```

2. Build the environment with [Dockerfile](../Dockerfile). This file creates the actual computer (container) where the code runs.

- `FROM`: Starts with the base image **apache/airflow:3.1.3**.
- `COPY`: copy all project files into /opt/airflow/spotify_project.
- `RUN pip install ...`: as the project is treated as a Python package (with the `src` folder is now a top-level package), this runs `setup.py` to install the project in "editable" mode \
➡️ Ensures when Airflow tries to `import src...`, Python knows exactly where to look.
- `ENV`: set environment variable -> `PYTHONPATH` affects Python’s import system (ensure modules are found when importing).

3. Running the infrastructure with [`docker-compose.yaml`](../docker-compose.yaml). This file manages multiple services that make up Airflow. 

4. The real orchestration in [`main_dag.py`](../src/pipelines/dags/main_dag.py). It consists of 3 tasks:
- `task_authenticate`: the authentication token is refreshed automatically at the start of this pipeline.
- `task_get_recently_played_tracks`: fetch raw JSON data from Spotify
- `task_export_data`: export as CSV files

# Additional notes 
## docker-compose.yaml 
- **Build context**: usually, `docker-compose.yaml` and `Dockerfile` are placed at **root**. Thus, when we define 
  ```
  build:
    context: .
    dockerfile: ./Dockerfile
  ```
  it will have access to all files in this project. 


- **Define volumes**: 
  - The `volumes section` at the **top level** of a `docker-compose.yaml` defines named volumes that can be referenced and reused across your services. These are persistent storage locations **managed by Docker**. For example:
    ```
    volumes:
      postgres-db-volume:
    ```
    acts as a container for data that persists even after containers are **stopped or removed** *(can only removed if you specifically remove it)*. For a database like PostgreSQL, this is crucial. \
    ❌ Without a named volume, every time you stop and restart your database container, all your data would disappear. \
    ✅ By declaring this volume here, a persistent storage location is created to keep data safe across container lifecycle events.
  
  - In case we already had a **Docker volume** *(previously created)*, we just need to declare it as **external**. For example, we have a volume called `defined_volume`, thus we declare as follows:
    ```docker
    volume:
      defined_volume:
        external: true 
    ```

  - Other lower level volumes are basically doing the **volume mapping**. For example: 
    ```py
    volumes:
      # Mount the entire repository root for development
      - ${AIRFLOW_PROJ_DIR:-.}/src:/opt/airflow/spotify_project/src

      # ${AIRFLOW_PROJ_DIR:-.}/data maps to /opt/airflow/spotify_project/data
      - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/spotify_project/data 

    ```
    The mapping means that any changes which take place on the **host machine** *(/SpotifyWrapped/src)* will also occur in the **cotainer** *(/opt/airflow/spotify_project/src)*.