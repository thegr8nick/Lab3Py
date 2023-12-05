import os
import csv
from typing import List


def get_full_paths(class_name: str) -> List[str]:
    """
        возвращает список путей для всех изображений определенного класса, который будет передан в функцию

        parameters

        class_name : str
            имя класса
        returns

        list
        спиок путей к изображениям определенного класса
    """
    full_path = os.path.abspath('dataset')
    class_path = os.path.join(full_path, class_name)
    image_names = os.listdir(class_path)
    image_full_paths = list(
        map(lambda name: os.path.join(class_path, name), image_names))
    return image_full_paths


def get_rel_paths(class_name: str) -> List[str]:
    """
       возвраает список относительных путей относительно файла dataset для
       всех изображений определенного класса, который будет передан в функцию

       parameters

       class_name : str
         имя класса
       returns

       list
       cписок относительных путей к изображениям
    """
    rel_path = os.path.relpath('dataset')
    class_path = os.path.join(rel_path, class_name)
    image_names = os.listdir(class_path)
    image_rel_paths = list(
        map(lambda name: os.path.join(class_path, name), image_names))
    return image_rel_paths


def create_annotation():

    class1 = 'rose'
    class2 = 'tulip'

    rose_full_paths = get_full_paths(class1)
    rose_rel_paths = get_rel_paths(class1)
    tulip_full_paths = get_full_paths(class2)
    tulip_rel_paths = get_rel_paths(class2)

    with open('paths.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
        for full_path, rel_path in zip(rose_full_paths, rose_rel_paths):
            writer.writerow([full_path, rel_path, class1])
        for full_path, rel_path in zip(tulip_full_paths, tulip_rel_paths):
            writer.writerow([full_path, rel_path, class2])
