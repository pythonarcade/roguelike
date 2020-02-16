.. _git:

Git
===

If you are using git version control, you need a list of files and directories
for git to ignore. This are saved in the ``.gitignore`` file.

GitHub maintains a great list of sample ``.gitignore`` files in there
`collection of useful .gitignore templates`_.

My ``.gitignore`` for Python typically looks like this: `.gitignore`_.

.. note::
    Please teach your students not to check in SSH keys! Also make sure they don't check in the results of a build.
    Go over a typical .gitignore so they understand
    why things should be, and should not be checked in.

.. _collection of useful .gitignore templates: https://github.com/github/gitignore
.. _.gitignore: https://github.com/pvcraven/pypi_package_example/blob/master/.gitignore