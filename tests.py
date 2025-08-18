from functions.get_files_info import run_python_file

def print_result(title, result):
    print(title)
    print(result)
    print()

if __name__ == "__main__":
    # Test 1: Run main.py (should print usage instructions)
    result1 = run_python_file("calculator", "main.py")
    print_result("Result for 'main.py':", result1)

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