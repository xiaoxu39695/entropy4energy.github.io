.EXTRA_PREREQS=Makefile

# Directories
SRCDIR=src
BLDDIR=dist
CSSSRC=$(SRCDIR)/css
CSSBLD=$(BLDDIR)/css
JSSRC=$(SRCDIR)/js
JSBLD=$(BLDDIR)/js
NODEBIN=./node_modules/.bin

# HTML minifier
HTMLC=$(NODEBIN)/html-minifier-terser
HTMLCFLAGS=--collapse-whitespace --collapse-inline-tag-whitespace \
	--remove-comments --conservative-collapse --remove-optional-tags \
	--remove-empty-attributes --remove-redundant-attributes \
	--remove-script-type-attributes --use-short-doctype

# CSS stylesheet minifier flags
SASS=$(NODEBIN)/sass
SSC=$(NODEBIN)/postcss
SSCFLAGS=-u cssnano -u autoprefixer --no-map

# JavaScript compiler
JSC=i$(NODEBIN)/google-closure-compiler
JSCFLAGS=-O ADVANCED #--language_out ECMASCRIPT5_STRICT  # uncomment for IE

RSYNCFLAGS=-a --delete --prune-empty-dirs

.PHONY: all clean realclean html css js

all: html css js media

html:
	npm install html-minifier-terser

css: css-static $(CSSBLD)/main.css

$(CSSBLD)/main.css: $(CSSSRC)/main.scss
	npm install sass postcss-cli autoprefixer cssnano
	@mkdir -p $(@D)
	$(SASS) $< | $(SSC) $(SSCFLAGS) -o $@

css-static: $(CSSBLD)/academicons-1.9.1

$(CSSBLD)/%:
	@mkdir -p $(@D)
	rsync $(RSYNCFLAGS) $(@:$(BLDDIR)/%=$(SRCDIR)/%) $(CSSBLD)/

js:
	npm install google-closure-compiler

media:
	rsync $(RSYNCFLAGS) $(DISTDIR)/$@ $(BUILDDIR)/$@ 

clean:
	-rm -rf $(BUILDDIR)

realclean:
	-rm -rf node_modules $(BUILDDIR)
