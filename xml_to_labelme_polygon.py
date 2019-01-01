import glob
import os
import xml.etree.ElementTree as ET

from labelme.label_file import LabelFile


def get_text(ele, tag):
    for c in ele:
        if c.tag == tag:
            return c.text


def convert(f):
    tree = ET.parse(f)
    root = tree.getroot()

    filename = None

    shapes = []
    for c in root:
        if c.tag == 'filename':
            filename = c.text

        if c.tag == 'object':
            label = None
            for o in c:
                if o.tag == 'name':
                    label = o.text
                if o.tag == 'bndbox':
                    xmin = int(get_text(o, 'xmin'))
                    xmax = int(get_text(o, 'xmax'))
                    ymin = int(get_text(o, 'ymin'))
                    ymax = int(get_text(o, 'ymax'))

            shapes.append(
                dict(
                    label=label,
                    points=[[xmin, ymin], [xmax, ymin], [xmax, ymax],
                            [xmin, ymax]],
                    shape_type='polygon',
                    line_color=None,
                    fill_color=None,
                ))
    label_file = LabelFile()
    label_file.save(
        f.replace('.xml', '.json'),
        shapes=shapes,
        imagePath=filename,
        lineColor=[0, 255, 0, 128],
        fillColor=[255, 0, 0, 128],
        flags={})


def main():
    paths = glob.glob('data/*/*.xml')

    for path in paths:
        convert(path)


if __name__ == "__main__":
    main()
