.EXTRA_PREREQS=Makefile

# Directories
SRCDIR=src
BLDDIR=dist
CSSSRC=$(SRCDIR)/css
CSSBLD=$(BLDDIR)/css
JSSRC=$(SRCDIR)/js
JSBLD=$(BLDDIR)/js
NODEDIR=node_modules
NODEBIN=$(NODEDIR)/.bin

# HTML minifier
HTMLC=$(NODEBIN)/html-minifier-terser
HTMLCFLAGS=--collapse-whitespace --collapse-inline-tag-whitespace \
	--remove-comments --conservative-collapse --remove-optional-tags \
	--remove-empty-attributes --remove-redundant-attributes \
	--remove-script-type-attributes --use-short-doctype

# CSS stylesheet minifier flags
SASS=./$(NODEBIN)/sass
SSC=./$(NODEBIN)/postcss
SSCFLAGS=-u cssnano -u autoprefixer --no-map

# JavaScript compiler
JSC=./$(NODEBIN)/google-closure-compiler
JSCFLAGS=-O ADVANCED #--language_out ECMASCRIPT5_STRICT  # uncomment for IE

# rsync
RSYNCFLAGS=-a --delete --prune-empty-dirs
RSYNC=rsync $(RSYNCFLAGS)

# npm
NPMINST=npm install

.PHONY: all clean realclean html css js

all: html css js media

# HTML targets
html: html-install

html-install: $(NODEDIR)/html-minifier-terser

# CSS targets
css: css-static css-compiled

css-compiled: css-install $(CSSBLD)/main.css

css-install: $(NODEDIR)/sass $(NODEDIR)/postcss-cli $(NODEDIR)/autoprefixer $(NODEDIR)/cssnano

$(CSSBLD)/main.css: $(CSSSRC)/main.scss
	@mkdir -p $(@D)
	$(SASS) $< | $(SSC) $(SSCFLAGS) -o $@

css-static: $(CSSBLD)/academicons-1.9.1

$(CSSBLD)/%:
	@mkdir -p $(@D)
	$(RSYNC) $(@:$(BLDDIR)/%=$(SRCDIR)/%) $(CSSBLD)/

# JavaScript
js: js-install $(JSBLD)/slideshow.js

js-install: $(NODEDIR)/google-closure-compiler

$(JSBLD)/slideshow.js: $(JSSRC)/slideshow.js
	$(JSC) $(JSCFLAGS) --js $^ --js_output_file $@

# Static targets
media:
	$(RSYNC) $(SRCDIR)/$@ $(BLDDIR)/$@/

# General targets
$(NODEDIR)/%:
	test -d $@ || $(NPMINST) $(@:$(NODEDIR)/%=%)

clean:
	-rm -rf $(BLDDIR)

realclean: clean
	-rm -rf $(NODEDIR)
