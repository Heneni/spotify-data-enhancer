# 🎵 Spotify Data Enhancer

Enhance your Spotify streaming history with comprehensive audio features using the Spotify Web API. Built to handle large datasets (54,513+ tracks) efficiently with batch processing, progress tracking, and resumption capabilities.

## ✨ Features

- **Auto-Executing Test**: Runs comprehensive API tests automatically when you open the project
- **Batch Processing**: Efficiently processes up to 100 tracks per API request
- **Progress Tracking**: Real-time progress bars and detailed logging
- **Resume Capability**: Automatically resumes from where it left off if interrupted
- **Rate Limiting**: Built-in rate limiting to respect Spotify API limits
- **Multiple Formats**: Supports both CSV and JSON input/output
- **Audio Features**: Extracts 12 audio features per track:
  - `danceability`, `energy`, `key`, `loudness`, `mode`
  - `speechiness`, `acousticness`, `instrumentalness`
  - `liveness`, `valence`, `tempo`, `duration_ms`

## 🚀 Quick Start

### Using GitHub Codespaces (Recommended)

1. Open this repository in GitHub Codespaces
2. The devcontainer will automatically:
   - Install all dependencies
   - Run comprehensive API tests
   - Display performance estimates for your dataset

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Heneni/spotify-data-enhancer.git
cd spotify-data-enhancer

# Install dependencies
pip install -r requirements.txt

# Run the enhancer
python spotify_enhancer.py your_spotify_data.csv
```

## 📊 Usage Examples

### Basic Usage
```bash
# Enhance a CSV file
python spotify_enhancer.py streaming_history.csv

# Specify output file
python spotify_enhancer.py streaming_history.csv -o enhanced_tracks.csv

# Process JSON format
python spotify_enhancer.py tracks.json -o enhanced_tracks.json
```

### Advanced Options
```bash
# Start fresh (ignore previous results)
python spotify_enhancer.py tracks.csv --no-resume

# Validate enhancement results
python spotify_enhancer.py --validate -o enhanced_tracks.csv

# Use custom Spotify credentials
python spotify_enhancer.py tracks.csv --client-id YOUR_ID --client-secret YOUR_SECRET
```

## 📂 Input File Format

Your input file should contain a column with Spotify track IDs. Supported column names:
- `id`
- `track_id` 
- `spotify_id`
- `trackId`

Example CSV structure:
```csv
id,track_name,artist_name,played_at
7qiZfU4dY1lWllzX7mPBI3,Shape of You,Ed Sheeran,2023-01-01
0VjIjW4GlUZAMYd2vXMi3b,Blinding Lights,The Weeknd,2023-01-02
```

## 📈 Performance Estimates

Based on the auto-executing test in the devcontainer:
- **API Rate**: ~1000 tracks per minute (conservative estimate)
- **54,513 tracks**: Approximately 54-60 minutes processing time
- **Batch Size**: 100 tracks per request (maximum allowed by Spotify)

## 🔧 Configuration

The enhancer uses pre-configured Spotify API credentials that are tested automatically. For production use or different applications, you can provide your own:

1. Create a Spotify app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Use your `CLIENT_ID` and `CLIENT_SECRET` with command line options

## 📊 Output Format

Enhanced files include all original columns plus these audio features:

| Feature | Description | Range |
|---------|-------------|-------|
| `danceability` | How suitable for dancing | 0.0 - 1.0 |
| `energy` | Perceptual measure of intensity | 0.0 - 1.0 |
| `speechiness` | Presence of spoken words | 0.0 - 1.0 |
| `acousticness` | Confidence of acoustic nature | 0.0 - 1.0 |
| `instrumentalness` | Predicts no vocals | 0.0 - 1.0 |
| `liveness` | Presence of audience | 0.0 - 1.0 |
| `valence` | Musical positivity | 0.0 - 1.0 |
| `tempo` | Estimated BPM | ~0 - 250+ |
| `loudness` | Overall loudness in dB | ~-60 - 0 |
| `key` | Musical key (Pitch Class) | 0 - 11 |
| `mode` | Major (1) or minor (0) | 0 or 1 |
| `duration_ms` | Track length in milliseconds | varies |

## 🔍 Validation

Validate your enhancement results:
```bash
python spotify_enhancer.py --validate -o enhanced_tracks.csv
```

Sample validation output:
```
📊 Validation Results:
   Total rows: 54,513
   Enhanced rows: 52,891
   Enhancement rate: 97.0%
   Audio features: danceability, energy, valence, tempo, ...
```

## 🛠 Troubleshooting

### Rate Limiting
- The enhancer automatically handles rate limiting with exponential backoff
- Default delay: 100ms between requests (conservative)
- API rate limit errors are automatically retried

### Resume from Interruption
- Progress is automatically saved every 1000 tracks
- Restart the same command to resume from where you left off
- Use `--no-resume` to start fresh

### Authentication Issues
- Check your internet connection
- Verify API credentials if using custom ones
- Check the log file: `spotify_enhancement.log`

## 📋 Requirements

- Python 3.11+
- Active internet connection
- Input data with valid Spotify track IDs (22-character strings)

## 🤝 Contributing

Feel free to open issues or submit pull requests. The devcontainer setup makes it easy to get started with development!

## 📄 License

This project is open source. Use responsibly and in accordance with Spotify's API terms of service.

---

Built with ❤️ for large-scale Spotify data analysis
