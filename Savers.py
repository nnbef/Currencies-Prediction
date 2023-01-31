import yaml
import json
import xlsxwriter
import csv


class IWriter:
    def __init__(self, param):
        print(f'Initialization of {param} writer')

    def write_data(self, output_file):
        print(f'Write data to {output_file} file')


class YamlWriter(IWriter):
    def __init__(self, data):
        super().__init__('yaml')
        self.__data = data

    def write_data(self, output_file):
        super().write_data(output_file + '.yaml')
        data = []
        for line in self.__data:
            data.append(line.get_data())
        with open(output_file + '.yaml', 'w') as file:
            yaml.dump(data, file)


class TxtWriter(IWriter):
    def __init__(self, data):
        super().__init__('txt')
        self.__data = data

    def write_data(self, output_file):
        super().write_data(output_file + '.txt')
        with open(output_file + '.txt', 'w') as file:
            for line in self.__data:
                file.write('[' + ', '.join(map(str, line.get_data())) + ']\n')


class JsonWriter(IWriter):
    def __init__(self, data):
        super().__init__('json')
        self.__data = data

    def write_data(self, output_file):
        super().write_data(output_file + '.json')
        data = []
        for i in range(len(self.__data)):
            x = self.__data[i].get_data()
            date = x[0].isoformat().split('-')
            date.reverse()
            x[0] = '.'.join(date)
            data.append(json.dumps({i: x}))
        data = ', '.join(data)
        with open(output_file + '.json', 'w') as file:
            file.write(data)


class XlsxWriter(IWriter):
    def __init__(self, data):
        super().__init__('xlsx')
        self.__data = data

    def write_data(self, output_file):
        super().write_data(output_file + '.xlsx')
        data = []
        for i in range(len(self.__data)):
            x = self.__data[i].get_data()
            date = x[0].isoformat().split('-')
            date.reverse()
            x[0] = '.'.join(date)
            data.append(x)
        workbook = xlsxwriter.Workbook(output_file + '.xlsx')
        worksheet = workbook.add_worksheet()
        for i in range(len(self.__data)):
            worksheet.write_row(i, 0, data[i])
        workbook.close()


class CsvWriter(IWriter):
    def __init__(self, data):
        super().__init__('csv')
        self.__data = data

    def write_data(self, output_file):
        super().write_data(output_file + '.csv')
        data = []
        for i in range(len(self.__data)):
            x = self.__data[i].get_data()
            date = x[0].isoformat().split('-')
            date.reverse()
            x[0] = '.'.join(date)
            data.append(x)
        with open(output_file + '.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(data)


def save_data(data, output_file, format_file):
    try:
        if format_file.lower() == 'yaml':
            writer = YamlWriter(data)
        elif format_file.lower() == 'txt':
            writer = TxtWriter(data)
        elif format_file.lower() == 'json':
            writer = JsonWriter(data)
        elif format_file.lower() == 'xlsx':
            writer = XlsxWriter(data)
        elif format_file.lower() == 'csv':
            writer = CsvWriter(data)
        else:
            print('Incorrect file format')
            exit()
        writer.write_data(output_file)
    except Exception:
        print('Failed to save file')
        exit()
    else:
        print('File saved successfully')
