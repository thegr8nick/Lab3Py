import os


def get_next(class_name: str):
    """
       данная функция возвращает относительрный путь для объекта класса, переданного
       в функцию

       parameters

       class_name : str
         имя класса
       returns

       str
       относительный путь к объекту
    """
    path = os.path.join('dataset', class_name)
    class_names = os.listdir(path)
    class_names.append(None)
    for i in range(len(class_names)):
        if class_names[i] is not None:
            yield os.path.join(path, class_names[i])
        elif class_names[i] is None:
            yield None   

print(*get_next('rose'))