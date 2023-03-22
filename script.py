
import argparse


def init():
    parser = argparse.ArgumentParser()
    # file/folder, 0 for webcam
    parser.add_argument('--source', type=str,
                        default='inference/images', help='source')
    parser.add_argument('--weights', nargs='+', type=str,
                        default='yolov7.pt', help='model.pt path(s)')
    opt = parser.parse_args()
    print("{'count': '" + opt.source + "'}")
    # print("INSIDE SCRIPT NAJA")
    # return "Success call this file"


if __name__ == "__main__":
    init()
