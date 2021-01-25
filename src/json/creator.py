import json
import ntpath
import os

from src.excel.parser import ExcelParser
from settings import OUTPUT_DIR


def export_result(excel_file_path):
    file_name = ntpath.basename(excel_file_path).replace(".xlsx", "")
    output_file_path = os.path.join(OUTPUT_DIR, f"{file_name}_output.json")
    parse_result = ExcelParser(excel_path=excel_file_path).run()
    with open(output_file_path, 'w') as f:
        json.dump(parse_result, f, indent=4)
    print(f"INFO:: Successfully saved in {output_file_path}")

    return


if __name__ == '__main__':
    export_result(excel_file_path="")
