from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='Segment bloodstains in an spatter pattern')
    parser.add_argument("-f", "--file", dest="filename",
                        help="file from base path", metavar="FILE")
    parser.add_argument("-F", "--AbsoluteFile", help="file from root", dest="full_path")
    parser.add_argument("-s", "--scale", dest="scale", type=int,
                        help="scale in pixels per mm", metavar="SCALE", default=7)

    args = parser.parse_args()
    return vars(args)