import sys

def print_numbered_lines(input_stream):
    line_number = 1
    for line in input_stream:
        print(f"{line_number:>6}\t{line}", end="")
        line_number += 1

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                print_numbered_lines(f)
        except FileNotFoundError:
            print(f"{filename}: No such file or directory")
        return

    print_numbered_lines(sys.stdin)

if __name__ == "__main__":
    main();
