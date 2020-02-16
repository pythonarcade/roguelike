.. _documentation:

Package Documentation Files
===========================

Documenting your project is important if you want anyone else to use it.
Documentation is done using a markup language that is then converted into HTML
for your website.

To convert from a markup language to HTML we use a tool called Sphinx_.
Sphinx is a popular tool for creating web documentation for Python projects. It
is part of a larger group of tools known as *Static Site Generators*. You can see a list of
top static site generators at StaticGen_.

Markdown_ (.md) and `RestructuredText`_ (.rst) - Static sites are normally written using
either markdown or restructured text. Markdown is more popular in the whole eco-system
of markup. RestructuredText is more popular for Python documentation. Restructured Text
also allows inclusion of external files, which is GREAT for maintaining code samples. See
examples of this at:

http://arcade.academy/examples

To get started with Sphinx, there's a sphinx-quickstart_ command that can build out
some of the files to get started. Personally, I find it easier to start with an
old project and copy/modify from there.

Building API Docs From Code
---------------------------
Sphinx can pull documentation stored in comments from
Python files. If the Python code looks like this:

.. literalinclude:: ../pypi_package_example/__init__.py
    :caption: Documented Python Code Listing
    :linenos:

Then, in the restructured text file add code like the following:

.. code-block:: text

    .. automodule:: pypi_package_example
        :members:
        :undoc-members:
        :inherited-members:
        :show-inheritance:

And finally get output that looks like this: :ref:`API`

Note how it also links to the source of the code!

Read The Docs
-------------

Do you have an open-source project and don't want to spend a lot of time
hosting a website and keeping everything up-to-date? ReadTheDocs_ will
take any GitHub project and automatically build a website for you
using Sphinx. They will inject some ads into it to help pay
for it.

ReadTheDocs supports custom URLs. They also support webhooks that
will auto-build the documentation every time you push a new version
to GitHub.

Files and Directories for Documentation
---------------------------------------

* ``/doc/`` Put your documentation in this directory
* ``/doc/index.rst`` This is your main landing page
* ``/doc/_static`` This directory will be included in your main project. I use it
  for a custom css file.
* ``/doc/images`` It is a good idea to keep images separate from content.
* ``/pypi_package_example/examples`` If you want example code, I suggest putting
  it in a subdirectory to your project. Don't put it in the doc directory. This
  makes it easy to run your example with a command like:

.. code-block:: text

    python -m pypi_package_example/examples/my_example

.. _StaticGen: http://staticgen.com
.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _Markdown: https://www.markdownguide.org/basic-syntax
.. _RestructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
.. _ReadTheDocs: https://readthedocs.org/
.. _sphinx-quickstart: https://www.sphinx-doc.org/en/master/usage/quickstart.html