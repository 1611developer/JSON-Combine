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

def merge_json_files(file1, file2, output_file, container_name=None):
    try:
        with open(file1, 'r') as f1:
            data1 = json.load(f1)
    except FileNotFoundError:
        print(f"Error: The file {file1} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {file1} is not a valid JSON.")
        return

    try:
        with open(file2, 'r') as f2:
            data2 = json.load(f2)
    except FileNotFoundError:
        print(f"Error: The file {file2} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {file2} is not a valid JSON.")
        return

    data1, data2 = ensure_same_keys_and_order(data1, data2)

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
        merged_data = merge_json_files(file1, file2, output_file, container_name)
    else:
        merged_data = merge_json_files(file1, file2, output_file)

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