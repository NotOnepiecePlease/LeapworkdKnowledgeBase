"""Cria pacotes portáteis e confere seus arquivos, sem dependências externas."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default='v1.3.1')
    args = parser.parse_args()
    if not re.fullmatch(r'v\d+\.\d+\.\d+', args.version):
        parser.error('Use uma versão como v1.0.0')
    content = json.loads((ROOT / 'research/course-content.json').read_text(encoding='utf-8'))
    videos = sorted({lesson['video'] for lesson in content['lessons'] if lesson.get('video')})
    missing = [name for name in videos if not (ROOT / 'videos' / f'{name}.mp4').is_file()]
    if missing:
        raise SystemExit('Vídeos ausentes: ' + ', '.join(missing))
    files = [ROOT / 'README.md', ROOT / 'ENRIQUECIMENTO.md', ROOT / 'REVISAO.md', ROOT / 'Abrir caderno.cmd']
    files += sorted(p for p in (ROOT / 'site').rglob('*') if p.is_file())
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    prefix = f'LeapworkKnowledgeBase-{args.version}'
    checksums = []
    for edition in ('essencial', 'completo'):
        included = files + ([ROOT / 'videos' / f'{name}.mp4' for name in videos] if edition == 'completo' else [])
        archive = output / f'{prefix}-{edition}.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
            for source in included:
                relative = source.relative_to(ROOT).as_posix()
                zipped.write(source, f'{prefix}/{relative}', compress_type=zipfile.ZIP_STORED if source.suffix == '.mp4' else zipfile.ZIP_DEFLATED)
        with zipfile.ZipFile(archive) as zipped:
            assert zipped.testzip() is None, f'ZIP inválido: {archive}'
            assert len(zipped.namelist()) == len(included)
            assert f'{prefix}/site/index.html' in zipped.namelist()
        with archive.open('rb') as source:
            digest = hashlib.file_digest(source, 'sha256').hexdigest()
        checksums.append(f'{digest}  {archive.name}')
        print(f'{archive.name}: {archive.stat().st_size:,} bytes; {len(included)} arquivos; CRC verificado', flush=True)
    (output / 'SHA256SUMS.txt').write_text('\n'.join(checksums) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
