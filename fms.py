import json
import threading


# note that i am creating a virtual file management system
block_size = 4
invalidChars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
address = ""

# create a list which stores previuos directories path
dir_hist = []
cur_dict = {}

mmap = {}

storage = []


# create a file and store it in dir_dict

def create_file(name, data):
    global mmap
    global dir_hist
    global cur_dict
    global address
    global mmap
    global storage
    

    # open storage and store in storage array
    storage = open_storage()

    # open mmap and store in mmap array
    mmap = open_mmap()

    # open dir_hist and store in dir_hist array
    dir_hist = open_dir_hist()

    size = len(data)
    if size % block_size == 0:
        blocks = size//block_size
    else:
        blocks = size//block_size+1

    if name in cur_dict:
        print("File already exists")
    # check if name is valid
    elif any(char in invalidChars for char in name):
        print("Invalid name")
    else:
        # check if there is enough space in storage
        print(len(storage))
        print(size)
        if len(storage) > size:
            address = ''
            for i in range(0, size):
                add = storage.pop(i)
                address += str(add)+"."

            if (dir_hist != []):
                c_dir = dir_hist[-1]
                print(c_dir)
                for i in mmap.keys():
                    if i == c_dir:
                        mmap[i][name+".txt"] = {'data': data,
                                                'address': address, 'size': size, 'blocks': blocks}
                print(name," File created")
                # update mmap
                save_mmap()
            else:
                mmap[name+".txt"] = {'data': data,
                                     'address': address, 'size': size, 'blocks': blocks}
                print("File created")
                # update mmap
                save_mmap()
            for i in range(0, size):
                add = storage.pop(i)
                address += str(add)+"."

        else:
            print("No space in storage")

    # save the storage
    save_storage()


def open_dir_hist():
    f = open('dir_hist.json')
    dir_hist = json.load(f)
    f.close()
    return dir_hist


def open_mmap():
    fi = open('mmap.json')
    mmap = json.load(fi)
    fi.close()
    return mmap


def open_storage():
    f = open('storage.json')
    storage = json.load(f)
    f.close()
    return storage


# create a directory and store it in dir_dict
def create_directory(name):
    global cur_dict
    global mmap
    mmap = open_mmap()
    dir_hist = open_dir_hist()

    if dir_hist != []:
        c_dir = dir_hist[-1]
        for i in mmap.keys():
            if i == c_dir:
                if name in mmap[i]:
                    print("Directory already exists")
                else:
                    mmap[i][name] = {}
                    print(name," Directory created")
                    save_mmap()
    else:
        if name in mmap:
            print("Directory already exists")
        else:
            mmap[name] = {}
            print(name," Directory created")
            save_mmap()


# delete a file
def delete_file(name):
    global cur_dict
    global mmap
    global dir_hist
    global storage

    storage = open_storage()
    mmap = open_mmap()
    dir_hist = open_dir_hist()

    if (storage != []):
        if dir_hist != []:
            c_dir = dir_hist[-1]
            for i in mmap.keys():
                if i == c_dir:
                    if name+".txt" in mmap[i]:
                        rest_addr = mmap[i][name+".txt"]['address']
                        rest_addr = rest_addr.split(".")
                        print(rest_addr)
                        for k in rest_addr:
                            if k != "":
                                storage.append(int(k))
                        del mmap[i][name+".txt"]
                        print(name," File deleted")
                        save_mmap()
                        save_dir_hist()
                        save_storage()
                    else:
                        print("File does not exist")
        else:
            if name+".txt" in mmap:
                rest_addr = mmap[name+".txt"]['address']
                rest_addr = rest_addr.split(".")
                print(rest_addr)
                for k in rest_addr:
                    if k != "":
                        storage.append((k))
                del mmap[name+".txt"]
                print(name," File deleted")
                save_mmap()
                save_dir_hist()
                save_storage()
            else:
                print("File does not exist")


# delete a directory
def delete_directory(name):
    if name in cur_dict:
        del cur_dict[name]
        print(name," Directory deleted")
        save_mmap()
    else:
        print("Directory does not exist")


# change directory
def change_directory(name):
    global dir_hist
    global cur_dict
    global address
    global mmap
    fi = open('mmap.json')
    mmap = json.load(fi)
    fi.close()
    dir_hist = open_dir_hist()
    if dir_hist != []:
        c_dir = dir_hist[-1]
        for i in mmap.keys():
            if i == c_dir:
                if name in mmap[i]:
                    dir_hist.append(name)
                    print("Directory changed to ",name)
                    save_dir_hist()
                else:
                    print("Directory does not exist")
    else:
        if name in mmap:
            dir_hist.append(name)
            print("Directory changed to ",name)
            save_dir_hist()
        else:
            print("Directory does not exist")


# go to parent directory
def go_to_parent_directory():
    global dir_hist
    global cur_dict
    global address
    f = open('dir_hist.json')
    dir_hist = json.load(f)
    f.close()
    if dir_hist:
        dir_hist.pop()
        print("Directory changed to prev directory")
        save_dir_hist()
    else:
        print("No parent directory")


# list files in current directory
def list_files():
    for key in cur_dict:
        if key[-4:] == ".txt":
            print(key)


# list directories in current directory
def list_directories():
    dir_hist = open_dir_hist()
    print("root/ ", end="")
    for i in dir_hist:
        print(i+"/ ", end="")
    print()


def display_mmap(directory, indent=0):
    for item_name, item in directory.items():
        if isinstance(item, dict):
            print("-" * indent + f"{item_name}/")
            display_mmap(item, indent + 4)
        else:
            print("-" * indent + f"{item_name}: {item}")

# save all data in a json format


def save_mmap():
    f = open('mmap.json', 'w')
    json.dump(mmap, f)
    f.close()


def save_dir_hist():
    f = open('dir_hist.json', 'w')
    json.dump(dir_hist, f)
    f.close()


def save_storage():
    f = open('storage.json', 'w')
    json.dump(storage, f)
    f.close()


def move_file(name, dest_dir):
    global mmap
    global dir_hist
    global storage
    global cur_dict
    file = ''
    mmap = open_mmap()
    dir_hist = open_dir_hist()
    storage = open_storage()
    if (storage != []):
        if dir_hist != []:
            c_dir = dir_hist[-1]
            for i in mmap.keys():
                if i == c_dir:
                    if name+".txt" in mmap[i]:
                        file = mmap[i][name+".txt"]
                        del mmap[i][name+".txt"]
                    else:
                        print("File does not exist")
                        return
            if dest_dir in mmap.keys():
                mmap[dest_dir][name+".txt"] = file
                print(name," File moved")
                save_mmap()
                save_dir_hist()
                save_storage()
            elif dest_dir == "root":
                mmap[name+".txt"] = file
                print(name," File moved")
                save_mmap()
                save_dir_hist()
                save_storage()
            else:
                print("Directory does not exist")

        else:
            if name+".txt" in mmap:
                file = mmap[name+".txt"]
                del mmap[name+".txt"]
                if dest_dir in mmap.keys():
                    mmap[dest_dir][name+".txt"] = file
                    print("File moved")
                    save_mmap()
                    save_dir_hist()
                    save_storage()
                else:
                    print("Directory does not exist")
            else:
                print("File does not exist")


def write(filename, txt, mode):
    global mmap
    global dir_hist
    global storage
    global cur_dict
    file = ''
    mmap = open_mmap()
    dir_hist = open_dir_hist()
    storage = open_storage()
    if (storage != []):
        if dir_hist != []:
            c_dir = dir_hist[-1]
            for i in mmap.keys():
                if i == c_dir:
                    if filename+".txt" in mmap[i]:
                        if file != '':
                            if mode == 'w':
                                prev_data = file['data']
                                # get length of prevdata
                                prev_data_len = len(prev_data)
                                pos = int(
                                    input("enter position at which u want to write: "))
                                if pos <= prev_data_len:
                                    pos = pos-1
                                    file['data'] = prev_data[:pos] + \
                                        txt+prev_data[pos+prev_data_len:]
                                    new_data = file['data']
                                    new_data_len = len(new_data)
                                    if new_data_len > prev_data_len:
                                        diff = new_data_len-prev_data_len
                                        for i in range(diff):
                                            # remove an adress from storage and add it in address of file
                                            file['address'] = file['address'] + \
                                                str(storage.pop())+"."

                                    save_mmap()
                                    save_dir_hist()
                                    print("file written")
                                else:
                                    print("Invalid position")

                            elif mode == 'a':
                                prev_data = file['data']
                                # get length of prevdata
                                prev_data_len = len(prev_data)
                                file['data'] = file['data']+txt
                                mmap[c_dir][filename+".txt"] = file
                                new_data = file['data']
                                new_data_len = len(new_data)
                                if new_data_len > prev_data_len:
                                    diff = new_data_len-prev_data_len
                                    for i in range(diff):
                                        # remove an adress from storage and add it in address of file
                                        file['address'] = file['address'] + \
                                            str(storage.pop())+"."
                                print("File written")
                                save_mmap()
                                save_dir_hist()
                                save_storage()

                        else:
                            print("File does not exist")
        else:
            if filename+".txt" in mmap:
                file = mmap[filename+".txt"]
                if file != '':
                    if mode == 'w':
                        prev_data = file['data']
                        # get length of prevdata
                        prev_data_len = len(prev_data)
                        pos = int(
                            input("enter position at which u want to write: "))
                        if pos <= prev_data_len:
                            pos = pos-1
                            file['data'] = prev_data[:pos] + \
                                txt+prev_data[pos+prev_data_len:]
                            new_data = file['data']
                            new_data_len = len(new_data)
                            if new_data_len > prev_data_len:
                                diff = new_data_len-prev_data_len
                                for i in range(diff):
                                    # remove an adress from storage and add it in address of file
                                    file['address'] = file['address'] + \
                                        str(storage.pop())+"."
                            print("file written")
                            save_mmap()
                            save_dir_hist()
                        else:
                            print("Invalid position")

                    elif mode == 'a':
                        prev_data = file['data']
                        # get length of prevdata
                        prev_data_len = len(prev_data)
                        file['data'] = file['data']+txt
                        mmap[filename+".txt"] = file
                        new_data = file['data']
                        new_data_len = len(new_data)
                        if new_data_len > prev_data_len:
                            diff = new_data_len-prev_data_len
                            for i in range(diff):
                                # remove an adress from storage and add it in address of file
                                file['address'] = file['address'] + \
                                    str(storage.pop())+"."
                        print("File written")
                        save_mmap()
                        save_dir_hist()
                        save_storage()
                else:
                    print("File does not exist")
            else:
                print("File does not exist")


def readfile(name, mode):
    global mmap
    global dir_hist
    global storage
    global cur_dict
    file = ''
    mmap = open_mmap()
    dir_hist = open_dir_hist()
    storage = open_storage()
    if (storage != []):
        if dir_hist != []:
            c_dir = dir_hist[-1]
            for i in mmap.keys():
                if i == c_dir:
                    if name+".txt" in mmap[i]:
                        file = mmap[i][name+".txt"]
                        if file != '':
                            if mode == 'r':
                                print(file['data'])
                            elif mode == 'r+':
                                pos = int(
                                    input("enter position from which u want to read"))
                                if pos <= len(file['data']):
                                    print(file['data'][pos-1])
                                else:
                                    print("Invalid position")

                        else:
                            print("File does not exist")
                    else:
                        print("File does not exist")
        else:
            if name+".txt" in mmap:
                file = mmap[name+".txt"]
                if file != '':
                    if mode == 'r':
                        print(file['data'])
                    elif mode == 'r+':
                        pos = int(
                            input("enter position from which u want to read"))
                        if pos <= len(file['data']):
                            print(file['data'][pos:])
                        else:
                            print("Invalid position")
                else:
                    print("File does not exist")
            else:
                print("File does not exist")


def truncate_size(name, new_size):
    global mmap
    global dir_hist
    global storage
    global cur_dict
    file = ''
    mmap = open_mmap()
    dir_hist = open_dir_hist()
    storage = open_storage()
    if (storage != []):
        if dir_hist != []:
            c_dir = dir_hist[-1]
            for i in mmap.keys():
                if i == c_dir:
                    if name+".txt" in mmap[i]:
                        file = mmap[i][name+".txt"]
                        if file != '':
                            if new_size > len(file['data']):
                                print("Invalid size")
                            else:
                                file['data'] = file['data'][:new_size]
                                # update newsize
                                old_size = file['size']
                                old_address = file['address']
                                old_address = old_address.split(".")
                                file['size'] = new_size
                                # update address
                                file['address'] = old_address[:new_size]
                                released_addresses = old_address[new_size:]
                                # update storage
                                for i in released_addresses:
                                    storage.append(i)
                                # save mmap
                                save_mmap()
                                save_dir_hist()
                                save_storage()
                                print(name," File truncated")

                        else:
                            print("File does not exist")
                    else:
                        print("File does not exist")
        else:
            if name+".txt" in mmap:
                file = mmap[name+".txt"]
                if file != '':
                    if new_size > len(file['data']):
                        print("Invalid size")
                    else:
                        file['data'] = file['data'][:new_size]
                        # update newsize
                        old_size = file['size']
                        old_address = file['address']
                        old_address = old_address.split(".")
                        file['size'] = new_size
                        # update address
                        n_address = old_address[:new_size]
                        file['address'] = ""
                        for k in n_address:
                            file['address'] = file['address']+k+"."
                        released_addresses = old_address[new_size:]
                        # update storage
                        for i in released_addresses:
                            if i != "":
                                storage.append(int(i))
                        # save mmap
                        save_mmap()
                        save_dir_hist()
                        save_storage()
                        print(name," File truncated")
                else:
                    print("File does not exist")
            else:
                print("File does not exist")


def move_within_file(name, s_loc, e_loc):
    global mmap
    global dir_hist
    global storage
    global cur_dict
    file = ''
    mmap = open_mmap()
    dir_hist = open_dir_hist()
    storage = open_storage()
    if (storage != []):
        if dir_hist != []:
            c_dir = dir_hist[-1]
            for i in mmap.keys():
                if i == c_dir:
                    if name+".txt" in mmap[i]:
                        file = mmap[i][name+".txt"]
                        if file != '':
                            if s_loc <= len(file['data']) and s_loc <= len(file['data']):
                                print("Current location is", s_loc)
                                new_loc = int(input("Enter new location"))
                                if new_loc <= len(file['data']):
                                    # swap
                                    temp = file['data'][s_loc-1:e_loc-1]
                                    file['data'][new_loc:] = temp
                                    print("Location changed to " ,new_loc)
                                    save_mmap()
                                    save_dir_hist()
                                    save_storage()
                                else:
                                    print("Invalid location")
                            else:
                                print("Invalid location")
                        else:
                            print("File does not exist")
                    else:
                        print("File does not exist")
        else:
            if name+".txt" in mmap:
                file = mmap[name+".txt"]
                if file != '':
                    if s_loc <= len(file['data']) and s_loc <= len(file['data']):
                        print("Current location is", s_loc)
                        new_loc = int(input("Enter new location"))
                        if new_loc <= len(file['data']):
                            # swap
                            temp = file['data'][s_loc-1:e_loc-1]
                            # remove temp from the data
                            file['data'] = file['data'][:s_loc-1] + \
                                file['data'][e_loc-1:]
                            # add temp to the new location
                            file['data'] = file['data'][:new_loc-1] + \
                                temp+file['data'][new_loc-1:]

                            print("Location changed to " ,new_loc)
                            save_mmap()
                            save_dir_hist()
                            save_storage()
                        else:
                            print("Invalid location")
                    else:
                        print("Invalid location")
                else:
                    print("File does not exist")
            else:
                print("File does not exist")

# create a menu


def menu():
    print("1. Create a file")
    print("2. Create a directory")
    print("3. Delete a file")
    print("4. Delete a directory")
    print("5. Change directory")
    print("6. Go to parent directory")
    print("7. List directories")
    print("8. Display mmap")
    print("9. Move file")
    print("10. Write to a file")
    print("11. Read from a file")
    print("12. Truncate file")
    print("13. Move within file")
    print("14. Exit")


# create a lock to synchronize access to shared resources
lock = threading.Lock()

def create_file_thread():
    lock.acquire()
    name = input("Enter file name: ")
    data = input("Enter file data: ")
    create_file(name, data)
    lock.release()


def create_directory_thread():
    name = input("Enter directory name: ")
    create_directory(name)
    lock.release()

def delete_file_thread():
    name = input("Enter file name: ")
    delete_file(name)
    lock.release()

def delete_directory_thread():
    name = input("Enter directory name: ")
    delete_directory(name)
    lock.release()

def change_directory_thread():
    name = input("Enter directory name: ")
    change_directory(name)
    lock.release()

def go_to_parent_directory_thread():
    go_to_parent_directory()
    lock.release()

def list_directories_thread():
    list_directories()
    lock.release()

def open_mmap_thread():
    mmap = open_mmap()
    display_mmap(mmap)
    lock.release()

def move_file_thread():
    name = input("Enter file name: ")
    dest_dir = input("Enter destination directory: ")
    move_file(name, dest_dir)
    lock.release()

def write_thread():
    name = input("Enter file name: ")
    data = input("Enter file data: ")
    mode = input("Enter mode a for append or w for write at any position: ")
    write(name, data, mode)
    lock.release()

def readfile_thread():
    name = input("Enter file name: ")
    mode = input("Enter mode r for read or r+ for read at any position: ")
    readfile(name, mode)
    lock.release()

def truncate_size_thread():
    name = input("Enter file name: ")
    new_size = int(input("Enter new size: "))
    truncate_size(name, new_size)
    lock.release()

def move_within_file_thread():
    name = input("Enter file name: ")
    s_loc = int(input("Enter start location: "))
    e_loc = int(input("Enter end location: "))
    move_within_file(name, s_loc, e_loc)
    lock.release()

def menu_thread():
    menu()

def main1():

    while True:
        menu_thread()

        choice = int(input("Enter your choice: "))

        if choice == 1:
            t = threading.Thread(target=create_file_thread)
            t.start()
        elif choice == 2:
            t = threading.Thread(target=create_directory_thread)
            t.start()
        elif choice == 3:
            t = threading.Thread(target=delete_file_thread)
            t.start()
        elif choice == 4:
            t = threading.Thread(target=delete_directory_thread)
            t.start()
        elif choice == 5:
            t = threading.Thread(target=change_directory_thread)
            t.start()
        elif choice == 6:
            t = threading.Thread(target=go_to_parent_directory_thread)
            t.start()
        elif choice == 7:
            t = threading.Thread(target=list_directories_thread)
            t.start()
        elif choice == 8:
            t = threading.Thread(target=open_mmap_thread)
            t.start()
        elif choice == 9:
            t = threading.Thread(target=move_file_thread)
            t.start()
        elif choice == 10:
            t = threading.Thread(target=write_thread)
            t.start()
        elif choice == 11:
            t = threading.Thread(target=readfile_thread)
            t.start()
        elif choice == 12:
            t = threading.Thread(target=truncate_size_thread)
            t.start()   
        elif choice == 13:
            t = threading.Thread(target=move_within_file_thread)
            t.start()
        elif choice == 14:
            break
        else:
            print("Invalid choice")



def main():
    users=int(input("Enter number of users: "))
    if users==1:

        print("one user working")
        create_file("file1", "abcd")
        create_file("file2", "123")
        display_mmap(mmap)
        write("file1", "xyz", "w")
        display_mmap(mmap)

    elif users==2:

        
        print("two users working")
        create_file("file1", "abcd")
        create_file("file2", "123")
        display_mmap(mmap)
        write("file1", "xyz", "w")
        display_mmap(mmap)
        create_file("file3", "abcd")
        delete_file("file2")
        truncate_size("file1", 2)
        display_mmap(mmap)

    elif users==3:

        print("three users working")
        create_file("file1", "abcd")
        create_file("file2", "123")
        display_mmap(mmap)
        write("file1", "xyz", "w")
        display_mmap(mmap)
        create_file("file3", "abcd")
        delete_file("file2")
        truncate_size("file1", 2)
        display_mmap(mmap)
        create_directory("dir1")
        change_directory("dir1")
        create_file("file4", "abcd")
        go_to_parent_directory()
        display_mmap(mmap)

    elif users==4:

        print("four users working")
        create_file("file1", "abcd")
        create_file("file2", "123")
        display_mmap(mmap)
        write("file1", "xyz", "w")
        display_mmap(mmap)
        create_file("file3", "abcd")
        delete_file("file2")
        truncate_size("file1", 2)
        display_mmap(mmap)
        create_directory("dir1")
        change_directory("dir1")
        create_file("file4", "abcd")
        go_to_parent_directory()
        display_mmap(mmap)
        create_directory("dir2")
        change_directory("dir2")
        create_directory("dir3")
        display_mmap(mmap)

    elif users==5:

        print("five users working")
        create_file("file1", "abcd")
        create_file("file2", "123")
        display_mmap(mmap)
        write("file1", "xyz", "w")
        display_mmap(mmap)
        create_file("file3", "abcd")
        delete_file("file2")
        truncate_size("file1", 2)
        display_mmap(mmap)
        create_directory("dir1")
        change_directory("dir1")
        create_file("file4", "abcd")
        go_to_parent_directory()
        display_mmap(mmap)
        create_directory("dir2")
        change_directory("dir2")
        create_directory("dir3")
        display_mmap(mmap)
        go_to_parent_directory()
        create_file("file5", "abcd")
        

    else:
        print("Invalid choice")






if __name__ == "__main__":
    main()