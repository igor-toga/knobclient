========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/python-knobclient.svg
    :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on

========================
python-knobclient
========================

OpenStack Indexing and Search API Client Library

This is a client library for Knob built. It
provides a Python API (the ``knobclient`` module)

.. _Github: https://github.com/igor-toga/python-knobclient

python-knobclient is licensed under the Apache License like the rest of
OpenStack.

.. contents:: Contents:
   :local:

Install the client from PyPI
----------------------------
The :program:`python-knobclient` package is published on `PyPI`_ and
so can be installed using the pip tool, which will manage installing all
python dependencies::

   $ pip install python-knobclient

.. note::
   The packages on PyPI may lag behind the git repo in functionality.

.. _PyPI: https://pypi.python.org/pypi/python-knobclient/

Setup the client from source
----------------------------

* Clone repository for python-knobclient::

    $ git clone https://github.com/openstack/python-knobclient.git
    $ cd python-knobclient

* Setup a virtualenv

.. note::
   This is an optional step, but will allow knobclient's dependencies
   to be installed in a contained environment that can be easily deleted
   if you choose to start over or uninstall knobclient.

::

    $ tox -evenv --notest

Activate the virtual environment whenever you want to work in it.
All further commands in this section should be run with the venv active:

::

    $ source .tox/venv/bin/activate

.. note::
   When ALL steps are complete, deactivate the virtualenv: $ deactivate

* Install knobclient and its dependencies::

    (venv) $ python setup.py develop


Testing
-------

There are multiple test targets that can be run to validate the code.

* tox -e pep8 - style guidelines enforcement
* tox -e py27 - traditional unit testing
