"""Build installable skills into dist/skills/.

Every skill under skills/<category>/<name>/ becomes dist/skills/coding-<name>/, with its
frontmatter `name` prefixed and pack-relative paths rewritten to point at the installed
siblings. coding-standards also bundles standards/Clean-Code/ and standards/Principles.md as
references, so the lessons travel with the skill.

Run from anywhere: python scripts/build_skills.py
"""

import re
import shutil
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parent.parent
SOURCE_SKILLS = PACK_ROOT / "skills"
DIST_SKILLS = PACK_ROOT / "dist" / "skills"
PREFIX = "coding-"
STANDARDS_SKILL = PREFIX + "standards"


def main():
    if DIST_SKILLS.exists():
        shutil.rmtree(DIST_SKILLS)
    DIST_SKILLS.mkdir(parents=True)

    skill_dirs = sorted(path.parent for path in SOURCE_SKILLS.glob("*/*/SKILL.md"))
    skill_names = [path.name for path in skill_dirs]

    for source_dir in skill_dirs:
        built_dir = DIST_SKILLS / (PREFIX + source_dir.name)
        shutil.copytree(source_dir, built_dir)
        rewrite_skill_file(built_dir / "SKILL.md", source_dir.name, skill_names)

    bundle_standards_references(DIST_SKILLS / STANDARDS_SKILL, skill_names)
    print(f"Built {len(skill_dirs)} skills into {DIST_SKILLS.relative_to(PACK_ROOT)}")


def rewrite_skill_file(skill_file, source_name, skill_names):
    text = skill_file.read_text(encoding="utf-8")
    text = re.sub(r"^name: .*$", f"name: {PREFIX}{source_name}", text, count=1, flags=re.M)
    text = rewrite_pack_paths(text, skill_names, standards_root="../" + STANDARDS_SKILL + "/references")
    write_lf(skill_file, text)


def bundle_standards_references(standards_dir, skill_names):
    references = standards_dir / "references"
    shutil.copytree(PACK_ROOT / "standards" / "Clean-Code", references / "clean-code")
    shutil.copy(PACK_ROOT / "standards" / "Principles.md", references / "principles.md")
    for reference_file in references.rglob("*.md"):
        text = reference_file.read_text(encoding="utf-8")
        text = text.replace("](./Clean-Code/", "](./clean-code/")
        write_lf(reference_file, rewrite_pack_paths(text, skill_names, standards_root="references"))


def rewrite_pack_paths(text, skill_names, standards_root):
    """Point pack-layout paths at installed skill locations."""
    names = "|".join(map(re.escape, skill_names))
    text = re.sub(rf"(?:\.\./)*skills/[\w-]+/({names})/SKILL\.md", rf"../{PREFIX}\1/SKILL.md", text)
    text = re.sub(rf"(?<![\w-])\.\./({names})/SKILL\.md", rf"../{PREFIX}\1/SKILL.md", text)
    text = re.sub(r"(?:\.\./)*standards/Clean-Code/", f"{standards_root}/clean-code/", text)
    text = re.sub(r"(?:\.\./)*standards/Principles\.md", f"{standards_root}/principles.md", text)
    return text


def write_lf(path, text):
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
