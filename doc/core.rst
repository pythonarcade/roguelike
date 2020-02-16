.. _core:

Core Files and Directories
==========================

There are only two required files, and one required directory:

* ``/pypi_package_example/`` This is the main project directory
  where all the Python source code goes.
  The directory should be named the same as your package name. Check the
  `PyPi Package Index`_ to make sure there isn't a conflict before picking
  your package name.
* ``/pypi_package_example/__init__.py`` This is the starting file for your
  project. It is run when you import your package. It should not do much
  processing, it should just load in all the functions and classes that you
  plan on using in your project.

.. _setup:

Setup File
----------

* ``/setup.py`` or ``/setup.cgf``. This specifies how your project is to be built, and other
  meta information about the project. The ``/setup.py`` seems more common based on my
  limited experience, but in 2016 `PEP 518`_ was provisionally accepted which specifies a different
  setup method, to be stored in a file called ``setup.cfg``.

.. _PEP 518: https://www.python.org/dev/peps/pep-0518/

Setup File In Detail
--------------------
When you run setup.py, you can get a full list of commands:

.. code-block:: text
    :caption: setup.py options

    (venv) C:\pypi_package_example>python setup.py --help-commands
    Standard commands:
      build             build everything needed to install
      build_py          "build" pure Python modules (copy to build directory)
      build_ext         build C/C++ extensions (compile/link to build directory)
      build_clib        build C/C++ libraries used by Python extensions
      build_scripts     "build" scripts (copy and fixup #! line)
      clean             clean up temporary files from 'build' command
      install           install everything from build directory
      install_lib       install all Python modules (extensions and pure Python)
      install_headers   install C/C++ header files
      install_scripts   install scripts (Python or otherwise)
      install_data      install data files
      sdist             create a source distribution (tarball, zip file, etc.)
      register          register the distribution with the Python package index
      bdist             create a built (binary) distribution
      bdist_dumb        create a "dumb" built distribution
      bdist_rpm         create an RPM distribution
      bdist_wininst     create an executable installer for MS Windows
      check             perform some checks on the package
      upload            upload binary package to PyPI

    Extra commands:
      bdist_wheel       create a wheel distribution
      build_sphinx      Build Sphinx documentation
      flake8            Run Flake8 on modules registered in setup.py
      compile_catalog   compile message catalogs to binary MO files
      extract_messages  extract localizable strings from the project code
      init_catalog      create a new catalog based on a POT file
      update_catalog    update message catalogs from a POT file
      alias             define a shortcut to invoke one or more commands
      bdist_egg         create an "egg" distribution
      develop           install package in 'development mode'
      dist_info         create a .dist-info directory
      easy_install      Find/get/install Python packages
      egg_info          create a distribution's .egg-info directory
      install_egg_info  Install an .egg-info directory for the package
      rotate            delete older distributions, keeping N newest files
      saveopts          save supplied options to setup.cfg or other config file
      setopt            set an option in setup.cfg or another config file
      test              run unit tests after in-place build
      upload_docs       Upload documentation to PyPI

    usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
       or: setup.py --help [cmd1 cmd2 ...]
       or: setup.py --help-commands
       or: setup.py cmd --help

The setup.py file itself can be pretty simple. As it is Python, you can keep adding onto it
as your project gets more complex and you need more customization. See the `setup.py documentation`_
for an idea of what you can do with that file.

.. literalinclude:: ../setup.py
    :caption: setup.py
    :linenos:


.. _PyPi Package Index: https://pypi.org/
.. _setup.py documentation: https://github.com/pvcraven/pypi_package_example/blob/master/setup.py
.. _Writing the Setup Script: https://docs.python.org/3.8/distutils/setupscript.html
