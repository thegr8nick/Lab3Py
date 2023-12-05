import os
import shutil
import csv
from typing import List
from multiprocessing import Pool


def get_full_paths2(class_name: str):
    """
        данная функция возвращает список абсолютных путей для всех изображений определенного
        класса, который будет передан в функцию, после перемещения изображений в другую директорию

        parameters

        class_name : str
          имя класса
        returns

        list
        список абсолютных путей к изображениям
    """
    full_path = os.path.abspath('dataset2')
    image_names = os.listdir(full_path)
    image_class_names = [name for name in image_names if class_name in name]
    image_full_paths = list(
        map(lambda name: os.path.join(full_path, name), image_class_names))
    return image_full_paths


def get_rel_paths2(class_name: str):
    """
        данная функция возвращает список относительных путей для всех изображений определенного класса,
        который будет передан в функцию, после перемещения изображений в другую директорию

        parameters

        class_name : str
          имя класса
        returns

        list
        список относительных путей к изображениям
    """
    rel_path = os.path.relpath('dataset2')
    image_names = os.listdir(rel_path)
    image_class_names = [name for name in image_names if class_name in name]
    image_rel_paths = list(
        map(lambda name: os.path.join(rel_path, name), image_class_names))
    return image_rel_paths


def replace_images(class_name: str):
    """
       данная функция изменяет имена изображений, объединяет номер изображения и класс в формате class_number.jpg,
       переносит изображения в директорию dataset и удаляет папку, где хранились изображения класса

       parameters

       class_name : str
         имя класса
       returns

       none
    """
    old_rel_path = os.path.relpath('dataset')
    new_rel_path = os.path.relpath('dataset2')

    class_path = os.path.join(old_rel_path, class_name)
    image_names = os.listdir(class_path)
    image_rel_paths = list(
        map(lambda name: os.path.join(class_path, name), image_names))
    new_rel_paths = list(
        map(lambda name: os.path.join(new_rel_path, f'{class_name}_{name}'), image_names))
    zip_paths = zip(image_rel_paths, new_rel_paths)
    
    with Pool(10) as p:
        p.starmap(shutil.copyfile, zip_paths)

def create_dataset2():

    class1 = 'rose'
    class2 = 'tulip'

    if os.path.isdir('dataset2'):
        shutil.rmtree('dataset2')
    
    os.mkdir('dataset2')
    '''
    old = os.path.relpath('dataset')
    new = os.path.relpath('dataset2')
    shutil.copytree(old, new)
    '''
    replace_images(class1)
    replace_images(class2)



def create_annotation2():

    class1 = 'rose'
    class2 = 'tulip'

    rose_full_paths = get_full_paths2(class1)
    rose_rel_paths = get_rel_paths2(class1)
    tulip_full_paths = get_full_paths2(class2)
    tulip_rel_paths = get_rel_paths2(class2)
    
    with open('paths2.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
        for full_path, rel_path in zip(rose_full_paths, rose_rel_paths):
            writer.writerow([full_path, rel_path, class1])
        for full_path, rel_path in zip(tulip_full_paths, tulip_rel_paths):
            writer.writerow([full_path, rel_path, class2])