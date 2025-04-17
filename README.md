# 🚦 Traffic AI Tracking with YOLOv8

## Overview
This project is a traffic detection and tracking system built using **Python**, **YOLOv8**, and **OpenCV**. It:
- Downloads a driving video from YouTube using `yt-dlp`.
- Converts the video to MP4 format using FFmpeg if needed.
- Detects and tracks vehicles frame-by-frame using YOLOv8.
- Outputs a processed video with bounding boxes and class labels.

## Features

1. **Smart YouTube Video Downloader**
   - Downloads high-quality MP4 format using `yt-dlp`.
   - Auto-renames the video to `video.mp4` for easier processing.
   - Optional: Converts video format using FFmpeg.

2. **YOLOv8 Object Detection**
   - Uses a custom-trained YOLOv8 model.
   - Detects cars, trucks, and other traffic objects in real-time.

3. **OpenCV-Based Video Processing**
   - Reads input video and writes annotated output.
   - Displays bounding boxes and labels on vehicles.
   - Saves the final tracked video to the `output/` folder.

4. **Command-Line Simplicity**
   - Customizable input/output paths.
   - Optional FFmpeg conversion support.

## How It Works

1. Run the `download_video.py` script to fetch and optionally convert a YouTube video.
2. Run the `track_traffic.py` script to process the downloaded video using YOLOv8.
3. The final annotated video is saved in the `output/` folder.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/traffic-ai-tracking.git
   cd traffic-ai-tracking
