AUTOMAKE_OPTIONS = foreign

if MAKE_DESKTOP_ENTRY
applicationsdir = $(datadir)/applications
applications_DATA = thinkhdaps.desktop
endif

pixmapdir = $(datadir)/pixmaps
pixmap_DATA = thinkhdaps-error.svg  thinkhdaps-logo.svg  thinkhdaps-paused.svg

bin_SCRIPTS = thinkhdaps
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = thinkhdaps.py ${applications_DATA} ${pixmap_DATA}

thinkhdaps: thinkhdaps.py
	$(SED) \
		-e 's|@pixmapdir[@]|$(pixmapdir)|g' \
		-e 's|@VERSION[@]|$(VERSION)|g' \
		-e 's|@PYTHON[@]|$(PYTHON)|g' \
	   <thinkhdaps.py >thinkhdaps
