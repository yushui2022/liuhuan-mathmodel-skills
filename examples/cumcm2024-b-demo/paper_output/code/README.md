# Current Contest Code Workspace

This directory is for code generated or modified for the current contest problem.

The skill package `scripts/` directories are reusable templates and code-level prompts. Do not write contest-specific scripts back into installed skill package directories.

## Subdirectories

```text
paper_output/code/
├── data_processing/   # cleaning, feature engineering, field mapping, dataset joins
├── visualization/     # paper-ready plotting scripts and figure/table formatting scripts
├── modeling/          # q1/q2/q3 modeling scripts and result contract writers
└── qa/                # optional contest-specific validation/check scripts
```

Generated code should read from `problem_files/`, `crawled_data/`, `paper_output/plan/`, and `paper_output/data_cleaned/`, then write outputs back to `paper_output/data_cleaned/`, `paper_output/figures/`, `paper_output/tables/`, and `paper_output/results/`.
