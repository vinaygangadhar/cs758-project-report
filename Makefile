.phony: prelim.pdf

prelim.pdf::
	pdflatex prelim
	bibtex prelim
	pdflatex prelim
	@find_repeated.py

clean:
	rm prelim.pdf
