from pathlib import Path
import time

from sympy.physics.units import current


class DataLoader:
    def __init__(self, directory_files_path = 'C:/podcasts'):
        self.directory_files_path = Path(directory_files_path)

    def meta_data(self):
        all_files = []
        for file in self.directory_files_path.iterdir():

            current_file = {'file_path': f'{self.directory_files_path}/{file.name}'}
            file_path = file.name
            meta_data = {}
            meta_data['name'] = file.name
            meta_data['size'] = file.stat().st_size
            meta_data['date_time'] = time.ctime(file.stat().st_mtime)
            current_file['meta_data'] = meta_data
            all_files.append(current_file)

        print(all_files)

if __name__ == '__main__':
    l = DataLoader()
    l.meta_data()