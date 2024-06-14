import re
import os
import torch
from TTS.api import TTS as tts

# Get device
device = "cpu"
if torch.cuda.is_available():
    print("Cuda is available")
    torch.cuda.empty_cache()
    device = "cuda"

def get_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files

def run_tts(path_to_text, output_path, start_chapter, end_chapter):

    # Init TTS with the target model name
    tts_model = tts(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    chap_list = get_files_in_directory(path_to_text)
    chap_list.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    chap_list = [chap_file for chap_file in chap_list if start_chapter <= int(re.search(r'\d+', chap_file).group()) <= end_chapter]

    for chap_name in chap_list:
        OUTPUT_PATH = output_path + "/%s.wav" % (chap_name.replace(".txt", ""))
        with open("%s\\%s" % (path_to_text, chap_name), "r", encoding="utf8") as text_file:
            text_to_tts = text_file.read()

        banned_chars = ['“ ', '”', "'", '"', '[', ']', '<', '>', '(', ')', '…']
        for char in banned_chars:
            text_to_tts = text_to_tts.replace(char, " ")
        text_to_tts = text_to_tts.replace('...', '.')
        text_to_tts = text_to_tts.replace('’', "'")
        text_to_tts = text_to_tts.replace('LV', "level ")

        # This one is special, need to break up lines to be less than 400 tokens
        text_to_tts = text_to_tts.replace(',', ".")
        tts_model.tts_to_file(text=text_to_tts,
                            # speaker="Ana Florence",
                            speaker='Baldur Sanjin',
                            language="en",
                            speed=1.5,
                            file_path=OUTPUT_PATH,
                            split_sentences=True)

if __name__ == "__main__":
    path_to_text = "\\Users\\DevUser\\code\\audiobook\\html-scraper\\Delve"
    output_path = "./Delve"
    start_chapter = 107
    end_chapter = 150
    run_tts(path_to_text=path_to_text, output_path=output_path, start_chapter=start_chapter, end_chapter=end_chapter)

#Models
#  1: tts_models/multilingual/multi-dataset/xtts_v2
    #Speakers
    # ['Claribel Dervla',
    # 'Daisy Studious',
    # 'Gracie Wise',
    # 'Tammie Ema',
    # 'Alison Dietlinde',
    # 'Ana Florence',
    # 'Annmarie Nele',
    # 'Asya Anara',
    # 'Brenda Stern',
    # 'Gitta Nikolina',
    # 'Henriette Usha',
    # 'Sofia Hellen',
    # 'Tammy Grit',
    # 'Tanja Adelina',
    # 'Vjollca Johnnie',
    # 'Andrew Chipper',
    # 'Badr Odhiambo',
    # 'Dionisio Schuyler',
    # 'Royston Min',
    # 'Viktor Eka',
    # 'Abrahan Mack',
    # 'Adde Michal',
    # 'Baldur Sanjin',
    # 'Craig Gutsy',
    # 'Damien Black',
    # 'Gilberto Mathias',
    # 'Ilkin Urbano',
    # 'Kazuhiko Atallah',
    # 'Ludvig Milivoj',
    # 'Suad Qasim',
    # 'Torcull Diarmuid',
    # 'Viktor Menelaos',
    # 'Zacharie Aimilios',
    # 'Nova Hogarth',
    # 'Maja Ruoho',
    # 'Uta Obando',
    # 'Lidiya Szekeres',
    # 'Chandra MacFarland',
    # 'Szofi Granger',
    # 'Camilla Holmström',
    # 'Lilya Stainthorpe',
    # 'Zofija Kendrick',
    # 'Narelle Moon',
    # 'Barbora MacLean',
    # 'Alexandra Hisakawa',
    # 'Alma María',
    # 'Rosemary Okafor',
    # 'Ige Behringer',
    # 'Filip Traverse',
    # 'Damjan Chapman',
    # 'Wulf Carlevaro',
    # 'Aaron Dreschner',
    # 'Kumar Dahl',
    # 'Eugenio Mataracı',
    # 'Ferran Simen',
    # 'Xavier Hayasaka',
    # 'Luis Moray',
    # 'Marcos Rudaski']
#  2: tts_models/multilingual/multi-dataset/xtts_v1.1
#  3: tts_models/multilingual/multi-dataset/your_tts
#  4: tts_models/multilingual/multi-dataset/bark
#  11: tts_models/en/ljspeech/tacotron2-DDC [already downloaded]
#  12: tts_models/en/ljspeech/tacotron2-DDC_ph
#  13: tts_models/en/ljspeech/glow-tts
#  14: tts_models/en/ljspeech/speedy-speech
#  15: tts_models/en/ljspeech/tacotron2-DCA
#  16: tts_models/en/ljspeech/vits
#  17: tts_models/en/ljspeech/vits--neon
#  18: tts_models/en/ljspeech/fast_pitch
#  19: tts_models/en/ljspeech/overflow
#  20: tts_models/en/ljspeech/neural_hmm
#  21: tts_models/en/vctk/vits
#  22: tts_models/en/vctk/fast_pitch
#  23: tts_models/en/sam/tacotron-DDC
#  24: tts_models/en/blizzard2013/capacitron-t2-c50
#  25: tts_models/en/blizzard2013/capacitron-t2-c150_v2
#  26: tts_models/en/multi-dataset/tortoise-v2
#  27: tts_models/en/jenny/jenny

#Vocoders (voices)
#  1: vocoder_models/universal/libri-tts/wavegrad
#  2: vocoder_models/universal/libri-tts/fullband-melgan
#  3: vocoder_models/en/ek1/wavegrad
#  4: vocoder_models/en/ljspeech/multiband-melgan
#  5: vocoder_models/en/ljspeech/hifigan_v2 [already downloaded]
#  6: vocoder_models/en/ljspeech/univnet
#  7: vocoder_models/en/blizzard2013/hifigan_v2
#  8: vocoder_models/en/vctk/hifigan_v2
#  9: vocoder_models/en/sam/hifigan_v2