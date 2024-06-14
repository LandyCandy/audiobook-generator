# pip install pydub mutagen ffmpeg-python
import os
from pydub import AudioSegment

# List of file paths for each chapter
# chapter_files = ['PoA-320', 'PoA-321', 'PoA-322', 'PoA-323', 'PoA-324', 'PoA-325']
chapter_files = ['PoA-326', 'PoA-327', 'PoA-328', 'PoA-329', 'PoA-330', 'PoA-331']

#List of names for each chapter
# chapter_names = ['PoA 320', 'PoA 321', 'PoA 322', 'PoA 323', 'PoA 324', 'PoA 325']
chapter_names = ['PoA 326', 'PoA 327', 'PoA 328', 'PoA 329', 'PoA 330', 'PoA 331']

# Initialize an empty audio segment to store the audiobook
audiobook = AudioSegment.empty()

# Iterate over each chapter file and append it to the audiobook
file_to_write = "Path of Ascension 326 to 331"
with open("chapters.txt", 'w+') as a:
    open_lines = [';FFMETADATA1\n',
                'title=%s\n' % file_to_write,
                'artist=C Mantis\n']
    a.writelines(open_lines)
    for idx in range(len(chapter_files)):
        chapter_file = chapter_files[idx]
        chapter = AudioSegment.from_file("../tts/PoA/" + chapter_file + '.wav', format="wav")
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