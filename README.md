# arxiv_tool

Some tools for working with arXiv papers.

## Installation

Install the requirements of `arxiv-collector`: [arxiv-collector · PyPI](https://pypi.org/project/arxiv-collector/#requirements)

Install the requirements of `arxiv_tools`:

```bash
pip install -r requirements.txt
```

## Usage
1. Copy the sources of the paper in the `data/` directory.
2. Run `python arxiv_tools.py data/paper data/output_paper` to generate the submission files in the `data/output_paper` directory.
3. Upload the files to arXiv.

## Future features
- [ ] Directly clone the sources from GitHub
- [ ] Support more cases (nested folders, etc.)

## References
- [How to publish your preprints on Arxiv • Northern Robotics Laboratory](https://norlab.ulaval.ca/research/publish-prepints-arxiv/)
