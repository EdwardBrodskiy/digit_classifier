from typing import Tuple

import numpy as np

from data_managers.sampling_methods import sample_from_stream, balanced_serializer, Sampler, SerialData, Serializer, DataSampleStream, \
    FullData


class DataHandler:
    def __init__(self, file_path_labels, file_path_imgs, groups=1000, method: Sampler = sample_from_stream,
                 serializer: Serializer = balanced_serializer, amount=1):
        self._sampling_method: Sampler = method
        self._serializer: Serializer = serializer

        self.file_path_imgs: str = file_path_imgs
        self.file_path_labels: str = file_path_labels
        self._groups: int = groups
        self._amount: int = amount
        self._is_data_loaded: bool = False
        self.data: FullData = {i: [] for i in range(10)}

    @property
    def sampling_method(self):
        return self._sampling_method

    @sampling_method.setter
    def sampling_method(self, value: Sampler):
        self.sampling_method = value

    @property
    def serializer(self):
        return self._sampling_method

    @serializer.setter
    def serializer(self, value: Serializer):
        self._serializer = value

    @property
    def groups(self) -> int:
        return self._groups

    @groups.setter
    def groups(self, value: int):
        if 0 < value:
            self._groups = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if self._amount > 0:
            self._amount = value

    def get_epoch(self, *method_args, **method_kwargs) -> DataSampleStream:
        # TODO: fix is perceived by pycharm as the output not the function it self
        is_sampling_method_serial = SerialData in self._sampling_method.__annotations__.values()
        if self._is_data_loaded:
            if is_sampling_method_serial:
                return self._sampling_method(self._serializer(self.data), self._groups, *method_args, **method_kwargs)
            else:
                return self._sampling_method(self.data, self._groups, *method_args, **method_kwargs)
        else:
            if is_sampling_method_serial:
                return self._sampling_method(self._tap_into_loading_data(self.get_from_file_iter()), self._groups, *method_args,
                                             **method_kwargs)
            else:
                self.load_data()
                return self.get_epoch(*method_args, **method_kwargs)

    def get_all_data(self) -> SerialData:
        if self._is_data_loaded:
            return self._serializer(self.data)
        else:
            return self._tap_into_loading_data(self.get_from_file_iter())

    def load_data(self):
        for label, value in self.get_from_file_iter():
            self.data[label].append(value)
        self._is_data_loaded = True

    def _tap_into_loading_data(self, stream_iter: SerialData) -> SerialData:
        for label, value in stream_iter:
            self.data[label].append(value)
            yield label, value
        self._is_data_loaded = True

    def get_from_file_iter(self) -> SerialData:
        with open(self.file_path_imgs, "rb") as imgs:
            with open(self.file_path_labels, "rb") as labels:
                number_of_elements, img_resolution = self.get_meta_data(labels, imgs)
                elements_per_img = img_resolution[0] * img_resolution[1]

                for i in range(int(round(number_of_elements * self._amount, 0))):
                    label: int = int.from_bytes(labels.read(1), byteorder='big')
                    image = []
                    for j in range(elements_per_img):
                        image.append([int.from_bytes(imgs.read(1), byteorder='big') / 255])  # TODO: may be wrong

                    yield label, np.array(image, dtype='float32')

    @staticmethod
    def get_meta_data(labels, imgs) -> Tuple[int, Tuple[int, int]]:
        DataHandler.check_magic_numbers(labels, imgs)

        number_of_elements = DataHandler.check_number_of_elements(labels, imgs)
        img_resolution = DataHandler.get_resolution(imgs)

        return number_of_elements, img_resolution

    @staticmethod
    def check_magic_numbers(labels, imgs):
        imgs_magic_num = int.from_bytes(imgs.read(4), byteorder="big")
        if imgs_magic_num != 2051:
            print("Not the correct file given for the images")
        labels_magic_num = int.from_bytes(labels.read(4), byteorder="big")
        if labels_magic_num != 2049:
            print("Not the correct file given for the labels")

    @staticmethod
    def check_number_of_elements(labels, imgs) -> int:
        num_of_imgs = int.from_bytes(imgs.read(4), byteorder='big')
        num_of_labels = int.from_bytes(labels.read(4), byteorder='big')
        if num_of_imgs != num_of_labels:
            print("Label size doesn't match Image size")
        return min(num_of_labels, num_of_imgs)

    @staticmethod
    def get_resolution(imgs) -> Tuple[int, int]:
        rows = int.from_bytes(imgs.read(4), byteorder='big')
        columns = int.from_bytes(imgs.read(4), byteorder='big')
        return rows, columns