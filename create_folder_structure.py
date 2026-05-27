import os
import argparse


def create_folder_with_markdowns(folder_name: str, num_markdowns: int, base_path: str = ".") -> None:
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    for i in range(1, num_markdowns + 1):
        md_filename = f"chapter{i:02d}.md"
        md_path = os.path.join(folder_path, md_filename)
        if not os.path.exists(md_path):
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# Chapter {i}\n\n")
            print(f"  Created: {md_path}")
        else:
            print(f"  Skipped (exists): {md_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a folder with a given number of markdown files inside."
    )
    parser.add_argument("folder_name", help="Name of the folder to create")
    parser.add_argument("num_markdowns", type=int, help="Number of markdown files to generate")
    parser.add_argument(
        "--base-path",
        default=".",
        help="Base directory where the folder will be created (default: current directory)",
    )
    args = parser.parse_args()

    if args.num_markdowns < 1:
        parser.error("num_markdowns must be at least 1")

    create_folder_with_markdowns(args.folder_name, args.num_markdowns, args.base_path)
    print(f"\nDone: '{args.folder_name}' with {args.num_markdowns} markdown file(s).")


if __name__ == "__main__":
    main()
