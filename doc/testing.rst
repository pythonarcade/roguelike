.. _testing:

Testing
=======

PyTest
------

There are several testing frameworks that exist for helping
with unit tests. One of the most popular for Python is
PyTest_. PyTest makes it easy to write and run unit tests.

Typically I create a directory called "tests" for all of the
unit tests. I put the "tests" directory in my root folder, but
if you want to run tests as part of the package once it has been
installed, then you'll need to include it as a subdirectory in the
folder with the source code.

Files that contain tests should start with ``test_`` and contain
functions that start the same way:

``/tests/test_*.py``

An example test file:

.. literalinclude:: ../tests/test_my_addition_function.py
    :caption: test_my_addition_function.py
    :linenos:

If you are using PyCharm you can right-click on the tests folder
and run the tests easily from within the IDE.

You can run PyTest from the command-line by just typing in ``pytest`` on the
root folder. If that doesn't work:

* Make sure PyTest is listed in ``requirements.txt`` and installed.
* Create an empty file called ``conftest.py`` in the root of your
  project folder.

Code Coverage
-------------

If you'd like to make sure that your unit tests cover all (or most) of your
code, you can add the pytest-cov_ package. Then you can run PyTest with the
``--cov`` parameter to see what percent of the project your tests cover:

``pytest --cov=pypi_package_example tests/``

You'll get putput like this:

.. code-block:: text

    (venv) S:\Webserver\pypi_package_example>pytest --cov=pypi_package_examp
    le tests/
    ========================= test session starts =========================
    platform win32 -- Python 3.7.4, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
    rootdir: S:\Webserver\pypi_package_example
    plugins: cov-2.8.1
    collected 2 items

    tests\test_my_addition_function.py .                             [ 50%]
    tests\test_my_function.py .                                      [100%]

    ----------- coverage: platform win32, python 3.7.4-final-0 -----------
    Name                               Stmts   Miss  Cover
    ------------------------------------------------------
    pypi_package_example\__init__.py       4      0   100%


    ========================== 2 passed in 0.09s ==========================

This does not guarantee that your tests are good tests, just help you identify
what parts of the code are at least run once as part of the tests.

If you want an even nicer display, the Coveralls_ website allows you to display
and navigate your code coverage statistics. This is easy to add, by linking
the Coveralls_ website to your GitHub account, turning on the project, and
updating the ``/.travis.yml`` file to send over the data.

.. _pre-commit-doc:

Pre-Commit
----------

If you want to make sure that everything is in order before you
commit, the `Pre-commit`_ module will allow you to run tests
(andy anything else you'd like)
whenever you try to commit with git. This helps encourage
code quality.

.. _Pre-commit: https://pre-commit.com/
.. _PyTest: https://docs.pytest.org/en/latest/
.. _Coveralls: https://pypi.org/project/python-coveralls/
.. _pytest-cov: https://pypi.org/project/pytest-cov/
