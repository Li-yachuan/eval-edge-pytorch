import os
from argparse import ArgumentParser

from nms_process import nms_process
from impl.edges_eval_dir import edges_eval_dir

from os.path import join


def eval_one_epoch(args):

    print(args.root)
    result_dir = join(args.root, "mat")  # forward result directory
    nms_dir = join(args.root, "nms")  # forward result directory

    datasets = {
        "BSDS": "../GT/BSDS",
        "BIPED": "../GT/BIPED",
        "NYUD": "../GT/NYUD"
    }

    gt_dir = datasets[args.dataset]

    key = args.key  # x = scipy.io.loadmat(filename)[key]
    file_format = args.file_format  # ".mat" or ".npy"

    thrs = 99 if not args.light else 9

    nms_process(result_dir, nms_dir, key, file_format)
    edges_eval_dir(nms_dir, gt_dir, thrs=thrs, thin=1, max_dist=0.0075, workers=-1)


if __name__ == '__main__':
    parser = ArgumentParser("edge eval")
    parser.add_argument("root", type=str, default="examples/hed_result", help="results directory")
    parser.add_argument("--key", type=str, default="img", help="key")
    parser.add_argument("--file_format", type=str, default=".mat", help=".mat or .npy")
    parser.add_argument("--workers", type=int, default="-1", help="number workers, -1 for all workers")
    parser.add_argument("--dataset")
    parser.add_argument("-l","--light",action="store_true")
    args = parser.parse_args()
    eval_one_epoch(args)
