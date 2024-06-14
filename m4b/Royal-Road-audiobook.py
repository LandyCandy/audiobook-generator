# pip install pydub mutagen ffmpeg-python
import os
import re
from pydub import AudioSegment

def get_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files

author_name = "SenescentSoul"
story_name = "Delve"
start_chap = 76
end_chap = 100

chapter_files = get_files_in_directory("\\Users\\DevUser\\code\\audiobook\\tts\\%s" % story_name)
chapter_files = [chapter_file for chapter_file in chapter_files if start_chap <= int(re.search(r'\d+', chapter_file).group()) <= end_chap]
chapter_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
chapter_names = [chapter_file.replace(".wav", '').replace('-', ' ') for chapter_file in chapter_files]

# Initialize an empty audio segment to store the audiobook
audiobook = AudioSegment.empty()

# Iterate over each chapter file and append it to the audiobook
file_to_write = "%s %s to %s" % (story_name, start_chap, end_chap)
with open("chapters.txt", 'w+') as a:
    open_lines = [';FFMETADATA1\n',
                'title=%s\n' % file_to_write,
                'artist=%s \n' % author_name]
    a.writelines(open_lines)
    for idx in range(len(chapter_files)):
        chapter_file = chapter_files[idx]
        print("Appending %s" % chapter_file)
        chapter = AudioSegment.from_file(("../tts/%s/" % story_name) + chapter_file, format="wav")
        time = len(audiobook)
        audiobook += chapter
        lines = ["[CHAPTER]\n"]
        lines.append("TIMEBASE=1/1000\n")
        lines.append("START=%s\n" % str(time))
        time = len(audiobook)
        lines.append("END=%s\n" % str(time))
        lines.append("title=%s\n" % chapter_names[idx])
        lines.append("\n")
        a.writelines(lines)

# Export the concatenated audio as an M4A file
audiobook.export("audiobook.m4a", format="ipod")

# Convert audio to audiobook
cmd = '''ffmpeg -i audiobook.m4a -i chapters.txt -map 0 -map_metadata 1 -c copy "%s.m4b"''' % file_to_write
os.system(cmd)
os.remove("audiobook.m4a")