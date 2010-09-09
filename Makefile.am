AUTOMAKE_OPTIONS = foreign

if MAKE_DESKTOP_ENTRY
applicationsdir = $(datadir)/applications
applications_DATA = hdapsicon.desktop
endif

pixmapdir = $(datadir)/pixmaps
pixmap_DATA = hdapsicon-error.svg  hdapsicon-logo.svg  hdapsicon-paused.svg

bin_SCRIPTS = hdapsicon
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = hdapsicon.py ${applications_DATA} ${pixmap_DATA}

hdapsicon: hdapsicon.py
	$(SED) \
		-e 's|@pixmapdir[@]|$(pixmapdir)|g' \
		-e 's|@VERSION[@]|$(VERSION)|g' \
		-e 's|@PYTHON[@]|$(PYTHON)|g' \
	   <hdapsicon.py >hdapsicon
