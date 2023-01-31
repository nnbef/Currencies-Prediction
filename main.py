import sys
from Parsers import arg_parser, parse
from Savers import save_data
from Model import LSTMmodel
from DataLoaderPreparer import DataLoader, DataPreparer
import tensorflow as tf
import numpy as np

if __name__ == '__main__':
    print('Application started with arguments:',
          str(sys.argv[1:]).replace('[', '').replace(']', '').replace("'", ''))
    arg_parser = arg_parser()
    arguments = arg_parser.parse_args(sys.argv[1:])

    if arguments.useFile == 'True':
        dl = DataLoader(arguments.fileName + '.' + arguments.format)
        data = dl.get_data()
    else:
        # need changes
        data = parse(arguments.startDate, arguments.currency)
        # need changes


    data_preparer = DataPreparer(data, float(arguments.split))
    data_train, labels_train, data_test, labels_test = data_preparer.get_prepared_data(30, 1)

    model = LSTMmodel()
    model.build()
    model.train(data_train, labels_train, 2, 8)
    predicted_data = model.predict(data_test)
    #print(type(predicted_data))
    print(np.average(np.abs(predicted_data - labels_test)))
    # save_data(data, arguments.fileName, arguments.format)
