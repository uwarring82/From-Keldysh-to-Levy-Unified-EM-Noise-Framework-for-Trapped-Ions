# From Keldysh to Lévy — Unified EM Noise Framework for Trapped Ions

This repository hosts the LaTeX source for our paper  
**“From Keldysh to Lévy: A Unified Framework for Electromagnetic Noise in Trapped Ions.”**

---

## 📘 Scope
The manuscript develops a cross-regime description of environmental noise affecting trapped ions,
bridging the Keldysh formalism with Lévy-type statistics.
It unifies **theory**, **scattering models**, and **inference protocols** into a coherent framework
for identifying noise sources and collision signatures in experiments.

---

## 🧠 Structure

```
sections/
  01_introduction.tex
  02_regimes_overview.tex
  03_theory_foundations.tex
  04_scattering_models.tex
  05_em_mediation.tex
  06_spatial_temporal_coherence.tex
  07_inference_protocol.tex
  08_discriminants_table.tex
  09_uncertainties_validation.tex
  10_conclusion_outlook.tex
figures/
bib/refs.bib
```

Each `.tex` file is an independent section, included by `main.tex`.

---

## 🛠️ Build Instructions

### Local build
Requires TeX Live or MiKTeX with `latexmk`.

```bash
git clone https://github.com/uwarring82/From-Keldysh-to-Levy-Unified-EM-Noise-Framework-for-Trapped-Ions.git
cd From-Keldysh-to-Levy-Unified-EM-Noise-Framework-for-Trapped-Ions
make pdf
```

Output: `main.pdf`

### Clean up

```
make clean
```

### Create arXiv bundle

```
make arxiv
```

---

## ⚙️ Continuous Integration

Each push or PR to main triggers GitHub Actions to compile the manuscript
and attach the resulting PDF as an artifact.
Status badge will appear here once merged:

![Build PDF](https://github.com/uwarring82/From-Keldysh-to-Levy-Unified-EM-Noise-Framework-for-Trapped-Ions/actions/workflows/latex.yml/badge.svg)

---

## 🧭 Guardian Tier

This repository follows the Guardian Integrity Model:
1. Negative controls (null channels)
2. Statistical rigor (power & identifiability)
3. Immutable archival (artifact hashes)
4. Cross-validation (alternate estimators)

All validation logic is documented in
`sections/09_uncertainties_validation.tex`.

---

## 📝 Terminology Policy

We use \emph{motional decoherence} as the umbrella term for any process that
reduces the purity of an ion’s motional state, encompassing both heating
(energy exchange driven by near-resonant force noise) and dephasing (phase
diffusion from slow potential variations). The explicit terms “heating” and
“dephasing” are retained when discussing spectral origins (e.g.\
$S_E(\omega_t)$ vs.\ low-frequency $S_{\delta\omega}$ or $S_E(0)$), the
structure of the master-equation generators ($\mathcal{D}_G$ vs.\
$\mathcal{J}_P$), or discriminants that isolate a single channel.

---

## 📄 License

MIT License – see `LICENSE`.
