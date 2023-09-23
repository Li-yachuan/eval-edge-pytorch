import os
import time
from datetime import datetime
import argparse
from eval_component import eval_one_epoch
num_test = {"BSDS": 200, "BRIND": 200, "NYUD": 654, "BIPED": 50, "UDED": 30}


def need_test(root, dset,full):
    flag = False
    sub_pth = os.listdir(root)
    flag_dir = "nms-eval" if full else "nms-eval-9"
    if ("png" in sub_pth) and ("mat" in sub_pth) and (flag_dir not in sub_pth):
        png_num = len(os.listdir(os.path.join(root, "png")))
        mat_num = len(os.listdir(os.path.join(root, "mat")))
        if png_num == num_test[dset] and mat_num == num_test[dset]:
            flag = True

    return flag


def getFlist(args):
    dirs_ = set()
    file_dirs = args.eval_dir.split(' ')
    print("*" * 40)
    for file_dir in file_dirs:
        for root, _, _ in os.walk(file_dir):
            if need_test(root, args.dataset,args.full):
                dirs_.add(root)
                print(root)
    print("*" * 40+"\n")
    return dirs_


class Quit_timer(object):
    def __init__(self, T, limit):
        self.time_flag = 0
        self.sleep_time = T
        self.quit_ceiling = limit

    def sleep(self):
        if self.time_flag == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M"), end=' ')
            print("no avaliable png,start to sleep ...")
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M"), end=' ')
            print("no avaliable png:")
        time.sleep(self.sleep_time * 3600)
        self.time_flag += self.sleep_time
        self.quit()

    def quit(self):
        if self.time_flag >= self.quit_ceiling:
            print("No new data has been generated for {} hours, the program automatically exits".format(
                self.quit_ceiling))
            exit(1)

    def refresh(self):
        self.time_flag = 0


class Parser_One_Epoch(object):
    def __init__(self,root,dataset,full):
        self.root = root
        self.dataset = dataset
        self.key = "img"
        self.file_format = ".mat"
        self.full = full

def mian_func(args):
    qtimer = Quit_timer(args.T, args.limit)
    while True:
        fset = getFlist(args)
        if len(fset) != 0:
            for updataset in fset:
                parser_one_epoch = Parser_One_Epoch(updataset,args.dataset,args.full)
                eval_one_epoch(parser_one_epoch)

            qtimer.refresh()
        else:
            if args.notwait:
                print("no avaliable result and args.notwait is true, return process")
                return
            qtimer.sleep()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='eval output')
    parser.add_argument('--T', type=float, default=0.5, help="sleep time,defult 0.5 hour")
    parser.add_argument('--limit', type=float, default=8, help="time of empty cycle(hours)")
    parser.add_argument("-nw", '--notwait', action="store_true", help="whether wait new result")
    parser.add_argument("-d", '--dataset', default=None)
    parser.add_argument("-f", '--full', action="store_true")

    parser.add_argument('eval_dir')
    args = parser.parse_args()

    if args.dataset is not None:
        for dataset in num_test.keys():
            if dataset in args.dataset.upper():
                args.dataset = dataset
                break
    else:
        for dataset in num_test.keys():
            if dataset in args.eval_dir.upper():
                args.dataset = dataset
                break

    if args.dataset is None:
        raise Exception("Point out dataset in test dir OR point out dataset in args.dataset")
    print("Start to eval result ...")
    mian_func(args)
