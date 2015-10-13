#! /usr/bin/env python
#
# Create 'a' which depends on 'b(2.0)'.
# create 'b' in versions 1.0, 2.0, and 3.0.
#
# Install 'a' and check that 'b(2.0)' is installed.
#
# Try to upgrade 'b' to version 3.0 and check that it fails.
#
# Try to downgrade 'b' to version 1.0 and check that it fails.
#

import os
import opk, cfg, opkgcl

opk.regress_init()

o = opk.OpkGroup()

o.add(Package="a", Depends="b (= 2.0)")
o.add(Package="b", Version="1.0")
o.add(Package="b", Version="2.0")
o.add(Package="b", Version="3.0")

o.write_opk()
o.write_list()

opkgcl.update()

# install a and check that b(2.0) is installed
opkgcl.install("a")
if not opkgcl.is_installed("a"):
    opk.fail("Package 'a' installed but reports as not installed.")
if opkgcl.is_installed("b", "3.0"):
    opk.fail("Package 'a' depends on 'b(2.0)', but 'b(3.0)' installed.")
if opkgcl.is_installed("b", "1.0"):
    opk.fail("Package 'a' depends on 'b(2.0)', but 'b(1.0)' installed.")
if not opkgcl.is_installed("b", "2.0"):
    opk.fail("Package 'a' depends on 'b(2.0)', but 'b(2.0)' not installed.")

# try installing b(3.0) which should fail
opkgcl.install("b_3.0_all.opk")
if not opkgcl.is_installed("a"):
    opk.fail("Package 'a' was removed.")
if opkgcl.is_installed("b", "3.0"):
    opk.fail("Package 'a' depends on 'b(2.0)', but 'b' upgraded to 3.0.")
if opkgcl.is_installed("b", "1.0"):
    opkg.fail("Install called on 'b(3.0)' but 'b' downgraded to 1.0.")
if not opkgcl.is_installed("b", "2.0"):
    opk.fail("Package 'a' depends on 'b(2.0)', but 'b(2.0)' removed.")

# try forcing a downgrade to b(1.0) which should fail
opkgcl.install("b_1.0_all.opk","--force-downgrade")
if not opkgcl.is_installed("a"):
    opk.fail("Package 'a' was removed.")
if opkgcl.is_installed("b", "3.0"):
    opk.fail("Install called on 'b(1.0)' with --force-downgrade but 'b(3.0)' installed.")
if opkgcl.is_installed("b", "1.0"):
    opk.fail("Package 'a' depends on 'b(2.0)', but 'b' downgraded to 1.0.")
if not opkgcl.is_installed("b", "2.0"):
    opkg.fail("Package 'a' depends on 'b(2.0)', but 'b(2.0)' removed.")
