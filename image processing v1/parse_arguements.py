from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='Segment bloodstains in an spatter pattern')
    parser.add_argument("-f", "--file", dest="filename",
                        help="file from base path", metavar="FILE")
    parser.add_argument("-F", "--AbsoluteFile", help="file from root", dest="full_path")
    parser.add_argument("-s", "--scale", dest="scale", type=float,
                        help="scale in pixels per mm", metavar="SCALE", default=7)
    parser.add_argument("-o", "--OutputPath", dest="output_path",
                        help="folder and base name for output", metavar="OUTPUT_PATH")
    parser.add_argument("-b", "--batch", dest="batch",  default=False,
                        help="Do not display preview or interactive graph output", metavar="BATCH")

    args = parser.parse_args()
    return vars(args)

def parse_batch_args():
    parser = ArgumentParser(description='Batch process segmenting bloodstain spatter patterns')
    parser.add_argument("-f", "--folder", dest="folder",
                        help="batch process folder from base path", metavar="FOLDER")
    parser.add_argument("-F", "--AbsoluteFolder", dest="full_path",
                        help="batch process abosolute path", metavar="FOLDER")
    parser.add_argument("-s", "--scale", dest="scale", type=float,
                        help="scale in pixels per mm", metavar="SCALE", default=7)
    parser.add_argument("-o", "--OutputPath", dest="output_path",
                        help="folder and base name for output", metavar="OUTPUT_PATH")

    args = parser.parse_args()
    return vars(args)