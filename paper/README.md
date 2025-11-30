# Research Paper

This folder contains everything needed to write and submit your research paper.

## Files

- `main.tex` - Main paper (LaTeX format, ~8 pages)
- `references.bib` - Bibliography (add citations here)
- `literature_review_reading_list.md` - 20 papers to read
- `figures/` - Copy your visualizations here

## Status

- [ ] Run experiments 3x (use `run_experiments_multiple_trials.py`)
- [ ] Read 20 papers (see `literature_review_reading_list.md`)
- [ ] Fill in Related Work section
- [ ] Add all citations to `references.bib`
- [ ] Copy figures to `paper/figures/`
- [ ] Compile LaTeX and review
- [ ] Proofread and polish
- [ ] Submit!

## How to Compile

### Option 1: Overleaf (Recommended)
1. Go to https://www.overleaf.com
2. Create new project → Upload Project
3. Upload `main.tex` and `references.bib`
4. Compile (it will handle everything)

### Option 2: Local LaTeX
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Timeline

**Day 1:**
- Morning: Run `python run_experiments_multiple_trials.py` (2-3 hours)
- Afternoon: Start reading papers (4-5 papers)

**Day 2:**
- Morning: Continue reading papers (10-15 papers)
- Afternoon: Fill in Related Work section

**Day 3:**
- Morning: Complete paper draft
- Afternoon: Polish and proofread
- Evening: Submit!

## Paper Structure (Current)

1. **Abstract** ✅ (Done)
2. **Introduction** ⚠️ (Needs expansion)
3. **Related Work** ❌ (TODO: Fill after reading papers)
4. **Methodology** ✅ (Done)
5. **Experiments** ✅ (Done - update with multiple trials)
6. **Results** ✅ (Done)
7. **Discussion** ✅ (Done)
8. **Conclusion** ✅ (Done)

## What's Already Done

✅ Abstract with all key results  
✅ Methodology section  
✅ All 4 experiments documented  
✅ Results tables with your actual numbers  
✅ Statistical analysis (t-test, p-value, CI)  
✅ Ablation study  
✅ Failure analysis  
✅ Discussion of findings  
✅ Conclusion  

## What You Need to Do

1. **Run Multiple Trials** (2-3 hours)
   ```bash
   python run_experiments_multiple_trials.py
   ```
   Then update tables in `main.tex` with mean ± std

2. **Read Papers** (8-10 hours over 1-2 days)
   - Follow `literature_review_reading_list.md`
   - Start with "MUST READ" papers
   - Take notes on key findings

3. **Write Related Work** (2-3 hours)
   - Use your notes from reading
   - Cite 15-20 papers
   - Show how your work fits in

4. **Polish** (2-3 hours)
   - Proofread
   - Check all citations
   - Verify all numbers match your results

## Tips

- **Don't overthink Related Work** - Just summarize what others did and how yours is different
- **Use your actual numbers** - They're already in the template
- **Keep it concise** - Workshop papers are 6-8 pages
- **Focus on contributions** - What's novel about your work?

## Questions?

If you get stuck:
1. Check the LaTeX comments (marked with % TODO)
2. Look at similar papers for structure
3. Ask for help with specific sections
