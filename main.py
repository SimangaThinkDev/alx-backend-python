# Context managers


class OpenClose():

    def __init__(self, path_to_file, mode):
        self.path_to_file = path_to_file
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open( self.path_to_file, self.mode )
        return self.file

    def __exit__(self, type, value, traceback):
        if self.file:
            self.file.close()
        else:
            print(f"An exception occured...\n{value}:{type}\n{traceback}")


#----------------------------------------Using Context Managers------------------------------------------

import contextlib

@contextlib.contextmanager
def logger(filename: str, mode: str):
    file = None

    try:
        print("Opening file")
        file = open(filename, mode)
        yield file
    finally:
        if file:
            file.close()
            print( "File operation was successful" )


with logger(filename="stuff.txt", mode="r") as file:
    data = file.read()

print(data)
