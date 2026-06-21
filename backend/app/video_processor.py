import subprocess
import os

def convert_to_hls(input_file, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    playlist = os.path.join(
        output_dir,
        "index.m3u8"
    )

    command = [
        "ffmpeg",
        "-i",
        input_file,
        "-codec:",
        "copy",
        "-start_number",
        "0",
        "-hls_time",
        "10",
        "-hls_list_size",
        "0",
        "-f",
        "hls",
        playlist
    ]

    subprocess.run(
        command,
        check=True
    )

    return playlist
