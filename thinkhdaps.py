#!@PYTHON@
# Copyright (c) 2008-2009  Thomas Pani <thomas.pani@gmail.com>
# based on an awn applet Copyright (c) 2008  onox <denkpadje@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import errno
import os
import platform
import sys

import pygtk
pygtk.require("2.0")
import gnome
import gobject
import gtk
import gtk.gdk


__version__ = '@VERSION@'


# Interval in milliseconds between two successive status checks.
CHECK_STATUS_INTERVAL = 250
# The sysfs mountpoint.
SYSDIR = '/sys'
# Check whether we're using /sys/block/%s/device/unload_heads (>=2.6.28)
# or /sys/block/%s/queue/protect (<=2.6.27).
# Native kernel interface measures in milliseconds, HDAPS in seconds.
PROTECT_FACTOR = 1
if '2.6.27' <= platform.release():
    PROTECT_FACTOR = 1000

# Images used as the applet's icon to reflect the current status of HDAPS.
IMAGE_DIR = '@pkgdatadir@'
icon_running = gtk.gdk.pixbuf_new_from_file(
        os.path.join(IMAGE_DIR, "thinkhdaps-logo.svg"))
icon_paused = gtk.gdk.pixbuf_new_from_file(
        os.path.join(IMAGE_DIR, "thinkhdaps-paused.svg"))
icon_error = gtk.gdk.pixbuf_new_from_file(
        os.path.join(IMAGE_DIR, "thinkhdaps-error.svg"))

def get_protect_file(device):
    """Returns the protect file based on the PROTECT_FACTOR."""
    if PROTECT_FACTOR != 1:
        return os.path.join(SYSDIR, 'block', device, 'device/unload_heads')
    else:
        return os.path.join(SYSDIR, 'block', device, 'queue/protect')

class ThinkHDAPSAboutDialog(gtk.AboutDialog):
    """ThinkHDAPS's AboutDialog."""

    def __init__(self):
        gtk.AboutDialog.__init__(self)
        self.set_icon(icon_running)

        self.set_authors(('Thomas Pani <thomas.pani@gmail.com>',))
        self.set_copyright(u'Copyright \u00a9 2008  Thomas Pani')
        self.set_logo(icon_running)
        self.set_name('ThinkHDAPS')
        self.set_version(__version__)
        self.set_license('''This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.''')
        self.set_wrap_license(True)
        self.set_website('http://pani.webhop.org/thinkhdaps.html')


class ThinkHDAPSApplet(gtk.StatusIcon):
    """StatusIcon that shows the status of HDAPS."""
    
    def __init__(self):
        gtk.StatusIcon.__init__(self)

        # context menu
        menu = gtk.Menu()
        menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menuItem.connect('activate', self.about_cb)
        menu.append(menuItem)
        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menuItem.connect('activate', self.quit_cb)
        menu.append(menuItem)

        self.connect('popup-menu', self.popup_menu_cb, menu)
        
        # status
        self.paused = None
        self.was_paused = None

        # initialize
        self.check_status_cb()
        
        gobject.timeout_add(CHECK_STATUS_INTERVAL, self.check_status_cb)

    def about_cb(self, widget, data=None):
        dlg = ThinkHDAPSAboutDialog()
        dlg.run()
        dlg.destroy()

    def quit_cb(self, widget, data=None):
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data=None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)

    def check_status_cb(self):
        """Check the status the hard disk monitored by HDAPS and change
        the applet's icon if necessary.
        """

        self.was_paused = self.paused
        self.paused = {}

        # Find HDAPS devices.
        # Check if and for how long the devices are unloaded.
        for device in os.listdir(os.path.join(SYSDIR, 'block')):
            self.paused[device] = None
            protect_file = get_protect_file(device)
            if os.path.isfile(protect_file):
                try:
                    f = open(protect_file, 'r')
                    self.paused[device] = \
                        float(f.readline()) / PROTECT_FACTOR
                except IOError, e:
                    if e.errno == errno.EOPNOTSUPP:
                        # device does not support the unload feature.
                        pass
                    else:
                        # report other errors.
                        self.paused[device] = -1
                        print >> sys.stderr, "Error reading %s: %s" % \
                            (protect_file, e.strerror)

        # Change icon and tooltip if status has changed.
        if self.paused != self.was_paused:
            tt_text = ""
            min_unload_time = min(self.paused.values())
            max_unload_time = max(self.paused.values())

            if max_unload_time is None:
                # No device supports HDAPS.
                self.set_from_pixbuf(icon_error)
                self.set_tooltip('\n'.join((
                    "HDAPS disabled",
                    "Can't find a device that supports HDAPS!",
                    "Probed devices: %s" % ' '.join(self.paused.keys())
                    ))
                    )

            elif max_unload_time == -1:
                # All devices threw errors while reading protect file.
                self.set_from_pixbuf(icon_error)
                self.set_tooltip('\n'.join((
                    "HDAPS disabled",
                    "Errors fetching HDAPS state on all devices!",
                    "Probed devices: %s" % ' '.join(self.paused.keys())
                    ))
                    )

            elif max_unload_time >= 0:
                # At least one device running.

                if min_unload_time == -1:
                    # One or more devices threw errors.
                    self.set_from_pixbuf(icon_error)
                elif max_unload_time > 0:
                    self.set_from_pixbuf(icon_paused)
                else:
                    self.set_from_pixbuf(icon_running)

                tt_text = "HDAPS enabled"
                for device in self.paused:
                    status = self.paused[device]
                    status_text = ""
                    if status == -1:
                        status_text = "error reading protect file"
                    elif status is None:
                        continue    # ignore devices that don't support HDAPS.
                    elif status == 0:
                        status_text = "running"
                    else:
                        status_text = "Parked (%.3fs remaining)" % \
                            self.paused[device]
                    tt_text += "\n%s: %s" % (device, str(status_text))
                self.set_tooltip(tt_text)

            else:
                assert False

        return True


def on_launch_browser_mailer(dialog, link, user_data=None):
    if user_data == 'mail':
        gnome.url_show('mailto:'+link)
    else:
        gnome.url_show(link)


if __name__ == "__main__":
    try:
        gtk.about_dialog_set_email_hook(on_launch_browser_mailer, 'mail')
        gtk.about_dialog_set_url_hook(on_launch_browser_mailer, 'url')

        hdaps_icon = ThinkHDAPSApplet()
        gtk.main()
    except KeyboardInterrupt:
        pass

