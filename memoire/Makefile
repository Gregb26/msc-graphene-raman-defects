TEX      := lualatex
FLAGS    := -interaction=nonstopmode
MAIN     := master_thesis


.PHONY: all clean distclean check

# Renommer une étiquette invalide les .aux/.out ; LaTeX échoue alors en
# relisant les anciens (« Undefined control sequence » sur r@chap:...).
# Passer par « make clean all » après toute modification d'étiquette.
clean:
	find . \( -name '*.aux' -o -name '*.out' -o -name '*.toc' -o -name '*.lof' \
	       -o -name '*.lot' -o -name '*.bbl' -o -name '*.bcf' -o -name '*.blg' \
	       -o -name '*.run.xml' -o -name '*.fls' -o -name '*.fdb_latexmk' \) -delete

distclean: clean
	rm -f $(MAIN).log $(MAIN).synctex.gz

# Erreurs et débordements > 10 pt
check:
	@grep -c '^!' $(MAIN).log | sed 's/^/erreurs : /'
	@grep -o 'Overfull \\hbox ([0-9.]*pt' $(MAIN).log \
	  | sed 's/[^0-9.]//g' | awk '$$1>10' | wc -l | sed 's/^/Overfull > 10 pt : /'
