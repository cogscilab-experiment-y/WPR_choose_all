from os.path import join
from psychopy import visual

from code.matrix import Matrix


class Trial:
    def __init__(self, win: visual.Window, config: dict, n: int, size: [int, int] = (3, 3), group_elements: bool = False):
        self.matrix_1 = Matrix(n=n,
                               size=size,
                               group_elements=group_elements,
                               stimulus_dist=config["stimulus_dist"],
                               stimulus_size=config["stimulus_size"],
                               stimulus_color=config["stimulus_color"],
                               central_pos=config["stimulus_central_pos"])

        mask_size_x = (size[1] - 1) * config["stimulus_dist"] + config["stimulus_size"] + config["extra_mask_size"]
        mask_size_y = (size[0] - 1) * config["stimulus_dist"] + config["stimulus_size"] + config["extra_mask_size"]
        self.mask = visual.ImageStim(win, image=join('images', 'mask.png'), interpolate=True,
                                     size=(mask_size_x, mask_size_y), pos=config['mask_pos'])

        self.matrix_2 = Matrix(n=size[0]*size[1],
                               size=size,
                               group_elements=group_elements,
                               stimulus_dist=config["stimulus_dist"],
                               stimulus_size=config["stimulus_size"],
                               stimulus_color=config["stimulus_color"],
                               central_pos=config["stimulus_central_pos"])
