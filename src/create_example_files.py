import os

def create_example_files():
    work_dir = 'work'
    os.makedirs(work_dir, exist_ok=True)

    # Create example .txt file
    txt_file_path = os.path.join(work_dir, 'example.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write("This is an example text file.\nYou can use it to test the file tree functionality.")

    # Create example .py file
    py_file_path = os.path.join(work_dir, 'example.py')
    with open(py_file_path, 'w', encoding='utf-8') as py_file:
        py_file.write("# This is an example Python file.\n")
        py_file.write("def example_function():\n")
        py_file.write("    print('Hello, world!')\n")

    print(f"Example files created in '{work_dir}' directory.")

if __name__ == "__main__":
    create_example_files()
