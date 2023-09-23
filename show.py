import os
import glob
import argparse


def getFlist(dir_str, full):
    dirs_ = set()
    file_dirs = dir_str.split(' ')
    for file_dir in file_dirs:
        for root, dirs, files in os.walk(file_dir):
            if not full and root.split("/")[-1] == "nms-eval-9" and 'eval_bdry.txt' in files:
                    dirs_.add(os.path.join(root, 'eval_bdry.txt'))
            elif full and root.split("/")[-1] == "nms-eval" and 'eval_bdry.txt' in files:
                    dirs_.add(os.path.join(root, 'eval_bdry.txt'))

    return dirs_


def main(args):
    # get the pathes of eval_bdry.txt
    # get ODS OID
    ODS_list = []
    OIS_list = []
    result_list = []

    for txt_path in getFlist(args.dir, args.full):
        with open(txt_path) as file:
            context = file.readline().split()
            # print(float(context[0]), float(context[4]))  # ODS OIS
        ODS_list.append((txt_path, float(context[3])))
        OIS_list.append((txt_path, float(context[6])))
        # result_list.append((txt_path, float(context[3]), float(context[6]), float(context[7])))
        result_list.append((txt_path, float(context[3]), float(context[6])))

    fun_sort(ODS_list)
    fun_sort(OIS_list)
    fun_sort(result_list)
    print("==" * 20)
    # print("epoch             ODS             OIS             AP")
    print("epoch          ODS            OIS")
    print("--" * 20)
    if len(result_list) == 0:
        print("\nThere is no avaliable result to show\n")
    else:
        for i in result_list:
            print("{:10}{:12}{:16}".format(i[0].split('/')[-3], i[1], i[2]))
        # print(i[0].split('/')[-3], "     ",i[1],"     ", i[2])
        # print(i[0].split('/')[-3], "     ",i[1],"     ", i[2],"     ", i[3])
    # with open('eval/test.lst', 'w') as f:
    #     for i in ODS_list:
    #         f.write(i + '\n')
    print("==" * 20 + "\n")


def fun_sort(lst):
    return lst.sort(key=lambda a: a[1], reverse=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Show ODS & OIS')
    parser.add_argument("dir", help='choose the dir of the evaled result')
    parser.add_argument("-f", "--full", action="store_true",
                        help="if true, show the result of full test")
    args = parser.parse_args()
    main(args)
