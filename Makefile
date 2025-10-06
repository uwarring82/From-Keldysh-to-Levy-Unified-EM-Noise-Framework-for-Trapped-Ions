PDF=main.pdf
TEX=main.tex

all: pdf

pdf:
	latexmk -pdf -halt-on-error -interaction=nonstopmode $(TEX)

clean:
	latexmk -C

arxiv:
	mkdir -p arxiv && git ls-files | grep -E '\\.(tex|bib)$|^figures/' | xargs -I{} cp --parents {} arxiv/
