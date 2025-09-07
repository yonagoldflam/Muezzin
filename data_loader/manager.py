
from data_loader import DataLoader


class Manager:
    def __init__(self):
        self.directory_files_path = 'C:/podcasts'
        self.data_loader = DataLoader(self.directory_files_path)

    def get_meta_data(self):
        return self.data_loader.meta_data()


if __name__ == '__main__':
    m = Manager()
    print(m.get_meta_data())
