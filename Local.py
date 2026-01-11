from pathlib import Path
import os
class Local:
    def __init__(self, path):
        self.path = path
    def __getattribute__(self, name):
        atr = super().__getattribute__(name)
        if name not in ["__init__","__getattribute__","write","append"] and callable(atr):
            def new_func(*args, **kwargs):
                print("Local ;",name)
                for i in args:
                    Path(i).mkdir(parents=True, exist_ok=True)
                for i in kwargs.values():
                    Path(i).mkdir(parents=True, exist_ok=True)
                return atr(*args, **kwargs)
            return new_func
        elif name not in ["__init__","__getattribute__"] and callable(atr):
            def new_func(*args, **kwargs):
                print("Local ; calling :",name)
                return atr(*args, **kwargs)
            return new_func
        return atr
    def list(self):
        return os.listdir(self.path)
    def read(self, filename):
        with open(f"{self.path}/{filename}", "r") as file:
            return file.read()
    def write(self, filename, content):
        with open(f"{self.path}/{filename}", "w") as file:
            file.write(content)
    def new_folder(self, folder_name):
        os.makedirs(f"{self.path}/{folder_name}", exist_ok=True)
    def delete(self, folder_name):
        os.rmdir(f"{self.path}/{folder_name}")
    def delete(self, filename):
        os.remove(f"{self.path}/{filename}")
    def move(self, old_name, new_name):
        os.rename(f"{self.path}/{old_name}", f"{self.path}/{new_name}")
    def copy(self, source_name, dest_name):
        import shutil
        shutil.copy(f"{self.path}/{source_name}", f"{self.path}/{dest_name}")
    def exists(self, name):
        return os.path.exists(f"{self.path}/{name}")
    def size(self, filename):
        return os.path.getsize(f"{self.path}/{filename}")
    def modified_time(self, filename):
        return os.path.getmtime(f"{self.path}/{filename}")
    def created_time(self, filename):
        return os.path.getctime(f"{self.path}/{filename}")
    def append(self, filename, content):
        with open(f"{self.path}/{filename}", "a") as file:
            file.write(content)
    def rename(self, old_name, new_name):
        os.rename(f"{self.path}/{old_name}", f"{self.path}/{new_name}")
    def clear(self, filename):
        with open(f"{self.path}/{filename}", "w") as file:
            file.truncate(0)
    def move_to(self, filename, new_path):
        import shutil
        shutil.move(f"{self.path}/{filename}", f"{new_path}/{filename}")
    def paste(self, filename, new_path):
        import shutil
        shutil.copy(f"{self.path}/{filename}", f"{new_path}/{filename}")
open("gg/t.py","wb")