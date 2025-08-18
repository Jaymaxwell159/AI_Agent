from functions.get_files_info import write_file

def print_result(title, result):
    print(title)
    print(result)
    print()

if __name__ == "__main__":
    # Test 1: Write to lorem.txt in calculator
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print_result("Result for 'lorem.txt':", result1)

    # Test 2: Write to pkg/morelorem.txt in calculator
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print_result("Result for 'pkg/morelorem.txt':", result2)

    # Test 3: Write to /tmp/temp.txt (should not be allowed)
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print_result("Result for '/tmp/temp.txt':", result3)