# ABCD Dataset PFN Sex Differences Replication Project

Fork of [ashleychari/abcd_sex_pfn_replication](https://github.com/ashleychari/abcd_sex_pfn_replication). The original method and figure walkthrough is at [https://ashleychari.github.io/abcd_sex_pfn_replication/](https://ashleychari.github.io/abcd_sex_pfn_replication/).

From Part 3 on, this version differs from those instructions:
- Only code is tracked by git. Data lives in `inputs/`, `reference_files/` and `results/` inside the clone, which git ignores; their locations are set in `CONFIG.txt`.
- All file paths come from `CONFIG.txt`; don't edit paths inside the scripts. Set `CODE_DIR` at the top of `CONFIG.txt`.
- Jobs run on SLURM. `cd` into the repo before running `sbatch`, because the job scripts read `CONFIG.txt` from the folder you submit from. Scripts run from the repo; nothing is copied into `dropbox/`.
- The univariate GAMs model `oSex * binarizedACE` and save sex, ACE and sex × ACE results. `binarizedACE` (0/1) is read from the ACE csv set by `ACE_CSV` in `CONFIG.txt` (baseline rows, matched on subject ID).
- `bash setup_env.sh` creates the `ace` conda environment (Python libraries, `wb_command`, R and R packages); the SLURM job scripts activate it.
- `bash download_reference_files.sh` downloads the medial-wall masks and the fsaverage5 resampling files into `reference_files/`.
