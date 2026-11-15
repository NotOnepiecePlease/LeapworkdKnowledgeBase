"""Use the local media as the authority for durations and validate lesson assets."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
site = ROOT / 'site'
script = "global.window={};require('./site/content.js');require('./site/module2.js');require('./site/module1-extra.js');require('./site/catalog.js');require('./site/module2-extra.js');require('./site/module3.js');require('./site/module4.js');require('./site/module5.js');console.log(JSON.stringify(window.LEAP));"
data = json.loads(subprocess.check_output(['node', '-e', script], cwd=ROOT, encoding='utf-8'))
media = []
for lesson in data['lessons']:
    seconds = None
    if lesson.get('video'):
        path = ROOT / 'videos' / f"{lesson['video']}.mp4"
        info = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration,size',
            '-show_entries', 'stream=codec_type,codec_name,width,height', '-of', 'json', str(path)
        ], encoding='utf-8'))
        seconds = round(float(info['format']['duration']))
        lesson['duration'] = f'{seconds // 60}:{seconds % 60:02}'
        media.append({'lesson': lesson['slug'], 'video': lesson['video'], 'duration': seconds, 'probe': info})
    for step in lesson['steps']:
        if seconds is not None:
            assert 0 <= step['time'] < seconds, f'Invalid timestamp: {lesson["slug"]}'
        else:
            assert 'time' not in step and 'image' not in step and 'animation' not in step
            assert step.get('doc') in [p for _,p in lesson['docs']], lesson['slug']
        if 'image' in step:
            assert (site / 'assets' / 'frames' / f"{lesson['video']}-{step['image']}.jpg").exists()
            assert step['image'] < seconds
        if 'animation' in step:
            clip = step['animation']
            assert (site / 'assets' / 'animations' / clip['file']).exists()
            assert 0 <= clip['start'] < clip['end'] <= seconds
        if 'imagePath' in step:
            assert (site / step['imagePath']).is_file(), step['imagePath']
    for _, doc_path in lesson['docs']:
        assert (ROOT / 'research' / 'docs' / (doc_path.replace('/', '__') + '.json')).exists(), doc_path
for _, file in data.get('module3Downloads',[]):
    assert (site / file).is_file(), file
(ROOT / 'research' / 'media-manifest.json').write_text(json.dumps(media, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'research' / 'course-content.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
durations = {lesson['video']:lesson['duration'] for lesson in data['lessons'] if lesson.get('video')}
(site / 'media.js').write_text('/* Durações verificadas nos arquivos de vídeo locais. */\n{const durations = ' + json.dumps(durations) + '; window.LEAP.lessons.forEach(l=>{l.duration=durations[l.video]||l.duration;});}\n', encoding='utf-8')
print(json.dumps({'lessons': len(data['lessons']), 'videos':len(media),'steps': sum(len(l['steps']) for l in data['lessons']), 'images_used': sum('image' in s or 'imagePath' in s for l in data['lessons'] for s in l['steps']), 'glossary': len(data['glossary'])}, ensure_ascii=False))
