import pandas as pd
import numpy as np
import csv
import json
import glob
from collections import OrderedDict

path_to_files = "/Users/Marcin/Desktop/output/"
body_parts_dic = {0: "Nose",\
1: "Neck",\
2: "RShoulder",\
3: "RElbow",\
4: "RWrist",\
5: "LShoulder",\
6: "LElbow",\
7: "LWrist",\
8: "MidHip",\
9: "RHip",\
10: "RKnee",\
11: "RAnkle",\
12: "LHip",\
13: "LKnee",\
14: "LAnkle",\
15: "REye",\
16: "LEye",\
17: "REar",\
18: "LEar",\
19: "LBigToe",\
20: "LSmallToe",\
21: "LHeel",\
22: "RBigToe",\
23: "RSmallToe",\
24: "RHeel",\
25: "Background"}

vertices = ["_x", "_y", "_conf"]


def json_data_to_csv(path, outfname):
    data = []
    frames = sorted(glob.glob(f"{path}/*.json"))
    for f in frames:
        frame_no = int(f.split("_")[-2])
        with open(f, "r") as fp:
            keypoints = json.load(fp)
        for i, person in enumerate(keypoints["people"]):
            data.append(np.array([frame_no, f"person_{i}"] + person["pose_keypoints_2d"]))
    df = pd.DataFrame(data)
    df.columns = ["frame_no", "person"] + [f"p{i}_{suff}" for i in range(25) for suff in ["x", "y", "conf"]]
    df.to_csv(path_to_files + outfname)


def convert_to_names(filename):
    df = pd.read_csv(path_to_files + "out.csv")
    count = 0

    reversed_body_parts = OrderedDict(list(body_parts_dic.items()))

    with open(filename, 'r+') as csvfile:
        datareader = csv.reader(csvfile)

        row_scanned = False
        for row in datareader:
            if row_scanned:
                break
            row_scanned = True
            for column in row:
                number = ""
                # sprawdź cały tekst w danej komórce i dodaj cyfry do @number
                for letter in column:
                    if letter.isnumeric():
                        number = number + letter
                body_parts_keys = reversed_body_parts.keys()
                for key in body_parts_keys:
                    # jeśli @number zawiera któryś z key zmień nazwę na ustaloną w @body_parts_dic
                    if number == str(key):
                        if count > 2:
                            count = 0

                        new_name = body_parts_dic[key] + vertices[count]
                        df.rename(columns={column: new_name}, inplace=True)
                        count += 1
                        break

    # Usuń kolumne unnamed:0
    df.drop(columns=['Unnamed: 0'], inplace=True)
    df.to_csv(path_to_files + "out_with_names.csv")



user_path = input("Podaj ścieżkę do plików JSON (zostaw puste, jeśli jesteś na swoim maczku): ")
if len(user_path) != 0:
    path_to_files = user_path
json_data_to_csv(path_to_files, "out.csv")
convert_to_names(path_to_files + "out.csv")
print("Chyba się udało...")
