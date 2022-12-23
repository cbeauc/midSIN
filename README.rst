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

The simplest way to use midSIN is via its `website application <https://midsin.roadcake.org>`_. If you prefer to use it locally on your own computer, follow the Installation instructions.


Installation
------------

To get the code (with git)

	$ git clone https://github.com/cbeauc/midSIN.git

To configure and install do

	$ cd midSIN

	$ python setup.py install --prefix=/home/username/local

You will need to make sure the path chosen as your prefix (e.g. ``/home/username/local``) for the installation location is in your ``PYTHONPATH`` environment variable, which should be different from the path where you ``git clone`` the source code. This would be something like:

	$ export PYTHONPATH="${HOME}/local/lib/python3.9/site-packages:${PYTHONPATH}"

If you plan to use the web interface ``midsin_web`` rather than the command-line interface ``midsin``, you also need to:

1. Set the ``MIDSIN_WEB_PATH`` environment variable to the installed path of your midSIN ``web`` directory. This would be something like:

	$ export MIDSIN_WEB_PATH="${HOME}/local/lib/python3.9/site-packages/midsin/web"

2. Type ``midsin_web migrate`` at the command-line once after a fresh installation. You will see a warning message like ``**WARNING**: Using insecure key. Fine if running midsin_web locally.`` You can safely ignore this if you are running ``midsin_web`` locally on your own computer, as opposed to serving it publicly on an intra/internet.

Local usage
~~~~~~~~~~~

If you want to use midSIN as a website application, type ``midsin_web runserver`` in a terminal which will launch the local web server at ``http://127.0.0.1:8000/``. You can just point your browser to this URL and you're ready to go. You will keep seeing the warning about insecure key, but you can safely ignore it.

If you want to use midSIN as a command-line application, type ``midsin [mytemplate.csv]`` where ``[mytemplate.csv]`` should be the path and name of your midSIN template file containing one or more sample outcomes. You can download the example template file ``midsin_batch.csv`` from `midSIN's website <https://midsin.roadcake.org/batch>`_, which also provides information on the template formatting.


Attribution
-----------

If you make use of this code, make sure to cite our paper.

The BibTeX entry is::

	@MISC{midSIN,
		AUTHOR = "Daniel Cresta and Donald C. Warren and Christian Quirouette and Amanda P. Smith and Lindey C. Lane and Amber M. Smith and Catherine A. A. Beauchemin",
		TITLE = "Time to revisit the endpoint dilution assay and to replace the {TCID}$_{50}$ as a measure of a virus sample's infection concentration",
    	JOURNAL = "PLOS Comput. Biol.",
		VOLUME = "17",
		NUMBER = "10",
		MONTH = "October",
		YEAR = "2021",
		PAGES = "e1009480",
		DOI = "10.1371/journal.pcbi.1009480",
		URL = "https://midsin.roadcake.org",
	}


License
-------

midSIN is free software made available under the GNU General Public License Version 3. For details see the LICENSE file.
