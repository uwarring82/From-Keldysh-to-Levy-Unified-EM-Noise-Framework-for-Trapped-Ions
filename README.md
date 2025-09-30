# From Keldysh to Lévy: Unified EM Noise Framework for Trapped Ions

This repository contains the LaTeX source for our note deriving a 
unified open-system description of ion heating. The framework bridges 
Gaussian field noise and discrete collision events via the 
Lévy–Khintchine generator obtained from the Keldysh formalism.

## Compile

To build the PDF locally:

```bash
latexmk -pdf main.tex
```

or manually:

```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Structure
•main.tex – master file, includes all sections
•introduction.tex – motivation and background
•theory_sections.tex – Keldysh → Lévy derivation
•discriminants_table.tex – observable discriminants
•scattering_formulas.tex – representative scattering models
•spatial_coherence.tex – trajectory coherence effects
•inference_protocol.tex – inference guide
•refs.bib – references
•figures/ – TikZ diagrams or generated plots

Figures

All diagrams are drawn in TikZ (em_mediation_diagram.tex,
trajectory_coherence_diagram.tex).
Future plots (e.g. PSDs, Allan variance curves) should go into /figures.

Versioning
•v0.1 – theory draft only
•v0.2 – added experimental sections
•v1.0 – polished for circulation / arXiv
