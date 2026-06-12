from pathlib import Path
import re


INPUT_PATH = Path("data/ipl_dataset_text.txt")
OUTPUT_DIR = Path("data/sections")


def split_into_sections(text: str) -> dict[str, str]:
    pattern = r"(Section\s+\d+:[^\n]+)"

    parts = re.split(pattern, text)

    sections = {}

    intro_text = parts[0].strip()
    if intro_text:
        sections["00_intro"] = intro_text

    for index in range(1, len(parts), 2):
        heading = parts[index].strip()
        content = parts[index + 1].strip() if index + 1 < len(parts) else ""

        section_number_match = re.search(r"Section\s+(\d+)", heading)

        if section_number_match:
            section_number = section_number_match.group(1).zfill(2)
            safe_heading = heading.lower()
            safe_heading = re.sub(r"[^a-z0-9]+", "_", safe_heading)
            safe_heading = safe_heading.strip("_")

            file_name = f"{section_number}_{safe_heading}"

            sections[file_name] = heading + "\n\n" + content

    return sections


def main():
    if not INPUT_PATH.exists():
        print(f"Input file not found: {INPUT_PATH}")
        return

    text = INPUT_PATH.read_text(encoding="utf-8")

    OUTPUT_DIR.mkdir(exist_ok=True)

    sections = split_into_sections(text)

    for file_name, section_text in sections.items():
        output_path = OUTPUT_DIR / f"{file_name}.txt"
        output_path.write_text(section_text, encoding="utf-8")

    print("Section splitting completed!")
    print(f"Total sections created: {len(sections)}")
    print(f"Saved inside: {OUTPUT_DIR}")
    print()

    print("Created files:")
    for file_name in sections:
        print(f"- {file_name}.txt")


if __name__ == "__main__":
    main()