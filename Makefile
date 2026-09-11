# Compilation de master_thesis
#
# Le TEXINPUTS ci-dessous fait passer cls_local/ AVANT la racine du dépôt :
# la copie corrigée de dms.cls y est donc trouvée en premier, tandis que
# l'original du département reste intact à la racine. Voir l'en-tête de
# cls_local/dms.cls pour le détail de la correction.
#
# Le « : » final est obligatoire : il conserve les chemins par défaut de TeX.

TEX      := lualatex
FLAGS    := -interaction=nonstopmode
MAIN     := master_thesis
TEXINPUTS_LOCAL := cls_local:

.PHONY: all clean distclean check

all:
	TEXINPUTS="$(TEXINPUTS_LOCAL)" $(TEX) $(FLAGS) $(MAIN).tex
	biber $(MAIN)
	TEXINPUTS="$(TEXINPUTS_LOCAL)" $(TEX) $(FLAGS) $(MAIN).tex
	TEXINPUTS="$(TEXINPUTS_LOCAL)" $(TEX) $(FLAGS) $(MAIN).tex

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
