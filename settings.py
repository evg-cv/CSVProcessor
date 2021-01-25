import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]

EXCEL_PATH = ""
