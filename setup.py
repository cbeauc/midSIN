# Copyright (C) 2020-2022 Catherine Beauchemin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from distutils.core import setup

setup(
	name = "midsin",
	version = "0.2",
	author = "Catherine Beauchemin et al. (See AUTHORS)",
	author_email = "cbeau@users.sourceforge.net",
	url = "https://github.com/cbeauc/midSIN",
	license = "See LICENSE file",
	description = "Measures the specific infection (SIN) concentration of a virus sample based on an endpoint dilution (TCID50) assay.",
	long_description = open("README.rst").read(),
	packages = [
		"midsin",
		"midsin.web",
		"midsin.web.settings",
	],
	package_dir = {"midsin":"src"},
	package_data = {
		"": ["LICENSE"],
		"midsin.web": ["templates/*","static/*","settings/*"],
	},
	scripts = [
		"bin/midsin",
		"bin/midsin_web",
	],
	install_requires = [
		"matplotlib",
		"numpy",
		"scipy",
	],
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Framework :: Django",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Natural Language :: English",
		"Programming Language :: Python :: 3",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Scientific/Engineering :: Medical Science Apps.",
		"Topic :: Utilities",
	],
)
