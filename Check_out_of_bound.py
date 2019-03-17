import xml.etree.ElementTree
import glob
import os

# path = "./Annotations/"

def check_out_of_bound(filepath):
    with open(filepath, "r") as f:
        filenames = f.readlines()
        f.close()

    error_file = []
    for filename in filenames:
        filename = filename.replace("\n", "")
        filename = filename.replace(".jpg", ".xml")
        filename = filename.replace("JPEGImages", "Annotations")
        # print(filename)
        e = xml.etree.ElementTree.parse(filename).getroot()
        print(e)
        for child in e:
            if child.tag == "size":
                w = float(child[0].text)
                h = float(child[1].text)
                break

        for obj in e.iter("object"):
            if float(obj[4][0].text) < 0 or float(obj[4][1].text) < 0 or float(obj[4][2].text) > w or float(obj[4][3].text) > h:
                filename = filename.replace(".xml", ".jpg")
                filename = filename.replace("Annotations", "JPEGImages")
                filename += '\n'
                error_file.append(filename)

    for filename in error_file:
        filenames.remove(filename)

    with open(filepath, "w") as f:
        f.writelines(filenames)
        f.close()

    return filepath # path to .txt file that contains checked files
