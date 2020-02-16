Getting Code Formatted Correctly
================================

Code should follow a consistent standard to help readability. For Python
this standard is defined in the style-guide called PEP-8_.

If you use PyCharm, you can use there hints. These appear as a yellow underline
around the offending code, and on the right margin. You can also scan an entire
prject with the *Code...Inspect Code* menu option.

To scan for PEP-8 compliance on the command-line, you can use the flake8_ module.

The Black_ will fix many issues for you automatically, rather than just telling
you about them.

Using the pre-commit_ module along with flake8_ and Black_ will make sure that
code meets standards before allowing it to be committed.

flake8_ can also be added as part of the Continuous Integration and cause a
broken build if standards aren't met.

.. _flake8: http://flake8.pycqa.org/en/latest/
.. _Black: https://pypi.org/project/black/
.. _pre-commit: https://pre-commit.com/
.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
