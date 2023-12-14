def shrekify_file(input_file_path, output_file_path="google_fourms\Shrek.txt"):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        shrekified_content = [' '.join(['Shrek' for _ in line.split()]) + '\n' for line in lines]

        with open(output_file_path, 'w') as file:
            file.writelines(shrekified_content)
        
        return "File shrekified successfully."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print(shrekify_file("google_fourms/counter_test.txt"))

