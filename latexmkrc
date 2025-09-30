# latexmkrc for one-command builds
$pdf_mode = 1;          # generate pdf
$interaction = 'nonstopmode';
$bibtex_use = 1;        # run bibtex automatically
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error %O %S';
