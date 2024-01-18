# This is a sample Python script.
import os
import shutil
import time
import zipfile
from tkinter import filedialog as fd
from PIL import Image, ImageFont
import numpy as np
from PIL import ImageDraw

MAX_FILE_SIZE = 20479999


def find_best_method(file_path):
    file_name = file_path.split("/")[-1]
    smallest = 0
    best_method = zipfile.ZIP_STORED
    for method in [zipfile.ZIP_DEFLATED, zipfile.ZIP_LZMA, zipfile.ZIP_BZIP2]:
        zip_file = zipfile.ZipFile("test.zip", mode="w", compression=method, compresslevel=9)
        zip_file.write(file_path, file_name)
        zipped_size = zip_file.getinfo(file_name).compress_size
        print(zipped_size, file_name)
        zip_file.close()
        if smallest == 0 or zipped_size < smallest:
            smallest = zipped_size
            best_method = method
    os.remove("test.zip")
    return best_method


def make_zips():
    dir_name = fd.askdirectory()
    test_file_path = dir_name + "/" + os.listdir(dir_name)[0]
    method = find_best_method(test_file_path)
    dir_files = os.listdir(dir_name)
    dir_files.sort()
    all_files = [x for x in dir_files if x[0] != "."]
    file_number = 1
    file_name_base = input("Name for zip files: ")
    zip_file_path = f"{dir_name}/{file_name_base}_{file_number:02}.zip"
    zip_file = zipfile.ZipFile(zip_file_path, mode="w", compression=method, compresslevel=9)
    archive_size = 0
    for filename in all_files:
        new_file_size = os.path.getsize(dir_name + "/" + filename)
        if new_file_size + archive_size > MAX_FILE_SIZE:
            zip_file.close()
            file_number += 1
            zip_file_path = f"{dir_name}/{file_name_base}_{file_number:02}.zip"
            zip_file = zipfile.ZipFile(zip_file_path, mode="w", compression=method, compresslevel=9)
            archive_size = 0
        zip_file.write(dir_name + "/" + filename, filename)
        zipped_size = zip_file.getinfo(filename).compress_size
        archive_size += zipped_size
    zip_file.close()


def load_palette():
    with open("color palette values.txt") as f:
        pal = f.readlines()
        color_list = []
        for line in pal:
            color_name, color_value = line.split(" ", 1)
            start = color_value.index("(") + 1
            end = color_value.index(")")
            rgb_values = color_value[start:end]
            rgb_array = rgb_values.split(", ")
            final_color = (int(rgb_array[0]), int(rgb_array[1]), int(rgb_array[2]), 255)
            color_list.append((color_name, final_color))
        return color_list


def make_images():
    pattern_file = fd.askopenfilename()
    pattern_location = pattern_file.rsplit("/", 1)[0]
    pattern_img = Image.open(pattern_file)
    background_color = Image.new("RGBA",(3600, 3600), "#ffffff")
    os.mkdir("png")
    for (color_name, color_value) in load_palette():
        pattern_color = Image.new("RGBA", (3600, 3600), color_value)
        comp = Image.composite(pattern_color, background_color, pattern_img)
        save_path = f"{pattern_location}/png/{color_name}.png"
        comp.save(save_path, dpi=(300, 300))


def make_images_and_zips():
    pattern_file = fd.askopenfilename()
    pattern_location = pattern_file.rsplit("/", 1)[0]
    pattern_img = Image.open(pattern_file)
    background_color = Image.new("RGBA",(3600, 3600), "#ffffff")
    if os.path.exists("png") and os.path.isdir("png"):
        shutil.rmtree("png")
    os.mkdir("png")
    method = find_best_method(pattern_file)
    file_name_base = input("Name for zip files: ")
    file_number = 1
    zip_file_path = f"{pattern_location}/{file_name_base}_{file_number:02}.zip"
    zip_file = zipfile.ZipFile(zip_file_path, mode="w", compression=method, compresslevel=9)
    archive_size = 0
    for (color_name, color_value) in load_palette():
        pattern_color = Image.new("RGBA", (3600, 3600), color_value)
        comp = Image.composite(pattern_color, background_color, pattern_img)
        file_name = f"{color_name}.png"
        save_path = f"{pattern_location}/png/{file_name}"
        comp.save(save_path, dpi=(300, 300))

        curr_file_size = os.path.getsize(save_path)
        if archive_size + curr_file_size > MAX_FILE_SIZE:
            zip_file.close()
            file_number += 1
            zip_file = zipfile.ZipFile(f"{pattern_location}/{file_name_base}_{file_number:02}.zip")
            archive_size = 0

        zip_file.write(save_path, file_name)
        archive_size += zip_file.getinfo(file_name).compress_size
    zip_file.write("DigitalWhims Color Chart.png", "DigitalWhims Color Chart.png")
    zip_file.close()


# def make_images_and_zips():
#     pattern_file = fd.askopenfilename()
#     pattern_img = Image.open(pattern_file)
#     background_color = Image.new("RGBA",(3600, 3600), "#ffffff")
#     pattern_color = Image.new("RGBA", (3600, 3600), "#ffffff")
#     os.mkdir("png")
#     for (color_name, color_value) in load_palette():
#         comp = Image.composite(pattern_color, background_color, pattern_img)
#         comp.save(f"png1/{color_name}.png")

def generate_label(pattern_name):
    img = Image.new("RGBA", (3600, 680), color=(255, 255, 255))
    logo = Image.open("digital whims logo cropped transparent.png")
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype("Sweety Strawberry.ttf", size=180)
    desc_font = ImageFont.truetype("Barlow-Regular.ttf", size=82)
    draw.text((60, 60), f"100 {pattern_name} Digital Papers", font=title_font, fill="black")
    draw.text((60, 340), "Digital Scrapbook Papers\n300 dpi PNG format\n100 sheets", font=desc_font, fill="black")
    img.paste(logo, (2740, 100), logo)
    draw.line((0, 10, 3600, 10), fill="black", width=20)
    draw.line((0, 670, 3600, 670), fill="black", width=20)
    img.show()


if __name__ == '__main__':
    generate_label("Buffalo Check Plaid")
    # make_images_and_zips()
    # process_image()
    # make_zips()
