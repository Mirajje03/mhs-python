import sys

def print_last_lines(lines, count):
    for line in lines[-count:]:
        print(line, end="")

def main():
    files = sys.argv[1:]

    if not files:
        lines = sys.stdin.readlines()
        print_last_lines(lines, 17)
        return

    for i, filename in enumerate(files):
        try:
            with open(filename, 'r') as f:
                if len(files) > 1:
                    if i > 0:
                        print()
                    print(f"==> {filename} <==")
                
                lines = f.readlines()
                print_last_lines(lines, 10)
        except FileNotFoundError:
            print(f"{filename}: No such file or directory")

if __name__ == "__main__":
    main()
