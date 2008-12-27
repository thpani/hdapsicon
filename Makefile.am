AUTOMAKE_OPTIONS = foreign

bin_SCRIPTS = thinkhdaps
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = thinkhdaps.py

pixmapsdir = $(datadir)/@PACKAGE@
dist_pixmaps_DATA = thinkhdaps-error.svg  thinkhdaps-logo.svg  thinkhdaps-paused.svg

thinkhdaps: thinkhdaps.py
	$(SED) \
		-e 's|@pkgdatadir[@]|$(pkgdatadir)|g' \
		-e 's|@VERSION[@]|$(VERSION)|g' \
		-e 's|@PYTHON[@]|$(PYTHON)|g' \
	   <thinkhdaps.py >thinkhdaps
