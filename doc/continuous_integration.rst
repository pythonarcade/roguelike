Continuous Integration
======================

There are many services that will automatically build your project on multiple
platforms and run unit tests, code formatting tests, and code coverage tests.

While you can create your own in-house build machine, there are companies that
already have it set up. Some of them include:

* Appveyor_
* Jenkins_
* TravisCI_

.. _travis-ci:

Travis CI
---------

In this example, we use TravisCI to do our builds. There is a `YAML`_ configuration
file for TravisCI in the main file:

* `.travis.yml`_

Here is the link so you can see the  `TravisCI for pypi_package_example`_
build history on TravisCI.

Using Coveralls, you can see the code coverage of our tests:

* https://coveralls.io/github/pvcraven/pypi_package_example

You can add cool badges to your docs for these:

.. image:: https://travis-ci.org/pvcraven/pypi_package_example.svg?branch=master
    :target: https://travis-ci.org/pvcraven/pypi_package_example

.. image:: https://coveralls.io/repos/github/pvcraven/pypi_package_example/badge.svg?branch=master
    :target: https://coveralls.io/github/pvcraven/pypi_package_example?branch=master

.. _.travis.yml: https://github.com/pvcraven/pypi_package_example/blob/master/.travis.yml
.. _TravisCI for pypi_package_example: https://travis-ci.org/pvcraven/pypi_package_example
.. _Appveyor: https://www.appveyor.com/
.. _Jenkins: https://jenkins.io/
.. _TravisCI: https://travis-ci.org/
.. _YAML: https://en.wikipedia.org/wiki/YAML
