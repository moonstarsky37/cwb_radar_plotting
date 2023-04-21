import matplotlib.pyplot as plt
import numpy as np
from zipfile import ZipFile
from glob import glob
import os
import json
import sys
import numpy as np
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from utils.ziyu_cmap import cmap_NWSReflectivity


class RadarPlotter:
    def __init__(self,
                 raw_radar_coor=(115.0, 126.5125, 18.0, 29.0125),
                 tw_radar_coor=(119.5, 122.4, 21.5, 25.6),
                 tw_size=(328, 232)):

        self.raw_radar_coor = raw_radar_coor
        self.tw_radar_coor = tw_radar_coor
        self.tw_size = tw_size

    def make_cmap(self, colors, position=None, bit=False):
        bit_rgb = np.linspace(0, 1, 256)
        if position == None:
            position = np.linspace(0, 1, len(colors))
        else:
            if len(position) != len(colors):
                sys.exit("position length must be the same as colors")
            elif position[0] != 0 or position[-1] != 1:
                sys.exit("position must start with 0 and end with 1")
        if bit:
            for i in range(len(colors)):
                colors[i] = (bit_rgb[colors[i][0]],
                             bit_rgb[colors[i][1]],
                             bit_rgb[colors[i][2]])
        cdict = {'red': [], 'green': [], 'blue': []}
        for pos, color in zip(position, colors):
            cdict['red'].append((pos, color[0], color[0]))
            cdict['green'].append((pos, color[1], color[1]))
            cdict['blue'].append((pos, color[2], color[2]))

        cmap = mpl.colors.LinearSegmentedColormap("ziyu", cdict, 256)
        return cmap

    def extract_zip(self, input_zip):
        input_zip = ZipFile(input_zip)
        return {name: input_zip.read(name) for name in input_zip.namelist()}

    def crop_raw_radar_to_tw(self, raw_radar):
        start_index = (round((self.raw_radar_coor[-1] - self.tw_radar_coor[-1]) / 0.0125),
                       round((self.tw_radar_coor[0] - self.raw_radar_coor[0]) / 0.0125))
        return raw_radar[start_index[0]:start_index[0] + self.tw_size[0],
                         start_index[1]:start_index[1] + self.tw_size[1]]

    def plot_radar(self,
                   input_path,
                   output_dir="./img_results",
                   file_type="zip",
                   corp_to_taiwan_area=True,
                   show_plot=False):
        self.input_path = input_path
        if file_type == "zip":
            fpList = glob(self.input_path)
            tmp = self.extract_zip(fpList[0])[os.path.basename(
                fpList[0]).replace("zip", "json")]
            tmp_json = json.loads(tmp)

            radar_return = tmp_json["cwbopendata"]["dataset"]["contents"]["content"]
        elif file_type == "json":
            with open(self.input_path) as f:
                tmp_json = json.load(f)
                radar_return = tmp_json["cwbopendata"]["dataset"]["contents"]["content"]

        arr = np.fromstring(radar_return, float, sep=',')
        arr = arr.reshape((881, 921))
        if corp_to_taiwan_area:
            arr = self.crop_raw_radar_to_tw(arr)

        arr[arr == -999] = np.nan
        arr[arr == -99] = np.nan

        levs = 65
        levs_lin = np.linspace(0, levs, levs+1)
        cmap = self.make_cmap(cmap_NWSReflectivity())
        figsize = 10
        fig, ax = plt.subplots(figsize=(figsize, figsize))
        ax.autoscale_view('tight')
        cax = ax.imshow(arr[::-1], cmap, BoundaryNorm(levs_lin, 256))
        cbar = fig.colorbar(
            cax, ticks=[i for i in range(0, 66, 5)], shrink=0.785)
        cbar.ax.set_yticklabels([i for i in range(0, 66, 5)])
        plt.savefig(
            f'{output_dir}/{os.path.basename(fpList[0])[:-4]}.png', bbox_inches='tight')
        if show_plot:
            print("="*75+"\nCheck the nan value")
            print(tmp_json["cwbopendata"]["dataset"]
                  ["contents"]["contentDescription"])
            plt.show()


if __name__ == '__main__':
    plotter = RadarPlotter()
    plotter.plot_radar(
        input_path="./data/O-A0059-001_20210607_0000.zip",
        output_dir="./results/",
        file_type="zip",
        show_plot=False)
