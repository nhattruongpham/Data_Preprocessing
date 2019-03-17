import sys
import os
# import shutil
import xml.etree.ElementTree as ET
import glob

XML_GLOB = "*.xml"

def check_box(img_dir, xml_dir, save_dir):
    xml_glob = os.path.join(xml_dir, XML_GLOB)
    total_img = 0
    box_img = 0

    with open(os.path.join(save_dir, "Car.txt"), "w") as f:
        for xml in glob.glob(xml_glob):

            total_img += 1
            img_name = os.path.split(xml)[-1][:-4]

            tree = ET.parse(xml)
            root = tree.getroot()
            print(os.path.join(img_dir, img_name))

            if root.findall("object"):
                box_img += 1
                f.write(os.path.join(img_dir, img_name + ".jpg") + "\n")



    print("Sucessful check {} images".format(total_img))
    print("Images have box: {}".format(box_img))

    return os.path.join(save_dir, "Car.txt") # path to .txt file that contains checked files

