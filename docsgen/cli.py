import argparse
from .docsgen import DocsGen

def main():
    parser = argparse.ArgumentParser(description='DocsGen CLI')
    parser.add_argument('lib', help='Lib name')
    parser.add_argument('dir', help='Library dir')
    args = parser.parse_args()
    docs = DocsGen(args.lib, args.dir)
    docs.write_documentation()
    print(f"[!] Done")

if __name__ == '__main__':
    main()
