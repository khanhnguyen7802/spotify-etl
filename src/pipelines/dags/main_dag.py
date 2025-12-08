from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

import src.helper.utils as utils
from src.models.SpotifyAlbum import SpotifyAlbum
from src.models.SpotifyArtist import SpotifyArtist
from src.models.SpotifyPlayer import SpotifyPlayer
from src.models.SpotifyTrack import SpotifyTrack
from src.auth.SpotifyAuth import SpotifyAuth

# Import your callable
from src.pipelines.scripts.refresh_token import init, refresh_token
from src.pipelines.scripts.spotify_etl import *

# Create DAG
dag = DAG(
    'my_pipeline',
    start_date=datetime(2025, 12, 9),
    schedule='@hourly',
    description='pipeline to get recently played tracks from Spotify API and export to CSV',
    catchup=False
)


# Define task functions
def task_authenticate(**context):
    spotify_auth = init()
    refresh_token(spotify_auth)
    
    # Return token info with underscore-prefixed keys to match spotify_etl.py expectations
    return {
        "_access_token": spotify_auth.access_token,
        "_refresh_token": spotify_auth.refresh_token,
        "_access_token_expiration_time": spotify_auth.access_token_expiration_time,
        "_client_id": spotify_auth.client_id,
        "_client_secret": spotify_auth.client_secret
    }

def task_get_recently_played_tracks(**context):
    try:
        # Get task instance from context
        ti = context.get('task_instance')
        if ti is None:
            raise ValueError("task_instance not available in context")
        
        # Get token info from previous task
        token_info = ti.xcom_pull(task_ids='authenticate')
        
        if token_info is None:
            raise ValueError("Failed to get token_info from authenticate task XCom")
        
        recently_played_tracks = get_recently_played(token_info) 
        artist_list, album_list, track_list, playback_list = extract_data(recently_played_tracks, token_info)
        
        return {
            "artist_list": [artist.to_dict() for artist in artist_list],
            "album_list": [album.to_dict() for album in album_list],
            "track_list": [track.to_dict() for track in track_list],
            "playback_list": [playback.to_dict() for playback in playback_list]
        }
    except Exception as e:
        raise Exception(f"Error in task_get_recently_played_tracks: {str(e)}") from e

def task_export_data(**context):
    # Get task instance from context
    ti = context.get('task_instance')
    if ti is None:
        raise ValueError("task_instance not available in context")
    
    # Get data from previous task
    recently_played_data = ti.xcom_pull(task_ids='get_recently_played_tracks')
    
    if recently_played_data is None:
        raise ValueError("Failed to get data from get_recently_played_tracks task XCom")
    
    class_names = ["artist", "album", "track", "playback"]
    
    records = [
        recently_played_data["artist_list"],
        recently_played_data["album_list"],
        recently_played_data["track_list"],
        recently_played_data["playback_list"]
    ]

    for class_name, record in zip(class_names, records):
        export_to_csv(record, class_name)
    
    return "Data export completed successfully"


# Create tasks
authenticate_task = PythonOperator(
    task_id='authenticate',
    python_callable=task_authenticate,
    dag=dag
)

get_recently_played_tracks_task = PythonOperator(
    task_id='get_recently_played_tracks',
    python_callable=task_get_recently_played_tracks,
    dag=dag
)

export_data_task = PythonOperator(
    task_id='export_data',
    python_callable=task_export_data,
    dag=dag
)

# Set dependencies
authenticate_task >> get_recently_played_tracks_task >> export_data_task

