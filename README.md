# Spotify Data Enhancer

Enhance your Spotify listening history with detailed audio features and analysis using the Spotify Web API.

## 🚀 Quick Start in GitHub Codespace

1. Upload your `tracks_for_import.csv` file to the workspace
2. Run the enhancer with analysis:
   ```bash
   python spotify_enhancer.py --analysis
   ```

## 📊 What This Does

- **Authenticates** with Spotify API using your credentials
- **Processes** your CSV in batches of 50 tracks
- **Adds 13+ audio features** from Spotify's database
- **Includes detailed analysis** (bars, beats, sections, segments)
- **Handles rate limiting** automatically
- **Provides real-time progress** updates

## 🔧 Usage Options

```bash
# Full enhancement with detailed analysis (recommended)
python spotify_enhancer.py --analysis

# Test with sample data first
python spotify_enhancer.py --sample 100 --analysis

# Basic enhancement only (no analysis)
python spotify_enhancer.py

# Custom file paths
python spotify_enhancer.py my_tracks.csv output.csv --analysis
```

## 📈 Enhanced Data Output

### Audio Features Added:
- `enhanced_acousticness` - Acoustic quality (0.0 to 1.0)
- `enhanced_danceability` - How danceable the track is
- `enhanced_energy` - Perceptual intensity and power
- `enhanced_tempo` - BPM (beats per minute)
- `enhanced_valence` - Musical positivity/mood
- `enhanced_loudness` - Overall loudness in dB
- `enhanced_speechiness` - Presence of spoken words
- `enhanced_instrumentalness` - Likelihood of no vocals
- `enhanced_liveness` - Presence of audience/live recording
- `enhanced_key` - Musical key (0-11)
- `enhanced_mode` - Modality (0=minor, 1=major)
- `enhanced_time_signature` - Time signature
- `duration_ms` - Track length in milliseconds

### Detailed Analysis Added (with --analysis flag):
- `bars_count` - Number of musical bars
- `beats_count` - Number of beats detected
- `sections_count` - Number of musical sections
- `segments_count` - Number of audio segments
- `tatums_count` - Number of tatums (shortest rhythmic unit)
- `first_section_tempo` - Tempo of the first section
- `first_section_loudness` - Loudness of the first section
- `first_section_key` - Key of the first section
- `first_section_mode` - Mode of the first section

## ⏱️ Processing Time Estimates

- **Sample (100 tracks)**: ~3-5 minutes
- **Full dataset (54K+ tracks)**: ~6-8 hours with analysis
- **Features only**: ~2-3 hours without analysis

*Note: Processing time depends on API rate limits and network speed*

## 🔐 API Credentials

The enhancer uses your Spotify app credentials:
- **Client ID**: `efef0dbb87ee4c37b550508ae2791737`
- **Client Secret**: `09c12b5178734b5aae18743d5b4335d5`
- **Redirect URI**: `http://127.0.0.1:8080/callback`

## 📋 Requirements

- Your CSV must have a `spotify_track_uri` column
- Track URIs should be in format: `spotify:track:TRACK_ID`
- Python 3.11+ (automatically installed in Codespace)
- Internet connection for API calls

## 🐛 Troubleshooting

**File not found error?**
- Make sure your CSV is named `tracks_for_import.csv` or specify the path

**Authentication failed?**
- Check that your Spotify app is in Development mode
- Verify your Client ID and Secret are correct

**Rate limited?**
- The enhancer automatically handles rate limits with delays
- Large datasets will take several hours due to API limits

## 📁 Output

Creates `enhanced_spotify_tracks.csv` with:
- All your original columns
- 13+ new audio feature columns
- 9 detailed analysis columns (if --analysis used)
- Same number of rows as input

## 🚀 Performance Tips

1. **Test first**: Use `--sample 100` to verify everything works
2. **Use analysis**: The `--analysis` flag adds valuable musical structure data
3. **Let it run**: Large datasets take time due to API rate limits
4. **Check progress**: The tool shows real-time progress and success rates

Enjoy your enhanced Spotify data! 🎵