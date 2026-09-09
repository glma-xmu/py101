"""Check deployed gallery coverage and ensure original decks are not published."""
import json
import sys
from pathlib import Path

site = Path(sys.argv[1] if len(sys.argv) > 1 else 'site')
projects = json.loads((site / 'projects/manifest.json').read_text(encoding='utf-8'))
assert projects and len({p['id'] for p in projects}) == len(projects), 'Missing or duplicate projects'
for project in projects:
    assert project['title'] and project['count'] > 0
    folder = site / 'projects/previews' / project['id']
    for name in ['cover'] + list(map(str, range(1, project['count'] + 1))):
        asset = folder / f'{name}.webp'
        data = asset.read_bytes()
        assert data[:4] == b'RIFF' and data[8:12] == b'WEBP', asset
for locale in ['', 'zh/']:
    page = (site / locale / 'projects/index.html').read_text(encoding='utf-8')
    assert 'data-projects' in page and 'data-cohort="25S"' in page and 'data-cohort="26S"' in page
    assert 'javascripts/projects.js?v=1' in page
    for path in (site / locale / 'projects').rglob('*'):
        assert path.suffix.lower() not in {'.pptx', '.ppt', '.pdf', '.docx'}, path
assert not (site / 'resource/projects').exists(), 'Original sources must stay private'
print(f'Project gallery OK: {len(projects)} projects, {sum(p["count"] for p in projects)} slides, EN/ZH, no original decks.')
