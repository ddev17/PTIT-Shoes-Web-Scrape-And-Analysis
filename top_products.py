import os
import json
import numpy as np
from os.path import join

import hydra
from hydra.utils import get_original_cwd

from underthesea import word_tokenize
from underthesea.models.fast_crf_sequence_tagger import FastCRFSequenceTagger

distinct_gender = ['U', 'W', 'M']
distinct_colors = [
    'red', 'blue', 'green', 'yellow', 'black', 'white', 'purple',
    'pink', 'gray', 'orange', 'brown', 'beige', 'gold', 'silver',
    'teal', 'cyan', 'navy', 'cream', 'mauve', 'violet', 'olive',
    'aqua', 'burgundy', 'lavender', 'caramel', 'mint', 'khaki',
    'copper', 'indigo', 'xanh dương', 'đỏ', 'vàng', 'trắng',
    'đen', 'nâu', 'hồng', 'tím', 'xám', 'cam', 'xanh', 'cam', 'do', 'vang',
    'trang', 'den', 'tim', 'xanh la', 'xanh duong', 'xam', 'hong'
]

distinct_materials = [
    'Vải dệt', 'Lưới tổng hợp', 'Da tổng hợp', 'Moleskin n Cotton', 'EVA',
    'Nylon', 'Lông nhân tạo', 'Cao su', 'Vải',
    'Synthetic', 'Da', 'PVC', 'Sợi gai dầu', 'Organic Cotton',
    'Canvas', 'Suede', 'Textile', 'Da lộn',
    'Vải Knit', 'Microfiber', 'Nubuck', 'Recycled Cotton', 'TPU', 'Polyester',
    'Vải lưới', 'Tổng hợp',
]

distinct_lining = [
    'Vải dệt',
    'Lưới tổng hợp',
    'Da tổng hợp',
    'Nubuck',
    'Polyester',
    'Vải',
    'EVA',
    'Lông nhân tạo',
    'Cao su',
    'Recycled Polyester',
    'Microfiber',
    'Canvas',
    'TPU',
    'OrthoLite',
    'Nhựa Croslite',
    'Xốp mềm',
    'Sợi gai dầu',
    'Cotton',
    'Da',
    'Da lộn',
    'Tổng hợp',
    'PET',
    'Polyethylene'
]


def one_hot_encode(value_string, distinct_values):
    if value_string is None:
        return [0] * len(distinct_values)
    # Create a dictionary for easy indexing
    value_to_index = {value: idx for idx, value in enumerate(distinct_values)}

    # Initialize a one-hot vector with zeros
    one_hot_vector = [0] * len(distinct_values)

    # Split the string by '/' to get individual values
    values = value_string.split('/')

    # Set the corresponding indices to 1 for the values in the string
    for value in values:
        if value in value_to_index:
            one_hot_vector[value_to_index[value]] = 1

    return one_hot_vector


val = "red/blue/yellow"
ret = one_hot_encode(val, distinct_colors)
print(ret)

with open('processed_shoes_data.json', 'r', encoding='utf-8') as file:
    data_list = json.load(file)  # data_list is a list of objects

cnt = 0

for data in data_list:
    if data['min_size(vn_size)'] is None:
        cnt += 1

print(cnt)
input_object = {
}
output_dir_path = "postag_model"
text = "Mình đang tìm mẫu giày mẫu nam màu xanh dương chất liệu da size 42 giá 1700000"
tokens = word_tokenize(text)
tokens = [[token] for token in tokens]

model = FastCRFSequenceTagger()
model.load(output_dir_path)
y = model.predict(tokens)
for token, x in zip(tokens, y):
    if '-PR' in x:
        input_object["price"] = token.pop()
    if '-CL' in x:
        input_object["color"] = token.pop()
    if '-SZ' in x:
        input_object["size"] = token.pop()
    if '-MT' in x:
        input_object["material"] = token.pop()
    if '-GD' in x:
        input_object["gender"] = token.pop()
    print(token, "\t", x)




def square(x):
    return x * x


def cosine_distance(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length.")

    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 1  # Maximum distance if either vector is zero

    cosine_similarity = dot_product / (magnitude1 * magnitude2)

    return 1 - cosine_similarity


distances = []
for data in data_list:
    distance = 0
    # Handle None values by using a default value (e.g., 0)
    price = data['price'] if data['price'] is not None else 0
    min_size = data['min_size(vn_size)'] if data['min_size(vn_size)'] is not None else 0
    max_size = data['max_size(vn_size)'] if data['max_size(vn_size)'] is not None else 0

    if input_object['price'] is None:
        distance += square(input_object['price'] - price)
    if input_object['size'] is None:
        distance += square(input_object['size'] - min_size)
        distance += square(input_object['size'] - max_size)
    if input_object['material'] is None:
        distance += cosine_distance(
            one_hot_encode(input_object['material'], distinct_materials),
            one_hot_encode(data['material'], distinct_materials)
        )
    if input_object['gender'] is None:
        distance += cosine_distance(
            one_hot_encode(input_object['gender'], distinct_gender),
            one_hot_encode(data['gender'], distinct_gender)
        )
    # if input_object['lining'] is None:
    #     distance += cosine_distance(
    #         one_hot_encode(input_object['lining'], distinct_lining),
    #         one_hot_encode(data['lining'], distinct_lining)
    #     )
    if input_object['color'] is None:
        distance += cosine_distance(
            one_hot_encode(input_object['color'], distinct_colors),
            one_hot_encode(data['color'], distinct_colors)
        )

    distances.append(distance)

k = 3
# Sort distances and get the top k results
top_k_shoes = [x for _, x in sorted(zip(distances, data_list), key=lambda pair: pair[0])][:k]

print(top_k_shoes)