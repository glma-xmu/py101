"""Compress local slide renders for publication; never copy source decks.

First run export_project_slides.ps1 locally (PowerPoint and Poppler required).
Then run this script with Pillow installed. Normal site builds use the committed
WebP files and need none of these conversion dependencies.
"""
from pathlib import Path
import json
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'resource/projects/.previews'
DEST = ROOT / 'docs/projects'
TITLES = {
    '26s-01': 'DataMind: Stock Data Analysis with Machine Learning',
    '26s-02': 'Forecasting Commodity Returns',
    '26s-04': 'Predicting Student Performance from Game Play',
    '26s-05': 'AI-Generated Text Detection',
    '26s-06': 'Forest Cover Type Prediction',
    '26s-07': 'Christmas Tree Bin Packing Optimization',
    '26s-08': 'Dynamic Retraining for Quantitative Models',
    '26s-09': 'F1 Pit Stop Strategy Modeling',
    '26s-10': 'F1 Pit Stop Prediction',
    '26s-11': 'Plant Disease Classification',
    '26s-12': 'Money Talks, But Does Happiness Walk?',
    '26s-13': 'AI4Code: Understanding Code in Python Notebooks',
    '26s-14': 'Ocean Temperature Profile Prediction',
    '26s-15': 'Orbit War Agent Development',
}


def build():
    records = json.loads((SOURCE / 'sources.json').read_text(encoding='utf-8-sig'))
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('Duplicate project IDs in source metadata')
    titles_path = ROOT / 'scripts/project_titles.json'
    titles = {**TITLES, **(json.loads(titles_path.read_text(encoding='utf-8')) if titles_path.exists() else {})}
    projects = []
    for record in records:
        project_id = record['id']
        if project_id not in titles:
            raise ValueError(f'Add a reviewed title for {project_id}: {record["source"]}')
        destination = DEST / 'previews' / project_id
        destination.mkdir(parents=True, exist_ok=True)
        for number in range(1, record['count'] + 1):
            source_image = SOURCE / project_id / f'{number}.png'
            preview = destination / f'{number}.webp'
            if (preview.exists() and preview.stat().st_mtime >= source_image.stat().st_mtime
                    and (number != 1 or (destination / 'cover.webp').exists())):
                continue
            with Image.open(SOURCE / project_id / f'{number}.png') as image:
                image.convert('RGB').save(destination / f'{number}.webp', quality=83, method=6)
                if number == 1:
                    cover = image.convert('RGB')
                    cover.thumbnail((640, 400), Image.Resampling.LANCZOS)
                    cover.save(destination / 'cover.webp', quality=80, method=6)
        projects.append(dict(id=project_id, cohort=record['cohort'], title=titles[project_id], count=record['count']))
    (DEST / 'manifest.json').write_text(json.dumps(projects, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(projects)} projects, {sum(p["count"] for p in projects)} slides.')
    # A private contact sheet for visual QA; never part of the published site.
    sheet = Image.new('RGB', (1000, ((len(projects) + 3) // 4) * 175), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, project in enumerate(projects):
        with Image.open(DEST / 'previews' / project['id'] / 'cover.webp') as cover:
            thumb = ImageOps.contain(cover, (240, 140))
            x, y = (i % 4) * 250, (i // 4) * 175
            sheet.paste(thumb, (x, y))
            draw.text((x + 5, y + 145), project['id'], fill='black')
    sheet.save(SOURCE / 'contact-sheet.jpg')


if __name__ == '__main__':
    build()
