import pandas as pd
import yaml


class Writer:
    def __init__(self, param):
        print(f'Initialization of {param} writer')

    def WriteData(self, outputFile):
        print('Write data from Interface class')


class YamlWriter(Writer):
    def __init__(self, data):
        super().__init__('yaml')
        self.__data = data

    def WriteData(self, outputFile):
        with open(outputFile + '.yaml', 'w') as file:
            yaml.dump(self.__data, file)


class TxtWriter(Writer):
    def __init__(self, data):
        super().__init__('txt')
        self.__data = data

    def WriteData(self, outputFile):
        with open(outputFile + '.txt', 'w') as file:
            for line in self.__data:
                file.write('[')
                s = ''
                for elem in line:
                    s += str(elem) + ' '
                s = s.strip()
                file.write(s + ']\n')


class JsonWriter(Writer):
    def __init__(self, data):
        super().__init__('json')
        self.__data = pd.DataFrame(data)

    def WriteData(self, outputFile):
        self.__data.to_json(outputFile + '.json')


class XlsxWriter(Writer):
    def __init__(self, data):
        super().__init__('xlsx')
        self.__data = pd.DataFrame(data)

    def WriteData(self, outputFile):
        self.__data.to_excel(outputFile + '.xlsx')


class CsvWriter(Writer):
    def __init__(self, data):
        super().__init__('csv')
        self.__data = pd.DataFrame(data)

    def WriteData(self, outputFile):
        self.__data.to_csv(outputFile + '.csv')


def SaveData(data, outputFile, formatFile):
    try:
        if formatFile.lower() == 'yaml':
            writer = YamlWriter(data)
        elif formatFile.lower() == 'txt':
            writer = TxtWriter(data)
        elif formatFile.lower() == 'json':
            writer = JsonWriter(data)
        elif formatFile.lower() == 'xlsx':
            writer = XlsxWriter(data)
        elif formatFile.lower() == 'csv':
            writer = CsvWriter(data)
        else:
            print('Incorrect file format')
            exit()
        writer.WriteData(outputFile)
    except Exception:
        print('Failed to save file')
        exit()
    else:
        print('File saved successfully')
