# This script will extract only the Spanish part of the podcast 

import soundfile
import numpy as np
import time
import librosa
import os
import logging
from pydub import AudioSegment


PODCAST_PATH = r'C:\Users\Chris\Documents\Python\StoryLearningSpanish\podcast-test'
OUTPUT_PATH = r'C:\Users\Chris\Documents\Python\StoryLearningSpanish\podcast-test'

def convert_to_wav(input_path, output_path):
    """Takes all the .m4a in input_path and convert them to
     .wav in output_path"""
    logger = logging.getLogger(__name__)
    audio_files = os.listdir(input_path)
    
    for audio_file in audio_files:
        logger.info('Test')
        audio_path = os.path.join(input_path, audio_file)
        audio_name, audio_ext = audio_file.split('.')        
        track = AudioSegment.from_file(audio_path, audio_ext)
        wav_path = os.path.join(output_path, audio_name + '.wav')
        track.export(wav_path, format='wav')
    

def read_jingle(sr=1000):
    """Returns the jingle on which to cut the music off on"""
    pass


def main():

    convert_to_wav(PODCAST_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    start = time.time()
    logging.basicConfig(filename='info.log', 
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    main()
    print('It took {0:0.1f} seconds'.format(time.time() - start))


# from pydub import AudioSegment	

# file_path = r'C:\Users\Chris\Desktop\StoryLearning\Podcast\0.m4a'


# track = AudioSegment.from_file(file_path, 'm4a')
# wav_path = r'C:\Users\Chris\Desktop\StoryLearning\Podcast\0.wav'

# track.export(wav_path, format='wav')

# import soundfile as sf
# import numpy as np
# import time
# import librosa


# jingle_path = r'C:\Users\Chris\Desktop\StoryLearning\Podcast\jingle.wav'
# podcast_path = r'C:\Users\Chris\Desktop\StoryLearning\Podcast\0.wav'


# # data_jingle, samplerate_jingle = sf.read(jingle_path)
# # data_pc, samplerate_pc = sf.read(podcast_path)

# start_time = time.time()
# data_jingle, samplerate_jingle = librosa.load(jingle_path, sr=8000)
# data_pc, samplerate_pc = librosa.load(podcast_path, sr=8000)
# print("Read time:", time.time() - start_time)


# start_time = time.time()

# cor = np.correlate(data_pc, data_jingle, mode='valid')
# arg_max = np.argmax(cor)
# print(arg_max, cor[arg_max])

# print(time.time() - start_time)

