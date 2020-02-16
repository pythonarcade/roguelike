Building and Deployment
=======================

.. _requirements:

Requirements
------------

* ``/requirements.txt`` This should be a simple list of every package required
  to *develop* your project. The packages required to *run* the project go in
  setup.py. This file makes it easy for automatic setup of virtual environment,
  and automated builds.
* Python programs often use a virtual environment in a folder (usually named venv).
  Python has a lot of other tools like pipenv and more trying to solve this same
  problem. Last year, PEP 582 was approved that will use a ``__pypackages__`` directory
  that, if it exists, will be used instead of global packages.

Setup
-----

* ``/setup.py`` This is one of the two required files.
  You can use the setup file to build the project. For more info,
  refer back to :ref:`core`.

.. _make:

Make File
---------

* ``/make.bat``, ``make.sh``, ``make.py`` There are so many different commands for building, testing,
  and deployment, I like having a "make" file with a instructions to make the process easier.

Build Directory
---------------

* ``/build/`` This is automatically created by setup.py when you build.

Distribution Directory
----------------------

* ``/dist/`` This is automatically created by setup.py when we build wheels.

Additional Build Info
---------------------
* The command to build your project is ``python setup.py build``
* bdist / wheels - If you have the `wheel package`_ installed, you can create a
  one-file distribution of your project. If the project is pure Python, that wheel
  can work on any platform. If you've got platform-specific libraries, you can
  make wheels for each platform. See Python's `packaging projects`_ for more info.
  The command to create a wheel is ``python setup.py bdist_wheel``. This only works
  if you have the wheel package installed.
* Manifest: https://packaging.python.org/guides/using-manifest-in/
* Twine - Once your project is packaged in a wheel,
  you can upload it to the PyPi repository for other people to use.
  This is done with the twine_ module. It is simple as:

.. code-block:: text

    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

* AWS - If you deploy on your own server, Amazon Web Services has a great Python-based command-line
  interface as part of the `awscli package`_.

.. _packaging projects: https://packaging.python.org/tutorials/packaging-projects/
.. _twine: https://github.com/pypa/twine
.. _wheel package: https://wheel.readthedocs.io/en/stable/
.. _awscli package: https://aws.amazon.com/cli/
