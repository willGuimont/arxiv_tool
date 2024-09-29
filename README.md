# arxiv_tool

Some tools for working with arXiv papers.

## Installation

Install the requirements of
`arxiv-collector`: [arxiv-collector · PyPI](https://pypi.org/project/arxiv-collector/#requirements)

Install `arxiv_tool`:

```bash
pip install arxiv_tool
```

## Usage

1. Copy the sources of the paper in a directory, e.g., `paper_src/`.
2. Run `python arxiv_tool.py paper_src paper_out` to generate the submission files in the `paper_out`
   directory.
3. Upload the files to arXiv.

All the available options can be found by running `arxiv_tool --help`.

## Development

Install the requirements:

```bash
pip install -r requirements.txt
```

## Future features

- [ ] Directly clone the sources from GitHub
- [ ] Support more cases (nested folders, etc.)

## References

- [How to publish your preprints on Arxiv • Northern Robotics Laboratory](https://norlab.ulaval.ca/research/publish-prepints-arxiv/)
