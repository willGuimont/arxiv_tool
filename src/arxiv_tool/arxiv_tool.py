import argparse
import os
import pathlib
import re
import shutil
from typing import Sequence


def remove_useless_files(dir_path: pathlib.Path):
    shutil.rmtree(dir_path / '.git', ignore_errors=True)

    files_to_remove = ['*.aux', '*.log', '*.bbl', '*.blg', '*.fdb_latexmk', '*.fls', '*.out', 'root.pdf', '*.xml',
                       'root-blx.bib']
    for ext in files_to_remove:
        for f in dir_path.rglob(ext):
            f.unlink()


def replace_between_indices(s: str, start_index: int, end_index: int, replacement: str) -> str:
    prefix = s[:start_index]
    suffix = s[end_index:]
    return prefix + replacement + suffix


def fuse_texs(dir_path: pathlib.Path, tex_source: str) -> str:
    input_regex = re.compile(r'\\input{(.*)}')

    for include in reversed(list(input_regex.finditer(tex_source))):
        include_path = dir_path / pathlib.Path(include.group(1)).with_suffix(".tex")

        with open(include_path, 'r') as file:
            content = file.read() + '\n\n'

        include_path.unlink()

        start, end = include.span()
        tex_source = replace_between_indices(tex_source, start, end, content)

    return tex_source


def remove_commented_lines(tex_source: str) -> str:
    return "\n".join(
        filter(
            lambda l: not l.startswith("%"),
            tex_source.split("\n"),
        ),
    )


def move_figures(
        dir_path: pathlib.Path,
        tex_source: str,
        ignored_fignames: Sequence[str],
) -> str:
    tex_source = remove_commented_lines(tex_source)
    fig_regex = re.compile(r'\\includegraphics\[.*\]\{(.*)\}')

    for include in reversed(list(fig_regex.finditer(tex_source))):
        fig = pathlib.Path(include.group(1))
        if fig.name.lower() in ignored_fignames:
            continue
        fig_path = dir_path / fig
        fig_out_path = dir_path / fig_path.name.replace('_', '')
        shutil.move(fig_path, fig_out_path)

        start, end = include.span(1)
        tex_source = replace_between_indices(tex_source, start, end, fig.name.replace('_', ''))

    return tex_source


def add_arxiv_message(tex_source: str) -> str:
    tex_source += '\n' + r'\typeout{get arXiv to do 4 passes: Label(s) may have changed. Rerun}'
    return tex_source


def rm_dirs(dir_path: pathlib.Path):
    for f in dir_path.iterdir():
        if f.is_dir():
            shutil.rmtree(f)


def main():
    parser = argparse.ArgumentParser(description='Publish arXiv papers')
    parser.add_argument('src_dir', type=str, help='source directory')
    parser.add_argument('dst_dir', type=str, help='destination directory')
    parser.add_argument("--ignore-img", type=str, nargs="+", help="ignored image names", default=[])
    parser.add_argument('-f', '--force', action='store_true', help='delete dst_dir if it exists')
    args = parser.parse_args()

    src_dir = pathlib.Path(args.src_dir)
    dst_dir = pathlib.Path(args.dst_dir)
    force_flag = args.force
    ignored_imgnames = args.ignore_img

    if not force_flag and dst_dir.exists() and len(list(dst_dir.iterdir())) > 0:
        raise FileExistsError(f'{dst_dir} already exists, use -f to force delete')

    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=force_flag)
    remove_useless_files(dst_dir)

    root = dst_dir / 'root.tex'

    if not root.exists():
        raise FileNotFoundError(f'Expected to find root.tex in {dst_dir}')

    with open(root, 'r') as file:
        tex_source = file.read()

    tex_source = fuse_texs(dst_dir, tex_source)
    tex_source = move_figures(dst_dir, tex_source, ignored_imgnames)
    tex_source = add_arxiv_message(tex_source)

    with open(root, 'w') as file:
        file.write(tex_source)

    rm_dirs(dst_dir)

    out_archive = f'{dst_dir.name}.tar.gz'
    os.system(
        f'cd {dst_dir} && pdflatex root.tex && biber root && pdflatex root.tex && arxiv-collector root.tex && mv arxiv.tar.gz {out_archive}')


if __name__ == '__main__':
    main()
