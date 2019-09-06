# @author Dominik Dziuba
# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import argparse
from Modules.AnalyticalProcessing import Processor as AProcessor
from Modules.MachineLearning import Processor as MLProcessor


def main():
    parser = argparse.ArgumentParser(description='This is a program for detecting whether image is blurred.')

    preprocessing = parser.add_argument_group('Preprocessing')
    # options for preprocessing such as adding blur, changing color space, etc
    preprocessing.add_argument('-b', '--blur', action='store_true', help='Randomly apply blur to random fraction of an image.')

    subparser = parser.add_subparsers()

    analytical = subparser.add_parser('a', help='Contains options for analytical algorithms for detecting blur.')
    # options for processing images that involve analitycal approach to detecting blur such as Fourier filter
    analytical.add_argument('-f', '--fourier', help='Applies Fourier\'s filter to detect if an image is blurred.')
    machine_learning = subparser.add_parser('ml', help='Contains options for machine learning driven algorithms for detecting blur.')
    # options for processing images that involve machine learning methods for detecting blur
    machine_learning.add_argument('-ml', '--machine-learning', help='Applies machine learning model to detect blurred images.')

    options = parser.parse_args()
    if options['a']:
        AProcessor.process(options)
    elif options['ml']:
        MLProcessor.process(options)


if __name__ == "__main__":
    main()

