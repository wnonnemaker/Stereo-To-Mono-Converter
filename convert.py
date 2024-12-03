import os
import subprocess
from pydub import AudioSegment
from tkinter import Tk
from tkinter.filedialog import askdirectory

def convert_to_stereo(input_file, output_file):
    # Load the input audio file (Pydub will auto-detect format based on file extension)
    audio = AudioSegment.from_file(input_file)

    # Check if the audio is stereo
    if audio.channels == 2:
        # Extract the left and right channels
        left_channel = audio.split_to_mono()[0]
        right_channel = left_channel  # Duplicate left channel to right

        # Combine left and right channels into a stereo track
        stereo_audio = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
    else:
        # If it's mono, duplicate it for both channels
        stereo_audio = AudioSegment.from_mono_audiosegments(audio, audio)

    # Export the converted audio to the output path in the same format as the input file
    stereo_audio.export(output_file, format=output_file.split('.')[-1])  # Export using the original format
    print(f"Converted {input_file} to stereo and saved as {output_file}")

def convert_folder(input_folder, output_folder):
    # Check if output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all files in the input folder
    for file_name in os.listdir(input_folder):
        # Ensure we're only dealing with audio files (wav and m4a in this case, you can add more extensions)
        if file_name.endswith((".wav", ".m4a")):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)
            input_file_path = input_file_path.replace("\\", "/")
            output_file_path = output_file_path.replace("\\", "/")

            # Call the function to convert the audio to stereo
            print(input_file_path)
            print(output_file_path)
            convert_to_stereo(input_file_path, output_file_path)

#This part of the code converts all files to wav

def remove_spaces_in_filename(file_name):
    """
    Remove spaces from the file name and replace with underscores.
    """
    return file_name.replace(" ", "_")



def convert_m4a_to_wav(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".m4a"):
            new_file_name = remove_spaces_in_filename(file_name)
            print(new_file_name)
            # Rename the file if it contains spaces
            if file_name != new_file_name:
                os.rename(os.path.join(input_folder, file_name), os.path.join(input_folder, new_file_name))
                file_name = new_file_name  # Update to use the renamed file
                
            input_file_path = os.path.join(input_folder, file_name)
            # Create corresponding .wav file name
            output_file_name = os.path.splitext(file_name)[0] + ".wav"
            output_file_path = os.path.join(output_folder, output_file_name)
            input_file_path = input_file_path.replace("/", "\\")
            output_file_path = output_file_path.replace("/", "\\")
            print(input_file_path)
            print(output_file_path)
            open(output_file_path, "w")
            
            if not os.path.exists(input_file_path):
                print(f"Input file not found: {input_file_path}")
            if not os.path.exists(output_file_path):
                print(f"Output path not valid: {output_file_path}")
            
            # Use FFmpeg to convert the file
            #command = ["ffmpeg", "-i", f'"{input_file_path}"', f'"{output_file_path}"']
            #subprocess.run(command, check=True)
            track = AudioSegment.from_file(input_file_path,  format= 'm4a')
            file_handle = track.export(output_file_path, format='wav')
            print(f"Converted {input_file_path} to {output_file_path}")


if __name__ == "__main__":
    # Hide the root tkinter window
    root = Tk()
    root.withdraw()

    print("Welcome to the Audio Converter Tool!")
    
    # Open file explorer to select input folder
    print("Please select the input folder containing your audio files.")
    input_folder = askdirectory(title="Select Input Folder")
    if not input_folder:
        print("No input folder selected. Exiting.")
        exit()

    output_folder = os.path.join(os.path.dirname(input_folder), "new_stereo_audios")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    else:
        print(f"Using existing output folder: {output_folder}")

    # Open file explorer to select output folder
    print("Converting .m4a files to .wav format...")
    convert_m4a_to_wav(input_folder, output_folder)
    print("Conversion to .wav completed.")
    
    print("Converting audio to stereo format...")
    convert_folder(output_folder, output_folder)
    print("Stereo conversion completed.")
