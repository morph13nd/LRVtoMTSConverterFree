import os
import subprocess
from pathlib import Path

def convert_lrv_to_mts(input_folder, output_folder_name="converted_mts"):
    # Get script's directory
    script_dir = Path(__file__).parent.resolve()
    
    # Create output folder if it doesn't exist
    output_folder = script_dir / output_folder_name
    output_folder.mkdir(exist_ok=True)
    
    # Verify FFmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: FFmpeg not found. Please install FFmpeg and add it to your system PATH.")
        return

    # Process files
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".lrv"):
            input_path = Path(input_folder) / filename
            output_path = output_folder / f"{Path(filename).stem}.mts"
            
            print(f"Converting {filename}...")
            
            try:
                subprocess.run([
                    "ffmpeg",
                    "-i", str(input_path),
                    "-c", "copy",  # Copy stream without re-encoding
                    "-y",  # Overwrite output file if exists
                    str(output_path)
                ], check=True)
                print(f"Success: {output_path.name}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {filename}: {str(e)}")

if __name__ == "__main__":
    input_folder = input("Enter the path to the folder containing LRV files: ")
    if Path(input_folder).is_dir():
        convert_lrv_to_mts(input_folder)
        print("\nConversion complete!")
    else:
        print("Invalid directory path. Please provide a valid folder path.")
