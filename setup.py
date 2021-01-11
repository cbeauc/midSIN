# Copyright (C) 2020-2021 Catherine Beauchemin
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
	name = 'midsin',
	version = '0.1',
	author = 'Catherine Beauchemin et al (See AUTHORS)',
	author_email = 'cbeau@users.sourceforge.net',
	url = 'https://github.com/cbeauc/midsin',
	license = 'See LICENSE file',
	description = 'Measures the specific infection (SIN) concentration of a virus sample based on an endpoint dilution (TCID50) assay.',
	long_description = open("README.rst").read(),
	package_data = {"": ["LICENSE"]},
	packages = [
		'midsin',
	],
	scripts = [
		'bin/midsin',
	],
	package_dir = {'midsin':'lib'}
)
