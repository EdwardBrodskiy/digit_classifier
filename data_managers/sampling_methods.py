from typing import Tuple, Any, Callable, Dict, List, Union, Iterator

FullData = Dict[int, List[Any]]

SerialData = Iterator[Tuple[int, Any]]

Serializer = Callable[[FullData], SerialData]

CommonArgs = [int, Tuple[Any], Dict[str, Any]]

DataSampleStream = Iterator[FullData]

SerialSampler = Callable[[SerialData, int, Tuple[Any], Dict[str, Any]], DataSampleStream]

FullDataSampler = Callable[[FullData, int, Tuple[Any], Dict[str, Any]], DataSampleStream]

Sampler = Union[SerialSampler, FullDataSampler]


def balanced_serializer(data: FullData) -> SerialData:
    counters = {label: 0 for label in data}
    data_left = True
    while data_left:
        data_left = False
        for label in data:
            if counters[label] < len(data[label]):
                yield label, data[label][counters[label]]
                counters[label] += 1
                data_left = True


def sample_from_stream(data_stream: SerialData, sample_size: int) -> DataSampleStream:
    data_sample = {i: [] for i in range(10)}
    sample_counter = 0
    for label, value in data_stream:
        data_sample[label].append(value)
        sample_counter += 1
        if sample_counter == sample_size:
            yield data_sample
            data_sample = {i: [] for i in range(10)}
            sample_counter = 0


def sample_saturate_data(data: FullData, distribution: List[float], sample_size: int = 100) -> DataSampleStream:
    pass
