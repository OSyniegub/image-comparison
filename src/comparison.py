from PIL import Image as img
import numpy as np
import sys
import os


class Comparison:
    def __init__(self):
        self.img1 = None
        self.img2 = None
        self.images = []
        self.files = []
    @staticmethod
    def read_data(self):
        if len(sys.argv) == 2:
            if sys.argv[1] == "--help" or sys.argv[1] == "-h":
                print("usage: solution.py [-h] --path PATH\n"
                      "\n"
                      "First test task on images similarity.\n"
                      "\n"
                      "optional arguments:\n"
                      "  -h, --help            show this help message and exit\n"
                      "  --path PATH           folder with images")
            else:
                print("Error.\nusage: app.py [-h] --path PATH.")
                exit(1)
        elif len(sys.argv) == 3:
            if sys.argv[1] == "--path":
                try:
                    directory_name = sys.argv[2]
                    if not os.path.isdir(directory_name):
                        print("Expected directory as input")
                        exit(1)
                    self.files = [f for f in os.listdir(directory_name) if os.path.isfile(os.path.join(directory_name, f))]
                    for image in self.files:
                        self.images.append(img.open(directory_name+"/"+image).convert("L"))
                except IOError:
                    print("Opening error")
                    exit(1)
            else:
                print("Error.\nusage: app.py [-h] --path PATH.")
        else:
            print("1 argument expected")
            exit(1)

    def threshold(self, err, th=5 * (10 ** (-3))):
        if err == 0:
            return 0
        elif 2 * (10 ** (-3)) <= err <= th:
            return 1
        elif err >= 0.01:
            return 3
        return 2

    # Mean Squared Error
    def mse(self, img1, img2):
        err = np.sum((img1 - img2) ** 2)
        if img1.size == img2.size:
            err /= float(img1.size * img2.size)
        else:
            err /= float(8 * 8)
        return err

    def image_comparison(self):
        result = ['duplicate', 'similar', 'modified', 'different images']
        img1 = np.asarray(self.img1, dtype=np.float)
        img2 = np.asarray(self.img2, dtype=np.float)
        if img1.size == img2.size:
            pass
        elif img1.size > img2.size:
            img2 = np.asarray(self.img2.resize((8, 8), img.ANTIALIAS), dtype=np.float)
            img1 = np.asarray(self.img1.resize((8, 8), img.ANTIALIAS), dtype=np.float)
        else:
            img1 = np.asarray(self.img1.resize((8, 8), img.ANTIALIAS), dtype=np.float)
            img2 = np.asarray(self.img2.resize((8, 8), img.ANTIALIAS), dtype=np.float)
        return result[self.threshold(self.mse(img1, img2))]

    def run(self):
        self.read_data(self)
        for i, image1 in enumerate(self.images):
            for j, image2 in enumerate(self.images):
                if i == j:
                    continue
                self.img1 = image1
                self.img2 = image2
                result = self.image_comparison()
                if not result == "different images":
                    print(self.files[i] + " " + self.files[j] + " - " + result)
