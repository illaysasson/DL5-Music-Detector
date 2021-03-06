import json
import shutil
import cv2

# Opens the data file with json
def open_data(path):
    with open(path) as f:
        return json.load(f)

# Returns a list of string numbers as a list of ints
def string_to_int_array(array):
    desired_array = [int(numeric_string) for numeric_string in array]
    return desired_array

# Returns a list of every category in the dataset
def classes_list(d):
    categories = d['categories']
    keys = categories.keys()
    int_keys = string_to_int_array(keys)
    classes = ["None"]
    for i in range(0, max(int_keys)):
        if i in int_keys:
            if categories[str(i)]['annotation_set'] == "deepscores":
                class_name = categories[str(i)]['name']
                classes.append(class_name)
    return classes

# Formats the yolo bbox correctly
def yolo_format_bbox(bbox, img_width, img_height):
    # x y width height (relative to image)
    int_bbox = [int(x) for x in bbox]

    x = (int_bbox[0] + int_bbox[2]) // 2
    y = (int_bbox[1] + int_bbox[3]) // 2
    width = int_bbox[2] - int_bbox[0]
    height = int_bbox[3] - int_bbox[1]

    # new_bbox = [x, y, width, height]

    # Turn into relative to image
    r_x = round(x / img_width, 6)
    r_y = round(y / img_height, 6)
    r_width = round(width / img_width, 6)
    r_height = round(height / img_height, 6)
    relative_bbox = [r_x, r_y, r_width, r_height]
    if min(relative_bbox) <= 0 or max(relative_bbox) >= 1:
        print('Error - Wrong annotation.')
    return relative_bbox

# Writes a new dataset given a list of specific annotations to include
def write_specific_annotations_to_txt(d, cat_list, folder):
    images = d['images']
    # Adds everything into a txt file array
    for img in images:
        file_name = img["filename"]
        index = 0
        txt_file = []
        txt_line = ""
        for cat in cat_list:
            for ann_id in img["ann_ids"]:
                cat_id = d['annotations'][ann_id]['cat_id'][0]
                if cat_id == str(cat):
                    img_height, img_width = cv2.imread(
                        'DeepScoresV2/images/' + file_name).shape
                    bbox = yolo_format_bbox(
                        d['annotations'][ann_id]['a_bbox'], img_width, img_height)
                    txt_line += str(index) + " "
                    txt_line += str(bbox).strip(
                        '[').strip(']').replace(",", '')
                    txt_file.append(txt_line)
                    txt_line = ""
            index += 1

        # Copies the file and image to folder:
        if not txt_file:  # If a list is empty
            continue
        shutil.copy('DeepScoresV2/images/' + file_name, folder)
        with open(folder + "/" + file_name[:-4] + ".txt", 'w') as f:
            for line in txt_file:
                f.write(line)
                f.write('\n')

data = open_data('DeepScoresV2/deepscores_train.json')
all_classes = classes_list(data)
wanted_class = ["staff", "noteheadBlackOnLine", "noteheadBlackInSpace", "noteheadHalfOnLine", "noteheadHalfInSpace", "noteheadWholeOnLine", "noteheadWholeInSpace"]
classes_index = [all_classes.index(x) for x in wanted_class]
write_specific_annotations_to_txt(data, classes_index, 'darknet/obj')
print('Finished!')
