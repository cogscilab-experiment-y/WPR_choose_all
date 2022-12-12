import random
from itertools import product
from psychopy import visual


class Matrix:
    def __init__(self, n: int,
                 stimulus_dist: int,
                 stimulus_size: int,
                 stimulus_color: int = "black",
                 central_pos: [int, int] = (0, 0),
                 size: [int, int] = (3, 3),
                 group_elements: bool = False):
        assert n <= size[0] * size[1], f"You can't put {n} elements in {size[0]}x{size[1]} matrix."
        self.n = n
        self.size_y = size[0]
        self.size_x = size[1]
        self.group_elements = group_elements
        self.matrix = []
        self.stimulus_to_draw = []
        self.stimulus_list = []

        # visual parameters
        self.stimulus_dist = stimulus_dist
        self.stimulus_size = stimulus_size
        self.stimulus_color = stimulus_color
        self.central_pos = central_pos

        self.create_empty_matrix()
        self.set_elements_positions()

    def create_empty_matrix(self):
        self.matrix = [[None for _ in range(self.size_x)] for _ in range(self.size_y)]

    def set_elements_positions(self):
        matrix_all_positions = list(product(range(self.size_y), range(self.size_x)))
        if self.group_elements:
            chosen_elements = [random.choice(matrix_all_positions)]
            matrix_all_positions.remove(chosen_elements[0])
            for i in range(self.n - 1):
                new_possible_positions = []
                for elem in chosen_elements:
                    possible_y = [elem[0] - 1, elem[0], elem[0] + 1]
                    possible_x = [elem[1] - 1, elem[1], elem[1] + 1]
                    new_possible_positions += [e for e in matrix_all_positions if e[0] in possible_y and e[1] in possible_x]
                new_possible_positions = list(set(new_possible_positions))
                chosen_elements.append(random.choice(new_possible_positions))
                matrix_all_positions.remove(chosen_elements[-1])
        else:
            chosen_elements = random.sample(matrix_all_positions, self.n)
        for i, (y, x) in enumerate(chosen_elements):
            self.matrix[y][x] = i

    def find_elem_in_matrix(self, elem):
        for i, matrix_i in enumerate(self.matrix):
            for j, value in enumerate(matrix_i):
                if value == elem:
                    return i, j

    def set_stimulus_draw_parameters(self, win: visual.Window, stimulus: str, idx: int, stimulus_type: str, border_color: str, border_width: int):
        used_stimulus_types = ["text", "image"]
        assert stimulus_type in used_stimulus_types, f"Unknown stimulus_type={stimulus_type}, choose from {used_stimulus_types}"

        pos_in_matrix = self.find_elem_in_matrix(idx)
        pos_y = self.central_pos[1] + self.stimulus_dist * (pos_in_matrix[0] - self.size_y / 2. + 0.5)
        pos_x = self.central_pos[0] + self.stimulus_dist * (pos_in_matrix[1] - self.size_x / 2. + 0.5)

        if stimulus_type == "text":
            stim_to_draw = visual.TextStim(win, color=self.stimulus_color, text=stimulus, height=self.stimulus_size, pos=(pos_x, pos_y))
        elif stimulus_type == "image":
            stim_to_draw = visual.ImageStim(win, image=stimulus, size=self.stimulus_size, pos=(pos_x, pos_y))
        stim_border = visual.Rect(win, pos=(pos_x, pos_y), height=self.stimulus_size, width=self.stimulus_size,
                                  lineColor=border_color, lineWidth=border_width, fillColor=None)
        return {"pos": pos_in_matrix, "stim_to_draw": stim_to_draw, "stimulus": stimulus, "stim_border": stim_border}

    def prepare_to_draw(self, win: visual.Window, stimulus_list: list, stimulus_type: str, border_color: str, border_width: int):
        assert len(stimulus_list) == self.n, f"len(stimulus_list) have to be equal n. Now n={self.n} and len(stimulus_list={len(stimulus_list)}"
        self.stimulus_list = stimulus_list
        for idx, stimulus in enumerate(stimulus_list):
            stim_to_draw = self.set_stimulus_draw_parameters(stimulus=stimulus, idx=idx, stimulus_type=stimulus_type, win=win,
                                                             border_color=border_color, border_width=border_width)
            self.stimulus_to_draw.append(stim_to_draw)

    def replace_stimulus(self, win: visual.Window, new_stimulus: str, stimulus_type: str):
        elem_to_replace = random.choice(range(self.n))
        stimulus_to_replace = self.set_stimulus_draw_parameters(stimulus=new_stimulus, idx=elem_to_replace, stimulus_type=stimulus_type, win=win)
        self.stimulus_to_draw[elem_to_replace] = stimulus_to_replace

    def draw(self):
        for elem in self.stimulus_to_draw:
            elem["stim_to_draw"].draw()

    def setAutoDraw(self, flag: bool):
        for elem in self.stimulus_to_draw:
            elem["stim_to_draw"].setAutoDraw(flag)
            if not flag:
                elem["stim_border"].setAutoDraw(flag)
