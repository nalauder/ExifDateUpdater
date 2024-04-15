import argparse
from os import walk
from PIL import Image
import re
import pyexiv2

def main(path, date, guess):
     images = identify_images(path)
     for image in images:
        if guess:
            det_date = determine_date(image)
            date = det_date if det_date is not None else date
        
        set_date(image, date)



def set_date(file, date):
    with pyexiv2.Image(file) as img:
        new_exif = {'Exif.Image.DateTime'}
        img.save



def determine_date(file):
    year_regex = "\D(19[7,8,9]\d|20[0,1,2]\d)\D"
    res = re.findall(year_regex, file)
    no_potential_years = len(res)
    if no_potential_years == 0:
        return None
    elif no_potential_years == 1:
        return res[0]
    else:
        print("Please enter the year you would like to use from:\n",file)
        for i in range(no_potential_years):
            print("\t",i+1,"-", res[i])
        selection = input("Selection:")
        try:
            return res[int(selection)-1]
        except:
            print("Invalid selection :(")
            return None

def identify_images(path):
    images_missing_data = []
    for root, dirs, files in walk(path):
        for file in files:
            file_path = "{}/{}".format(root, file)
            if is_image(file_path):
                with Image.open(file_path) as img:
                    exif = img.getexif()
                    if exif is None or 306 not in exif:
                        images_missing_data.append(file_path)
    
    return images_missing_data
    

def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Exif Date Updater",
        description="Finds files with missing Creation Date metadata and attempts to fill it in"
    )

    parser.add_argument('path')
    parser.add_argument('-d', '--date')
    parser.add_argument('-b', '--backup')
    parser.add_argument('-g', '--guess', action='store_true')

    args = parser.parse_args()

    main(args.path, args.date, args.guess, args.backup)