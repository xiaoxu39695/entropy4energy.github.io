.EXTRA_PREREQS=Makefile

# Directories
SRCDIR=src
BUILDDIR=dist
NODEBIN=node_modules/.bin

# HTML minifier
HTMLC=html-minifier-terser
HTMLCFLAGS=--collapse-whitespace --collapse-inline-tag-whitespace \
	--remove-comments --conservative-collapse --remove-optional-tags \
	--remove-empty-attributes --remove-redundant-attributes \
	--remove-script-type-attributes --use-short-doctype

# CSS stylesheet minifier flags
SSC=postcss
SSCFLAGS=-u cssnano -u autoprefixer --no-map

# JavaScript compiler
JSC=google-closure-compiler
JSCFLAGS=-O ADVANCED #--language_out ECMASCRIPT5_STRICT  # uncomment for IE

RSYNCFLAGS=-a --delete --prune-empty-dirs

.PHONY: all clean realclean html css js

all: html css js media

html:
	npm install html-minifier-terser

css:
	npm install sass cssnano

js:
	npm install google-closure-compiler

media:
	rsync $(RSYNCFLAGS) $(DISTDIR)/$@ $(BUILDDIR)/$@ 

clean:
	-rm -rf $(BUILDDIR)

realclean:
	-rm -rf node_modules $(BUILDDIR)
