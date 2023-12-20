import os

class ModuleDirFile:
    def __init__(self, filename, mode='r'):
        # Get the directory of the current module
        self.module_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full file path
        self.file_path = os.path.join(self.module_dir, filename)
        # Store the mode
        self.mode = mode

    def __enter__(self):
        # Open the file with the specified mode and return the file object
        self.file = open(self.file_path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the file
        if self.file:
            self.file.close()
