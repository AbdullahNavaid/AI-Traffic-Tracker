import os
import yt_dlp
import subprocess
from yt_dlp.utils import DownloadError


# Function to download video and convert it using FFmpeg if available
def download_video(url, download_folder, ffmpeg_path=None):
    # Set up the options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Prefer mp4 format
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Output filename pattern
        'merge_output_format': 'mp4',  # Force merged output to be mp4
    }

    # If FFmpeg path is provided, add it to the options
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    # Initialize yt-dlp downloader
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', 'mp4')
            video_filename = f"{video_title}.{video_ext}"
            video_path = os.path.join(download_folder, video_filename)

            print(f"Downloaded video: {video_path}")

            # Rename the downloaded video to "video" in the input folder
            new_video_path = os.path.join(download_folder, "video.mp4")

            if os.path.exists(video_path):
                # Rename the video file to "video.mp4"
                os.rename(video_path, new_video_path)
                print(f"Renamed video to: {new_video_path}")
                video_path = new_video_path

            # If FFmpeg is available and we need to convert (e.g., from webm to mp4)
            if ffmpeg_path and video_ext != 'mp4':
                # Use subprocess to call FFmpeg directly instead of the Python wrapper
                output_path = os.path.join(download_folder, "video_converted.mp4")

                # Create the full path to ffmpeg executable
                ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')

                # Check if the file exists before attempting conversion
                if not os.path.exists(video_path):
                    print(f"Warning: Downloaded file not found at {video_path}")
                    # Try to find the actual file
                    for file in os.listdir(download_folder):
                        if "video" in file:
                            video_path = os.path.join(download_folder, file)
                            print(f"Found video at: {video_path}")
                            break

                if os.path.exists(video_path):
                    # Build the FFmpeg command
                    command = [
                        ffmpeg_exe,
                        '-i', video_path,
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-strict', 'experimental',
                        output_path
                    ]

                    # Run the command
                    print("Starting FFmpeg conversion...")
                    result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        print(f"Video converted to: {output_path}")
                        # Don't remove original until we're sure conversion succeeded
                        # os.remove(video_path)
                        return output_path
                    else:
                        print(f"Conversion failed. FFmpeg output: {result.stderr}")
                        return video_path
                else:
                    print(f"Cannot convert: Video file not found")
                    return None

            return video_path

        except DownloadError as e:
            print(f"Error downloading video: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


# Example usage
download_folder = "D:/Pycharm Projects/New folder/Input_Video"  # Modify as per your folder
url = "https://www.youtube.com/watch?v=qYFhF4uu6dA"  # Replace with URL

# Specify your FFmpeg installation path (replace with the correct path if needed)
ffmpeg_path = r"C:\ffmpeg\bin"  # Update this path to where FFmpeg is installed

video_path = download_video(url, download_folder, ffmpeg_path)
if video_path:
    print(f"Video saved as: {video_path}")
else:
    print("Video download or conversion failed.")
