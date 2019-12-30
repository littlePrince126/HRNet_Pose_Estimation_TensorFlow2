import json
from pathlib import Path
import time
from configuration.base_config import Config


# keypoints: ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder',
#             'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee',
#             'right_knee', 'left_ankle', 'right_ankle']
# skeleton: [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7], [6, 8], [7, 9], [8, 10],
#            [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]
class COCO_keypoints(object):
    def __init__(self):
        self.annotation = Config.COCO_ROOT_DIR + "annotations/"
        self.train_annotation = Path(self.annotation + "person_keypoints_train2017.json")
        self.valid_annotation = Path(self.annotation + "person_keypoints_val2017.json")
        start_time = time.time()
        self.train_dict = self.__load_json(self.train_annotation)
        self.valid_dict = self.__load_json(self.valid_annotation)
        print("It took {:.2f} seconds to load the json files.".format(time.time() - start_time))
        self.__print_coco_keypoints()

    def __print_coco_keypoints(self):
        keypoints = self.train_dict["categories"][0]["keypoints"]
        skeleton = self.train_dict["categories"][0]["skeleton"]
        print("coco keypoints: {}".format(keypoints))
        print("coco skeleton: {}".format(skeleton))

    def __load_json(self, json_file):
        print("Start loading {}...".format(json_file.name))
        with json_file.open(mode='r') as f:
            load_dict = json.load(f)
        print("Loading is complete!")
        return load_dict

    def __get_image_information(self, data_dict):
        images = data_dict["images"]
        image_file_list = []
        image_id_list = []
        image_height_list = []
        image_width_list = []
        for image in images:
            image_file_list.append(image["file_name"])
            image_id_list.append(image["id"])
            image_height_list.append(image["height"])
            image_width_list.append(image["width"])
        return image_file_list, image_id_list, image_height_list, image_width_list

    def __get_keypoints_information(self, data_dict):
        annotations = data_dict["annotations"]
        keypoints_list = []
        image_id_list = []
        bbox_list = []
        for annotation in annotations:
            keypoints_list.append(annotation["keypoints"])
            image_id_list.append(annotation["image_id"])
            bbox_list.append(annotation["bbox"])
        return keypoints_list, image_id_list, bbox_list

    # def __parse_keypoints(self, keypoints):
    #     n_keypoints = len(keypoints) / 3
    #     x_list = []
    #     y_list = []
    #     v_list = []
    #     for i in range(int(n_keypoints)):
    #         x = keypoints[i*3]
    #         y = keypoints[i*3+1]
    #         v = keypoints[i*3+2]
    #         if v > 0:
    #             x_list.append(x)
    #             y_list.append(y)
    #             v_list.append(v)
    #     return x_list, y_list, v_list

    def __creat_dict_from_list(self, list_data):
        created_dict = {}
        for i in range(len(list_data)):
            created_dict[list_data[i]] = i
        return created_dict

    def __list_to_str(self, list_data):
        str_result = ""
        for i in list_data:
            str_result += str(i)
            str_result += " "
        return str_result.strip()

    # One line of txt: xxx.jpg height width xmin ymin w h x1 y1 v1 x2 y2 v2 ... x17 y17 v17
    # xxx.jpg：The name of the picture to which the keypoints of the human body belong.
    # height: The height of the picture.
    # width: The width of the picture.
    # xmin: The x coordinate of the upper-left corner of the bounding box.
    # ymin: The y coordinate of the upper-left corner of the bounding box.
    # w: The width of the bounding box.
    # h: The height of the bounding box.
    # xi (i = 1,...,17): The x coordinate of the keypoint.
    # yi (i = 1,...,17): The y coordinate of the keypoint.
    # vi (i = 1,...,17): When vi is 0, it means that this key point is not marked,
    # when vi is 1, it means that this key point is marked but not visible,
    # when vi is 2, it means that this key point is marked and also visible.
    def write_information_to_txt(self, dataset):
        if dataset == "train":
            data_dict = self.train_dict
            txt_file = Config.COCO_TRAIN_TXT
        elif dataset == "valid":
            data_dict = self.valid_dict
            txt_file = Config.COCO_VALID_TXT
        else:
            raise ValueError("Invaid dataset name!")
        image_files, image_ids, image_heights, image_widths = self.__get_image_information(data_dict)
        keypoints_list, image_ids_from_keypoints, bboxes= self.__get_keypoints_information(data_dict)
        image_id_dict = self.__creat_dict_from_list(image_ids)
        with open(file=txt_file, mode="a+") as f:
            for i in range(len(image_ids_from_keypoints)):
                one_human_instance_info = ""
                image_index = image_id_dict[image_ids_from_keypoints[i]]
                one_human_instance_info += image_files[image_index] + " "
                one_human_instance_info += str(image_heights[image_index]) + " "
                one_human_instance_info += str(image_widths[image_index]) + " "
                one_human_instance_info += self.__list_to_str(bboxes[i]) + " "
                one_human_instance_info += self.__list_to_str(keypoints_list[i])
                one_human_instance_info = one_human_instance_info.strip()
                one_human_instance_info += "\n"
                print("Writing information of image-{} to {}".format(image_files[image_index], txt_file))
                f.write(one_human_instance_info)





