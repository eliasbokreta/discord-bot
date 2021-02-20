import os


def get_audio_files(path: str, with_extensions=True):
    """List all audio files with .mp3 or .wav extensions
       from a given path. Can return a sorted list without
       extensions
    """
    files = []
    for f in os.listdir(path):
        if f.endswith(".mp3") or f.endswith(".wav"):
            files.append(f)
    if not with_extensions:
        return sorted([os.path.splitext(f)[0] for f in files])
    return sorted(files)
