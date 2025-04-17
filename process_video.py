import os
import cv2
from ultralytics import YOLO
from tqdm import tqdm # For progress bar


def process_video(video_path, model_path, output_path="output_video.mp4"):
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: The file {video_path} does not exist.")
        return None

    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Error: The model file {model_path} does not exist.")
        return None

    # Load the YOLOv8 model
    model = YOLO(model_path)

    # Open video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video was successfully opened
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video properties - Width: {width}, Height: {height}, FPS: {fps}")

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Ensure the output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Use mp4v codec for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Check if VideoWriter is successfully opened
    if not out.isOpened():
        print("Error: Failed to open video writer.")
        cap.release()
        return None

    # Process the video with a progress bar
    with tqdm(total=total_frames, desc="Processing video", unit="frame") as pbar:
        frame_count = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                # End of video
                if frame_count > 0:
                    print("Finished processing video.")
                else:
                    print("Error: Failed to read frame.")
                break

            frame_count += 1

            # Run YOLOv8 inference on the frame
            # Only detect your custom classes with confidence threshold
            results = model(frame, conf=0.3, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Write the annotated frame to the output video
            out.write(annotated_frame)

            # Update the progress bar
            pbar.update(1)  # Update by one frame

    # Release video objects
    cap.release()
    out.release()
    print(f"Processed video saved to: {output_path}")
    return output_path


# Define video directory (Change to your dir)
video_dir = "D:/Pycharm Projects/New folder/Input_Video/"

# Get the first video file in the directory (assuming there's only one)
video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

if video_files:
    video_filename = video_files[0]  # Take the first video found
    video_path = os.path.join(video_dir, video_filename)

    # Define output video path, keeping the original name
    output_video_dir = "D:/Pycharm Projects/New folder/Output_Videos/"# Change to output dir
    output_video_path = os.path.join(output_video_dir, video_filename)

    # Path to your custom trained model
    model_path = "runs/detect/train/weights/best.pt"

    # Process the video
    output_folder = process_video(video_path, model_path, output_video_path)

    # Verify the output
    if output_folder:
        print(f"Processed video saved to: {output_folder}")
    else:
        print("Video processing failed.")
else:
    print("No video files found in the input folder.")
