AC_PREREQ(2.65)
AC_INIT(hdapsicon, 0.3, thomas.pani@gmail.com)
AC_PROG_SED
AC_ARG_ENABLE([desktop],
			  [  --enable-desktop    Create a desktop entry],
			  [case "${enableval}" in
			    yes) desktop=true ;;
				no)  desktop=false ;;
				*) AC_MSG_ERROR([bad value ${enableval} for --enable-desktop]) ;;
			   esac],[desktop=false])
AM_CONDITIONAL([MAKE_DESKTOP_ENTRY], [test x$desktop = xtrue])
AM_INIT_AUTOMAKE(hdapsicon, 0.3)
AM_PATH_PYTHON
AC_OUTPUT(Makefile)
