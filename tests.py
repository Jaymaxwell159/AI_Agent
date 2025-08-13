from functions.get_files_info import get_file_content

def print_result(title, result):
    print(title)
    print(result)
    print()

if __name__ == "__main__":
    # Test 1: main.py in calculator
    result1 = get_file_content("calculator", "main.py")
    print_result("Result for 'main.py':", result1)

    # Test 2: pkg/calculator.py in calculator
    result2 = get_file_content("calculator", "pkg/calculator.py")
    print_result("Result for 'pkg/calculator.py':", result2)

    # Test 3: /bin/cat (should return error)
    result3 = get_file_content("calculator", "/bin/cat")
    print_result("Result for '/bin/cat':", result3)

    # Test 4: pkg/does_not_exist.py (should return error)
    result4 = get_file_content("calculator", "pkg/does_not_exist.py")
    print_result("Result for 'pkg/does_not_exist.py':", result4)