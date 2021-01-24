midSIN
=======

**Measures the concentration of specific infections (SIN) in a virus sample based on an endpoint dilution (TCID50) assay**

.. image:: https://img.shields.io/badge/GitHub-cbeauc%2FmidSIN-blue.svg?style=flat
    :target: https://github.com/cbeauc/midSIN
.. image:: https://img.shields.io/badge/license-GPL-blue.svg?style=flat
    :target: https://github.com/cbeauc/midSIN/blob/master/LICENSE


The name midSIN stands for **m**\ easure of **i**\ nfectious **d**\ ose in **SIN**\ . The SIN concentration of a virus sample corresponds to the number of infection the sample will cause per unit volume. The SIN concentration is computed using Bayesian-inference based on the outcome of an endpoint dilution (or TCID50) assay. midSIN replaces the Reed-Munch and Spearman-Karber methods to compute a virus sample's infectivity from an endpoint dilution (TCID50) assay. midSIN's outputs, the SIN concentration, replaces the TCID50 concentration as a measure of a virus sample's infectivity.


Installation
------------

To get the repo (with git)

	$ git clone https://github.com/cbeauc/midSIN.git

To configure and install do

	$ cd midSIN

	$ python setup.py install --prefix=/home/username/local/

If you plan to use the web interface ``midsin_web`` rather than the command-line interface ``midsin``, you also need to:
1. set the ``MIDSIN_WEB_PATH`` environment variable to the location of the installed path of your midSIN ``web`` directory.
2. type ``midsin_web migrate`` at the command-line.


Attribution
-----------

If you make use of this code, make sure to cite it.

The BibTeX entry is::

	@MANUAL{midSIN,
		AUTHOR = "Catherine A. A. Beauchemin and Donald C. Warren and Daniel Cresta and Christian Quirouette",
		TITLE = "{midSIN} measures a virus sample's infectious dose in {SIN}",
		YEAR = "2020",
		PUBLISHER = "{GitHub}",
		JOURNAL = "{GitHub} repository",
		HOWPUBLISHED = "\url{https://github.com/cbeauc/midSIN}"
	}


License
-------

midSIN is free software made available under the GNU General Public License Version 3. For details see the LICENSE file.
