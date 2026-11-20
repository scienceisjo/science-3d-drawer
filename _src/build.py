"""과학 3D 자료 서랍 — resources.json 을 index.html 에 끼워 넣는다.

쓰는 법: python _src/build.py   (저장소 루트에서)
자료를 더하거나 고칠 때는 resources.json 만 고치고 이 스크립트를 다시 돌린다.
GitHub Pages 는 '_' 로 시작하는 폴더를 내보내지 않으므로 _src/ 는 온라인에 나가지 않는다.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KINDS = {'edit', 'embed', 'link', 'check'}
NEED = ['id', 'name', 'maker', 'url', 'subject', 'desc', 'units', 'tech', 'lang', 'kind',
        'license', 'licenseNote', 'licenseUrl', 'howto', 'credit', 'embeddable', 'checked']


def main():
    data = json.loads((ROOT / 'resources.json').read_text(encoding='utf-8'))
    ids, errs = set(), []
    for it in data['items']:
        miss = [k for k in NEED if k not in it]
        if miss:
            errs.append(f"{it.get('id')}: 빠진 칸 {miss}")
        if it.get('kind') not in KINDS:
            errs.append(f"{it.get('id')}: kind 가 {it.get('kind')}")
        if it.get('subject') not in data['subjects']:
            errs.append(f"{it.get('id')}: subject 가 {it.get('subject')}")
        if it.get('kind') == 'link' and it.get('embeddable'):
            errs.append(f"{it.get('id')}: 링크로만인데 iframe 코드를 내보냄")
        if it.get('id') in ids:
            errs.append(f"{it.get('id')}: id 중복")
        ids.add(it.get('id'))
    if errs:
        print('\n'.join(errs))
        sys.exit(1)
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    tpl = (ROOT / '_src' / 'index.tpl.html').read_text(encoding='utf-8')
    assert tpl.count('/*DATA*/') == 1
    (ROOT / 'index.html').write_text(tpl.replace('/*DATA*/', blob), encoding='utf-8', newline='\n')
    print(f"index.html 만듦 · 자료 {len(data['items'])}개 · 최종 확인 {data['updated']}")


if __name__ == '__main__':
    main()
