import pandas as pd
import numpy as np
from random import shuffle


class DataLoader:
    def __init__(self, file_name: str):
        class FileReader:
            def __init__(self, reader_file_name):
                self.__file_name = '.'.join(reader_file_name.split('.')[:len(reader_file_name.split('.')) - 1])
                self.__format = reader_file_name.split('.')[-1]

            def read_data(self):
                if self.__format == 'csv':
                    df = pd.read_csv(self.__file_name + '.' + self.__format, sep=';', names=['date', 'count', 'curs'])
                elif self.__format == 'json':
                    pass
                elif self.__format == 'xlsx':
                    pass
                elif self.__format == 'txt':
                    pass
                elif self.__format == 'yaml':
                    pass
                else:
                    exit()
                df.curs = df['curs'] / df['count']
                return df.curs.to_numpy()

        fr = FileReader(file_name)
        self.__data = fr.read_data()

    def get_data(self):
        return self.__data


class DataPreparer:
    def __init__(self, data, split):
        self.__data = data
        self.__split = split
        self.__len_split = int(len(self.__data) * self.__split)

    def get_prepared_data(self, data_size, label_size):
        def do_arrays(start_index):
            def_data = []
            def_labels = []

            for i in range(start_index, start_index + data_size):
                def_data.append(self.__data[i])
            for i in range(start_index + data_size, start_index + data_size + label_size):
                def_labels.append(self.__data[i])

            return np.array(def_data), np.array(def_labels)

        array = []
        labels = []

        for index in range(len(self.__data) - data_size - label_size):
            temp_data, temp_labels = do_arrays(index)
            array.append(temp_data)
            labels.append(temp_labels)

        pairs = list(zip(array, labels))
        shuffle(pairs)

        # returns data_train, labels_train, data_test, labels_test
        return np.array([x[0] for x in pairs[:self.__len_split]]), \
            np.array([x[1] for x in pairs[:self.__len_split]]), \
            np.array([x[0] for x in pairs[self.__len_split:]]), \
            np.array([x[1] for x in pairs[self.__len_split:]])

        #return np.array(pairs[:self.__len_split][0]), np.array(pairs[:self.__len_split][1]), \
        #    np.array(pairs[self.__len_split:][0]), np.array(pairs[self.__len_split:][1])

        #return np.array(array[:self.__len_split]), np.array(labels[:self.__len_split]), \
        #    np.array(array[self.__len_split:]), np.array(labels[self.__len_split:])
