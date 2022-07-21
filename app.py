import baha
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "-u", "--username", dest="username", help="Login username", metavar="STRING"
)
parser.add_argument(
    "-p", "--password", dest="password", help="Login password", metavar="STRING"
)
parser.add_argument(
    "-cp", "--cookiepath", dest="cookiepath", help="cookie path", metavar="STRING"
)

args = parser.parse_args()

if __name__ == "__main__":
    baha.runBot(args)