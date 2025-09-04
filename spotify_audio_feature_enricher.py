import json
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# --- Load credentials from .env ---
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

assert SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI, (
    "Please set your .env credentials first!\n"
    "You need: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI"
)

# --- Setup Spotify API client ---
scope = "user-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    open_browser=False
))

# --- Read Input File ---
input_path = Path('input_tracks.json')
if not input_path.exists():
    raise FileNotFoundError(f"Input file {input_path} not found.")

if input_path.suffix == ".json":
    with open(input_path, 'r') as f:
        input_data = json.load(f)
        if isinstance(input_data, dict):
            input_data = list(input_data.values())
elif input_path.suffix == ".csv":
    df = pd.read_csv(input_path)
    input_data = df.to_dict(orient='records')
else:
    raise ValueError("Input file format not supported (.json or .csv only)")

def batch_iterator(iterable, batch_size=100):
    length = len(iterable)
    for i in range(0, length, batch_size):
        yield iterable[i:i+batch_size]

def fetch_audio_features_batch(track_ids: List[str]) -> Dict[str, Any]:
    try:
        response = sp.audio_features(tracks=track_ids)
        return {f['id']: f for f in response if f}
    except spotipy.SpotifyException as e:
        if e.http_status == 429:
            retry_seconds = int(e.headers.get('Retry-After', 5))
            print(f"Rate limit, sleeping for {retry_seconds} seconds...")
            time.sleep(retry_seconds)
            return fetch_audio_features_batch(track_ids)
        print(f"SpotifyException: {e}")
        return {}
    except Exception as e:
        print(f"Error fetching batch: {e}")
        return {}

def fetch_audio_features_single(track_id: str) -> Optional[dict]:
    try:
        feat = sp.audio_features([track_id])
        return feat[0] if feat and feat[0] else None
    except spotipy.SpotifyException as e:
        if e.http_status == 429:
            retry_seconds = int(e.headers.get('Retry-After', 5))
            print(f"Rate limit (1), sleeping for {retry_seconds} seconds...")
            time.sleep(retry_seconds)
            return fetch_audio_features_single(track_id)
        print(f"SpotifyException for {track_id}: {e}")
        return None
    except Exception as e:
        print(f"Error for track {track_id}: {e}")
        return None

track_id_map = {d['track_id']: d for d in input_data if 'track_id' in d}
track_ids = list(track_id_map.keys())

BATCH_SIZE = 100

for batch in tqdm(list(batch_iterator(track_ids, BATCH_SIZE)), desc="Processing batches"):
    features = fetch_audio_features_batch(batch)
    for tid in batch:
        if tid in features and features[tid]:
            track_id_map[tid]['audio_features'] = features[tid]
        else:
            single = fetch_audio_features_single(tid)
            track_id_map[tid]['audio_features'] = single if single else None

output_filename = "enriched_tracks_with_audio_features.json"
output_path = Path(output_filename)
with open(output_path, "w") as f:
    json.dump(list(track_id_map.values()), f, indent=2)
print(f"Done! Output saved to {output_path.resolve()}")