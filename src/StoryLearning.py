# This script will extract only the Spanish part of the podcast 

import soundfile
import numpy as np
import time
import librosa
import os
import csv
import logging
from shutil import copyfile
from pydub import AudioSegment

HOME_PATH = r'C:\Users\Chris\Documents\Python\StoryLearningSpanish'
PODCAST_PATH = os.path.join(HOME_PATH, 'podcast-prior')
OUTPUT_PATH = os.path.join(HOME_PATH, 'podcast-after')
META_DATA_PATH = os.path.join(HOME_PATH, 'meta-data')
SAMPLE_RATE = 1000
START_IN_SECONDS = 74
END_IN_SECONDS = 36

def convert_to_wav(input_path, output_path):
    """Takes all the .m4a in input_path and convert them to
     .wav in output_path"""
    logger = logging.getLogger(__name__)
    audio_files = os.listdir(input_path)
    

    for audio_file in audio_files:

        if audio_file.endswith('wav'):
            logging.info(f"{audio_file} is not a .m4a file.")
            continue

        audio_path = os.path.join(input_path, audio_file)
        audio_name, audio_ext = audio_file.split('.')

        
        processed_audio_files = os.listdir(output_path)
        processed_audio_files = [x.strip('.wav') 
                                for x in processed_audio_files]
        if audio_name in processed_audio_files:
            logger.info(f'{audio_name} already processed, continuing')
            continue

        logger.info(f'Converting {audio_name} ... ')
        track = AudioSegment.from_file(audio_path, audio_ext)
        wav_path = os.path.join(output_path, audio_name + '.wav')
        track.export(wav_path, format='wav')
        logger.info(f'Converting {audio_name} Done')

        audio_manager(output_path)

def read_audio_file(path, sample_rate=SAMPLE_RATE,
                    start=None, end=None):
    """Returns audio as readable signals

    @params:
        path -> str : path to the audio file
        sample_rate -> int : sample_rate to read the audio signal
                             can be lower than the original audio
        start -> int : time in seconds to begin sampling
        end -> int : time in seconds from the end to stop sampling

    """

    if not path.endswith('wav'):
        logging.info(f"{path} is not a .wav file.")
        return

    song_data, _ = librosa.load(path, sr=sample_rate)

    if not start and not end:
        return song_data

    start_sample = int(start * SAMPLE_RATE)
    end_sample = int(end * SAMPLE_RATE)

    return song_data[start_sample:-end_sample]


def split_audio(signal, split=2):
    signal_length = len(signal)
    return signal[:signal_length//split]


def find_offset_time(audio, jingle):
    cor = np.correlate(audio, jingle, mode='valid')
    arg_max = np.argmax(cor)

    return arg_max / SAMPLE_RATE


def audio_manager(temp_path):
    # Iterates through all the audio files in the folder to be processed

    logger = logging.getLogger(__name__)
    jingle_path = os.path.join(HOME_PATH, 'jingle', 'jingle.wav')

    logger.info("Reading jingle path")
    jingle_data = read_audio_file(jingle_path)

    audio_files = os.listdir(temp_path)
    for audio_file in audio_files:
        audio_file_path = os.path.join(temp_path, audio_file)

        logger.info(f"Reading {audio_file}")
        podcast_data = read_audio_file(audio_file_path, 
                                       start=START_IN_SECONDS,
                                       end=END_IN_SECONDS)

        podcast_data = split_audio(podcast_data)

        logger.info(f"Finding offset of {audio_file}")
        offset_time = find_offset_time(podcast_data, jingle_data)

        output_path = os.path.join(OUTPUT_PATH, audio_file.strip('.wav') + '.mp3')

        print("Start = ", START_IN_SECONDS, "End = ", START_IN_SECONDS + offset_time)
        
        sound = AudioSegment.from_file(audio_file_path)
        interested_piece = sound[START_IN_SECONDS*1000:(START_IN_SECONDS + offset_time)*1000]
        interested_piece.export(output_path, format="mp3")

        logger.info(f"Removing {audio_file_path}")
        os.remove(audio_file_path)




def rename_files(path):
    """ Rename files to their chapter titles """

    audio_files = sorted(os.listdir(path))
    chapter_title_filepath = os.path.join(META_DATA_PATH, 'Chapter_Titles.csv')

    chapter_titles = []
    with open(chapter_title_filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            chapter_titles.append(row[0])
        
    for index, audio_file in enumerate(audio_files):
        
        original_path = os.path.join(path, str(index) + '.mp3')
        out_name = chapter_titles[index]
        new_path = os.path.join(path, out_name + '.mp3') 
        copyfile(original_path, new_path)



def main():


    Create a temp folder to delete at the end
    temp_path = os.path.join(HOME_PATH, 'temp')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    convert_to_wav(PODCAST_PATH, temp_path)

    rename_files(OUTPUT_PATH)

if __name__ == "__main__":
    start = time.time()
    logging.basicConfig(filename='info.log', 
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    main()
    print('It took {0:0.1f} seconds'.format(time.time() - start))
