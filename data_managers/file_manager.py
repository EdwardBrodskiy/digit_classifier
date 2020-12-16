import os
import pickle


class FileManager:
    def __init__(self, files_dir="files", default_file_name="default.🥒"):
        self.__current_file_name = default_file_name
        self.bound = []

        if not os.path.exists(files_dir):
            os.makedirs(files_dir)

        save_files_location = os.path.join(os.getcwd(), files_dir)
        os.chdir(save_files_location)

        self._loaded_object = None
        self.load(self.__current_file_name)

    @property
    def current_file_name(self):
        return self.__current_file_name

    @property
    def loaded_object(self):
        return self._loaded_object

    @loaded_object.setter
    def loaded_object(self, value):
        self._loaded_object = value
        self._call_binds()

    def load(self, file_name):
        with open(file_name, 'rb') as file:
            self.loaded_object = pickle.load(file)
            self.__current_file_name = file_name
        self._call_binds()

    def save(self):
        with open(self.__current_file_name, 'wb') as file:
            pickle.dump(self.loaded_object, file)

    def save_as(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.loaded_object, file)
            self.__current_file_name = file_name
        self._call_binds()

    def bind(self, func):
        self.bound.append(func)

    def _call_binds(self):
        for func in self.bound:
            func()

    @staticmethod
    def show_all():
        return os.listdir()
