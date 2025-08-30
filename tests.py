from functions import get_files_info
from functions.get_files_info import run_python_file, get_file_content, write_file

def print_result(title, result):
    print(title)
    print(result)
    print()

if __name__ == "__main__":
    # Test 1: List root directory
    result1 = get_files_info.get_files_info("calculator", ".")
    print_result("Result for root directory:", result1)

    # Test 2: Run main.py with argument "3 + 5"
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print_result("Result for 'main.py' with '3 + 5':", result2)

    # Test 3: Run tests.py
    result3 = run_python_file("calculator", "tests.py")
    print_result("Result for 'tests.py':", result3)

    # Test 4: Run ../main.py (should return error)
    result4 = run_python_file("calculator", "../main.py")
    print_result("Result for '../main.py':", result4)

    # Test 5: Run nonexistent.py (should return error)
    result5 = run_python_file("calculator", "nonexistent.py")
    print_result("Result for 'nonexistent.py':", result5)

    # Test 6: List pkg directory
    result6 = get_files_info.get_files_info("calculator", "pkg")
    print_result("Result for pkg directory:", result6)

    # Test 7: Read main.py
    result7 = get_file_content("calculator", "main.py")
    print_result("Read main.py:", result7)

    # Test 8: Write to lorem.txt
    result8 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print_result("Write to lorem.txt:", result8)

    # Test 9: Write to /tmp/temp.txt (should not be allowed)
    result9 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print_result("Write to /tmp/temp.txt:", result9)