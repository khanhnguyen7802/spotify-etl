from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

from airflow.sdk import dag, task

default_args = {
    'owner': 'khanh',
    'retries': 1,
}

# Create DAG
@dag(
    dag_id='my_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 12, 9),
    schedule='@hourly',
    catchup=False,
    description='pipeline to get recently played tracks from Spotify API and export to CSV',
)
def my_dag():

    # Define task functions
    @task(multiple_outputs=True, task_id='authenticate')
    def task_authenticate(**context):
        from src.pipelines.scripts.refresh_token import init, refresh_token
        
        spotify_auth = init()
        refresh_token(spotify_auth)
        
        # Return token info as a dictionary to be used in XCom
        return {
            "_access_token": spotify_auth.access_token,
            "_refresh_token": spotify_auth.refresh_token,
            "_access_token_expiration_time": spotify_auth.access_token_expiration_time,
            "_client_id": spotify_auth.client_id,
            "_client_secret": spotify_auth.client_secret
        }

    @task(multiple_outputs=True, task_id='get_recently_played_tracks')
    def task_get_recently_played_tracks(**context):
        from src.pipelines.scripts.spotify_etl import get_recently_played, extract_data
        
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

    @task(task_id='export_data')
    def task_export_data(**context):
        # Get task instance from context
        ti = context.get('task_instance')
        if ti is None:
            raise ValueError("task_instance not available in context")
        
        # Get recently played tracks data from previous task
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
            from src.pipelines.scripts.spotify_etl import export_to_csv
            export_to_csv(record, class_name)
        
        return "Data export completed successfully"


    # Set dependencies
    task_authenticate() >> task_get_recently_played_tracks() >> task_export_data()

my_dag()