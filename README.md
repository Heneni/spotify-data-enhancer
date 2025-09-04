# Spotify Audio Feature Enricher

## Automated Usage

- Place your Spotify track IDs in `input_tracks.json`.
- Every time you push a change to `input_tracks.json`, GitHub Actions automatically runs the enrichment script.
- Output file: `enriched_tracks_with_audio_features.json`.

## Manual Usage (Codespaces/Locally)

1. Install dependencies:
    ```
    pip install spotipy python-dotenv tqdm pandas
    ```
2. Run the script:
    ```
    python spotify_audio_feature_enricher.py
    ```

## Troubleshooting

- Credentials are stored in `.env`. If you ever change your Spotify app, update this file.
- API rate limits are handled automatically.
- For help, just ask Copilot in your Codespace!