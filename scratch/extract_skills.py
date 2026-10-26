from pathlib import Path
import re
import yaml

src_path = Path(r"c:\Users\foste\Downloads\archival-and-refresh-bots.md")
dest_dir = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\.agents\skills")

text = src_path.read_text(encoding="utf-8").replace("\r\n", "\n")
# Eliminate all em-dashes and en-dashes per estate law
text = text.replace("\u2014", "--").replace("\u2013", "-")

pattern = re.compile(
    r"### `([a-z0-9-]+)`\s*\n\s*Save as `skills/[^/]+/SKILL\.md`\.\s*\n\s*```yaml\s*\n(---.*?---)\s*\n```\s*\n(.*?)(?=\n---\n|\n### `|\Z)",
    re.DOTALL
)

matches = list(pattern.finditer(text))
print(f"Skills parsed: {len(matches)}")

for m in matches:
    slug = m.group(1)
    fm_raw = m.group(2).strip()
    body = m.group(3).strip()
    
    # Parse yaml to unwrap folded multiline descriptions
    fm_data = yaml.safe_load(fm_raw.replace("---", ""))
    name = fm_data.get("name", slug)
    desc = " ".join(fm_data.get("description", "").split())
    
    clean_fm = f"---\nname: {name}\ndescription: \"{desc}\"\n---"
    content = f"{clean_fm}\n\n{body}\n"
    
    target_file = dest_dir / slug / "SKILL.md"
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")
    assert "\u2014" not in content and "\u2013" not in content
    print(f"Cleaned {slug}: desc ({len(desc)} chars)")
