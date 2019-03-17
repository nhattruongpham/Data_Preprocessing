import numpy as np
from Check_box import check_box
from Check_out_of_bound import check_out_of_bound

def split_train_valid(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        f.close()

    indices = np.arange(len(lines))
    np.random.shuffle(indices)

    lines = [lines[i] for i in indices]
    train = lines[ : int(len(lines) * 0.8)]
    valid = lines[int(len(lines) * 0.8) : ]

    path = filepath[ : filepath.rfind('/') + 1]

    with open(path + "train.txt", "w") as f:
        f.writelines(train)
        f.close()

    with open(path + "valid.txt", "w") as f:
        f.writelines(valid)
        f.close()

    return path + "train.txt", path + "valid.txt"

if __name__ == "__main__":
    filepath = check_box("/home/skyo-skynet/Personal/datasets/Car/JPEGImages", "/home/skyo-skynet/Personal/datasets/Car/Annotations", "/home/skyo-skynet/Personal/datasets/Car")
    filepath = check_out_of_bound(filepath)
    # print(filepath)
    train, valid = split_train_valid(filepath)

