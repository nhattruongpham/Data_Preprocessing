from auto_gen_augment import *
from shutil import copyfile
import xml.etree.ElementTree as ET
import numpy as np
import os, glob
import cv2


rhflip = RandomHorizontalFlip(0.4)
# rvflip = RandomVerticalFlip(0.6)
rscale = RandomScale(0.2, diff = True)  
rtranslate = RandomTranslate(0.2, diff = True)
rrotate = RandomRotate((25, 90))
rshear = RandomShear(0.4)
rnoise = RandomNoise(typical=(1, 6))
transforms = [rhflip, rscale, rtranslate, rrotate, rshear, rnoise]
# print(int(len(transforms) -0))
# print(transforms[0])


def get_bboxes(xml_file):
    bboxes = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
        xmin = round(float(member[4][0].text), 0)
        ymin = round(float(member[4][1].text), 0)
        xmax = round(float(member[4][2].text), 0)
        ymax = round(float(member[4][3].text), 0)
        bboxes.append((xmin, ymin, xmax, ymax))
    bboxes = np.asarray(bboxes)

    return bboxes


def get_images(img_file):
    img = cv2.imread(img_file)

    return img



if __name__ == '__main__':
    input_path = '/home/skyo-skynet/Personal/myhubs/augmentation/input'
    output_path = '/home/skyo-skynet/Personal/myhubs/augmentation/output'
    temp = 0

    for i, file in enumerate(glob.glob(os.path.join(input_path, "*.jpg"))):
        img_file = file
        xml_file = file.replace('.jpg', '.xml')
        file_name = img_file.split('/')[-1].split('.')[0]
        out_xml = os.path.join(output_path, file_name + '_' + str(i) + '.xml')
        out_img = out_xml.replace('.xml', '.jpg')
        img = get_images(img_file)
        bboxes = get_bboxes(xml_file)
        if temp <= int(len(transforms) - 1):
            r_img, r_coords = transforms[temp](img, bboxes)
            temp = temp + 1
        else:
            temp = 0
            r_img, r_coords = transforms[temp](img, bboxes)
        # copyfile(xml_file, out_xml)
        # tree = ET.parse(out_xml)
        # root = tree.getroot()
        if (r_coords is not None) and (r_img is not None):
            copyfile(xml_file, out_xml)
            tree = ET.parse(out_xml)
            root = tree.getroot()
            for j, member in enumerate(root.findall('object')):
                # print(j)
                try:
                    if j == 0:
                        member[4][0].text = str(r_coords[0][0])
                        member[4][1].text = str(r_coords[0][1])
                        member[4][2].text = str(r_coords[0][2])
                        member[4][3].text = str(r_coords[0][3])
                    elif j > 0:
                        member[4][0].text = str(r_coords[j][0])
                        member[4][1].text = str(r_coords[j][1])
                        member[4][2].text = str(r_coords[j][2])
                        member[4][3].text = str(r_coords[j][3])
                    else:
                        pass
                except IndexError:
                    pass

            tree.write(out_xml)
            cv2.imwrite(out_img, r_img)
        else:
            pass
        print("Done: ", i + 1)
        print("*************")
        # cv2.imshow("Image", r_img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
