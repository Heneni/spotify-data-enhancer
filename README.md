# Spotify Data Enhancer

Enhance your Spotify listening history with detailed audio features and analysis using the Spotify Web API.

## 🚀 Quick Start Options

### Option 1: Test with 1000 Records (Recommended First)
```bash
python test_1000_records.py
```
**Time**: ~15-20 minutes | **Purpose**: Validate everything works perfectly

### Option 2: Full Dataset with Analysis  
```bash
python spotify_enhancer.py --analysis
```
**Time**: ~6-8 hours | **Purpose**: Process all 54,513 tracks

### Option 3: Sample Test
```bash
python spotify_enhancer.py --sample 100 --analysis
```
**Time**: ~3-5 minutes | **Purpose**: Quick functionality test

## 📊 What This Does

- **Authenticates** with Spotify API using your credentials
- **Processes** tracks in batches of 50 for efficiency
- **Adds 13+ audio features** from Spotify's official database
- **Includes detailed analysis** (bars, beats, sections, segments)
- **Handles rate limiting** automatically with retry logic
- **Provides real-time progress** updates and error tracking

## 🧪 1000-Record Test Details

The `test_1000_records.py` script:
- ✅ Creates 1000 test records with popular track URIs
- ✅ Tests all API endpoints (audio-features + audio-analysis)
- ✅ Validates authentication and rate limiting
- ✅ Demonstrates full functionality in ~15-20 minutes
- ✅ Outputs detailed performance statistics
- ✅ Perfect for validation before running full dataset

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

| Dataset Size | Features Only | With Analysis | Purpose |
|-------------|---------------|---------------|---------|
| 100 tracks | ~3 minutes | ~5 minutes | Quick test |
| 1,000 tracks | ~8 minutes | ~15 minutes | Validation test |
| 54,513 tracks | ~3 hours | ~6-8 hours | Full processing |

*Note: Times depend on API rate limits and network speed*

## 🔧 Usage Examples

```bash
# 1. Test with 1000 records (RECOMMENDED FIRST)
python test_1000_records.py

# 2. Quick sample test
python spotify_enhancer.py --sample 100 --analysis

# 3. Full dataset processing
python spotify_enhancer.py tracks_for_import.csv enhanced_output.csv --analysis

# 4. Features only (no analysis)
python spotify_enhancer.py tracks_for_import.csv enhanced_output.csv
```

## 🔐 API Credentials

The enhancer uses your Spotify app credentials:
- **Client ID**: `efef0dbb87ee4c37b550508ae2791737`
- **Client Secret**: `09c12b5178734b5aae18743d5b4335d5`
- **App Name**: "my PlayListREader"
- **Status**: Development mode ✅

## 📋 Requirements

- Your CSV must have a `spotify_track_uri` column
- Track URIs should be in format: `spotify:track:TRACK_ID`
- Python 3.11+ (automatically installed in Codespace)
- Internet connection for API calls

## 🧪 Testing Strategy

1. **Start with 1000-record test**: `python test_1000_records.py`
   - Validates all functionality
   - Tests API authentication  
   - Confirms data quality
   - Shows performance metrics

2. **If test passes, run full dataset**: `python spotify_enhancer.py --analysis`
   - Processes all 54,513 tracks
   - Adds detailed analysis
   - Takes 6-8 hours total

## 🐛 Troubleshooting

**File not found error?**
- Make sure your CSV is named `tracks_for_import.csv` or specify the path

**Authentication failed?**
- Check that your Spotify app is in Development mode
- Verify your Client ID and Secret are correct

**Rate limited?**
- The enhancer automatically handles rate limits with delays
- Large datasets will take several hours due to API limits

**Want to test first?**
- Always run `python test_1000_records.py` before the full dataset

## 📁 Output Files

- `test_tracks_1000.csv` - Generated test data (1000 records)
- `enhanced_test_1000_results.csv` - Enhanced test results  
- `enhanced_spotify_tracks.csv` - Full dataset results

## 🚀 Performance Features

- ✅ Batch processing (50 tracks per request)
- ✅ Automatic retry on failures
- ✅ Rate limit handling with exponential backoff
- ✅ Real-time progress tracking
- ✅ Comprehensive error logging
- ✅ Resume capability on interruption
- ✅ Performance statistics and success rates

## 📊 Expected Results

For 1000-record test:
- **Success rate**: >95%
- **Processing time**: 15-20 minutes
- **API calls**: ~20 batch requests + 1000 analysis requests
- **Output columns**: 33 original + 22 enhanced = 55 total

For full dataset (54,513 tracks):
- **Success rate**: >90% 
- **Processing time**: 6-8 hours
- **API calls**: ~1,100 batch requests + 54,513 analysis requests
- **Output size**: ~15-20 MB CSV file

Ready to enhance your Spotify data! 🎵

---

**🧪 Recommended**: Start with `python test_1000_records.py` to validate everything works perfectly!