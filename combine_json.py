import json
from collections import OrderedDict
import os

def ensure_same_keys_and_order(obj1, obj2):
    all_keys = sorted(set(obj1.keys()) | set(obj2.keys()))

    ordered_obj1 = OrderedDict()
    ordered_obj2 = OrderedDict()

    for key in all_keys:
        ordered_obj1[key] = obj1.get(key, "")
        ordered_obj2[key] = obj2.get(key, "")

    return ordered_obj1, ordered_obj2

def load_and_display_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print(f"\nContents of {file_path}:")
        print(json.dumps(data, indent=4))
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON.")
        return None

def merge_json_files(file1, file2, output_file, container_name=None):
    data1, data2 = ensure_same_keys_and_order(file1, file2)

    if container_name:
        merged_data = {container_name: [data1, data2]}
    else:
        merged_data = [data1, data2]

    try:
        with open(output_file, 'w') as outfile:
            json.dump(merged_data, outfile, indent=4)
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")
        return

    return merged_data

if __name__ == "__main__":
    file1 = input("Enter the name of the first JSON file: ")
    file2 = input("Enter the name of the second JSON file: ")
    output_file = input("Enter the name for the output JSON file: ")

    create_container = input("Would you like to create a container object for the merged data? (yes/no): ").strip().lower()

    if create_container in ['yes', 'y']:
        container_name = input("Enter the name for the container object: ")
    else:
        container_name = None

    # Display contents of both files
    data1 = load_and_display_json(file1)
    if data1 is None:
        exit(1)

    data2 = load_and_display_json(file2)
    if data2 is None:
        exit(1)

    merged_data = merge_json_files(data1, data2, output_file, container_name)

    if merged_data is not None:
        print("\nMerged JSON data:")
        print(json.dumps(merged_data, indent=4))

        print(f"\nMerged data has been written to {output_file}")
        try:
            file_size = os.path.getsize(output_file)
            print(f"File size: {file_size} bytes")
        except OSError:
            print("Could not retrieve the file size.")
        print("Script execution completed.")