"""
Sound detector
"""

import argparse
import sound_detection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sound detector')

    parser.add_argument('--mode',
                        type=str, help='The mode of processing audio. Read from file or record.')

    parser.add_argument('-audiofile',
                        type=str, help='path to the audiofile')

    parser.add_argument('--reference',
                        type=str, help='path to the reference audiofile')

    parser.add_argument('-result',
                        type=str, help='Name of the file, where the result will be saved.')

    args = parser.parse_args()

    if (args.mode is None) or (args.reference is None):
        parser.error("Please, input all needed information!")
    if args.mode == 'read':
        audio = sound_detection.read_audio(args.audiofile)
    else:
        duration = int(args.mode)
        audio = sound_detection.record_audio(duration=duration)

    reference = sound_detection.read_audio(args.reference)

    cc = sound_detection.cross_correlation(audio, reference)

    if args.result:
        name = args.result
        sound_detection.display(audio, reference, cc, name)
    else:
        sound_detection.display(audio, reference, cc)