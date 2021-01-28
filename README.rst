midSIN
=======

**Measures the concentration of specific infections (SIN) in a virus sample based on an endpoint dilution (TCID50) assay**

.. image:: https://img.shields.io/badge/GitHub-cbeauc%2FmidSIN-blue.svg?style=flat
    :target: https://github.com/cbeauc/midSIN
.. image:: https://img.shields.io/badge/license-GPL-blue.svg?style=flat
    :target: https://github.com/cbeauc/midSIN/blob/master/LICENSE


The name midSIN stands for **m**\ easure of **i**\ nfectious **d**\ ose in **SIN**\ . The SIN concentration of a virus sample corresponds to the number of infection the sample will cause per unit volume. The SIN concentration is computed using Bayesian-inference based on the outcome of an endpoint dilution (or TCID50) assay. midSIN replaces the Reed-Munch and Spearman-Kärber methods to compute a virus sample's infectivity from an endpoint dilution (TCID50) assay. midSIN's outputs, the SIN concentration, replaces the TCID50 concentration as a measure of a virus sample's infectivity.


Usage
-----

The simplest way to use midSIN is via its `website application <https://midSIN.physics.ryerson.ca>`_. If you prefer to use it locally on your own computer, follow the Installation instructions.


Installation
------------

To get the repo (with git)

	$ git clone https://github.com/cbeauc/midSIN.git

To configure and install do

	$ cd midSIN

	$ python setup.py install --prefix=/home/username/local

You will need to make sure the path chosen as your prefix (e.g. ``/home/username/local``) for the installation location is in your ``PYTHONPATH`` environment variable, and that it is different from the path where you ``git clone`` the source code. If you plan to use the web interface ``midsin_web`` rather than the command-line interface ``midsin``, you also need to:

1. set the ``MIDSIN_WEB_PATH`` environment variable to the location of the installed path of your midSIN ``web`` directory.

2. type ``midsin_web migrate`` at the command-line once after a fresh installation.

Local usage
~~~~~~~~~~~

If you want to use midSIN as a website application, type ``midsin_web runserver`` in a terminal which will launch the local web server at ``http://127.0.0.1:8000/``. You can just point your browser to this URL and you're ready to go.

If you want to use midSIN as a command-line application, type ``midsin [mytemplate.csv]`` where ``[mytemplate.csv]`` should be the path and name of your midSIN template file containing one or more sample outcomes. You can download the example template file ``midsin_batch.csv`` from `midSIN's website <https://midsin.physics.ryerson.ca/batch>`_, which also provides information on the template formatting.


Attribution
-----------

If you make use of this code, make sure to cite it.

The BibTeX entry is::

	@MISC{midSIN,
		AUTHOR = "Daniel Cresta and Donald C. Warren and Christian Quirouette and Amanda P. Smith and Lindey C. Lane and Amber M. Smith and Catherine A. A. Beauchemin",
		TITLE = "Time to revisit the endpoint dilution assay and to replace {TCID}$_{50}$ and {PFU} as measures of a virus sample's infection concentration",
		MONTH = "January",
		YEAR = "2021",
		EPRINT = "2101.11526",
		ARCHIVEPREFIX = "arXiv",
		PRIMARYCLASS = "q-bio.QM",
		URL = "https://midSIN.physics.ryerson.ca"
	}


License
-------

midSIN is free software made available under the GNU General Public License Version 3. For details see the LICENSE file.
