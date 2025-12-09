import sys

def get_counts(content):
    lines = content.count('\n')
    words = len(content.split())
    bytes_count = len(content.encode('utf-8'))
    return lines, words, bytes_count

def main():
    filenames = sys.argv[1:]

    if not filenames:
        content = sys.stdin.read()
        l, w, b = get_counts(content)
        print(f"{l:>8}{w:>8}{b:>8}")
        return

    total_lines = 0
    total_words = 0
    total_bytes = 0
    
    for name in filenames:
        try:
            with open(name, 'r', encoding='utf-8') as f:
                content = f.read()
                l, w, b = get_counts(content)
                
                print(f"{l:>8}{w:>8}{b:>8} {name}")
                
                total_lines += l
                total_words += w
                total_bytes += b
                
        except FileNotFoundError:
            print(f"wc: {name}: No such file or directory")
        except IsADirectoryError:
            print(f"wc: {name}: Is a directory")

    if len(filenames) > 1:
        print(f"{total_lines:>8}{total_words:>8}{total_bytes:>8} total")

if __name__ == "__main__":
    main()
