FROM apache/airflow:3.1.3

# Switch to root to install system dependencies if needed
USER root

# Install system packages if required (optional - add as needed)
# RUN apt-get update && apt-get install -y curl && apt-get clean

# Switch back to airflow user
USER airflow

# Copy the entire repository root into the image
# This includes setup.py and src/ directory needed for pip install -e
COPY --chown=airflow:airflow . /opt/airflow/spotify_project


# The RUN instruction executes during image build
# pip install -e triggers setup.py execution:
  # navigate to /opt/airflow/spotify_project
  # look for setup.py
  # execute setup.py 
# basically install the Python package located at /opt/airflow/spotify_project 
# in editable mode, without keeping installation cache.
# This makes 'from src.auth...' and 'from src.models...' work seamlessly
RUN pip install --no-cache-dir -e /opt/airflow/spotify_project

# Set environment variables for Airflow configuration
ENV PYTHONPATH=/opt/airflow/spotify_project:/opt/airflow
ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/spotify_project/src/pipelines/dags


