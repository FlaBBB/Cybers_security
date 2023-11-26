import os, random, win32api, win32file, time

class PathTree:
    def __init__(self, name, parent=None) -> None:
        self.childern = dict()
        self.name = name
        self.parent = parent
    
    def add_child(self, child_name: str) -> None:
        self.childern[child_name] = PathTree(child_name, self)
    
    def get_child(self, name: str) -> "PathTree":
        return self.childern[name]
    
    def get_list_dir_not_in_tree(self) -> list:
        try:
            listed_dir = os.listdir(self.get_path())
        except (PermissionError, FileNotFoundError):
            return []
        return list(set(listed_dir) - set(self.childern.keys()))
    
    def get_path(self) -> str:
        node = self # type: PathTree
        path = node.name
        while node.parent != None:
            node = node.parent
            path = node.name + "\\" + path
        return path.replace("\\\\", "\\")

def get_local_drives():
    """Returns a list containing letters from local drives"""
    drive_list = win32api.GetLogicalDriveStrings()
    drive_list = drive_list.split("\x00")[0:-1]  # the last element is ""
    list_local_drives = []
    for letter in drive_list:
        if win32file.GetDriveType(letter) == win32file.DRIVE_FIXED:
            list_local_drives.append(letter)
    return list_local_drives 

def get_random_path_file():
    node = PathTree(random.choice(get_local_drives())) # type: PathTree
    while True:
        try:
            if len(node.get_list_dir_not_in_tree()) == 0:
                node = node.parent
                continue
            last_path = random.choice(node.get_list_dir_not_in_tree())
        except:
            node = node.parent
            continue
        node.add_child(last_path)
        node = node.get_child(last_path)
        if os.path.isdir(node.get_path()):
            continue
        break
    return node.get_path()

from globfuscator import globfuscator

longest_path_to_process = ""
longest_time = 0
sstart_time = time.time()
n_times = 1000
for i in range(n_times):
    while True:
        try:
            path = get_random_path_file()
            print(f"#[{i+1}]" + "\npath =", path)
            break
        except:
            continue

    start_time = time.time()
    result, score = globfuscator.globfuscator(path)
    long_process = time.time() - start_time
    if long_process > longest_time:
        longest_time = long_process
        longest_path_to_process = path

    print(f"result = {result} ({score[0]} - {score[1]}%) - {long_process}s")

print("#== Statistics ==")
print(f"longest_path_to_process = {longest_path_to_process}")
print(f"longest_time = {longest_time}s")
print(f"total_time = {time.time() - sstart_time}s")
print(f"average_time = {(time.time() - sstart_time) / n_times}s")