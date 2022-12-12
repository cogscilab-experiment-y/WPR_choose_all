from lxml import etree
from os import listdir
from os.path import join

width = "250.0pt"
height = "250.0pt"
stroke_color = "black"
colors = ["#FF3300", "#00B050", "#33CCFF", "#FFFF99", "#FF00FF",
          "#FF6161", "#66FF33", "#0070C0", "#FFC000", "#7030A0",
          "#800000", "#336600", "#0033CC", "#996633", "#666699",
          "#FFC4C4", "#A8D08C", "#9CC2E5", "#FEE599", "#FF6699",
          "#CC3402", "#00FF99", "#DDEAF6", "#FF9933", "#CC66FF"]
stroke_width = "5"
color_names = dict(white="white", ghostwhite="white", lightgrey="gray", dimgrey='slate')

all_possible_options = [color for color in colors]
filenames = listdir('figures_svg')
print filenames
for filename in filenames:
    tree = etree.parse(open(join('figures_svg', filename), 'r'))
    for color_idx, color in enumerate(colors):
        for element in tree.iter():
            curr_tag = element.tag.split("}")[1]
            if curr_tag == "svg":
                element.set("width", width)
                element.set("height", height)
            elif curr_tag == "g":
                element.set("fill", color)
                element.set("stroke", stroke_color)
                element.set("stroke-width", stroke_width)

        res_file_name = filename.split('.')[0] + "_" + str(color_idx + 1) + ".svg"
        with open(join('all_svg', res_file_name), 'w') as res_file:
            res_file.write(etree.tostring(tree, pretty_print=True))
