Installation
============

Overview
--------

All tools in this book are installed through **Conda** and **Mamba**, the
standard package managers for bioinformatics. Miniforge is the recommended
Conda distribution because it ships with Mamba (a fast, C++ drop-in
replacement for ``conda``) and defaults to the ``conda-forge`` channel.

This page walks you through installing Miniforge, creating isolated
environments for your projects, and exporting them for reproducibility.

Installation
------------

Download and run the Miniforge installer for your platform.

.. code-block:: bash

   # Install Miniforge (includes mamba)
   curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
   bash Miniforge3-Linux-x86_64.sh

Follow the prompts and allow the installer to initialise your shell. Restart
your terminal once installation finishes.

.. note::

   On macOS, replace ``Linux-x86_64`` with ``MacOSX-x86_64`` (Intel) or
   ``MacOSX-arm64`` (Apple Silicon).

Basic Usage
-----------

Creating an environment
^^^^^^^^^^^^^^^^^^^^^^^

Create a dedicated environment for each analysis project. Pin every package
version so that results stay reproducible.

.. code-block:: bash

   # Create an environment for an RNA-seq project
   mamba create -n rnaseq -c conda-forge -c bioconda \
     fastqc=0.12.1 fastp=0.23.4 star=2.7.11b \
     subread=2.0.6 samtools=1.19 multiqc=1.21

Activating an environment
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Activate the environment
   mamba activate rnaseq

All tools listed above are now on your ``$PATH``. Deactivate with
``mamba deactivate`` when you are done.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-n``
     - Name the new environment.
   * - ``-c``
     - Add a channel (use ``conda-forge`` and ``bioconda``).
   * - ``--override-channels``
     - Ignore channels in ``.condarc`` and use only those on the command line.
   * - ``--strict-channel-priority``
     - Resolve packages from channels in the order listed (recommended).

Exporting for Reproducibility
-----------------------------

Lock your environment so collaborators can recreate it exactly.

.. code-block:: bash

   # Export the environment for reproducibility
   mamba env export > environment.yml

Share ``environment.yml`` alongside your analysis code. A collaborator
recreates the environment with:

.. code-block:: bash

   mamba env create -f environment.yml

Expected Output
---------------

After running ``mamba activate rnaseq``, verify that tools are available:

.. code-block:: bash

   fastqc --version    # FastQC v0.12.1
   samtools --version   # samtools 1.19
   multiqc --version    # multiqc, version 1.21

See Also
--------

* :doc:`../infrastructure/conda-mamba` -- in-depth Conda/Mamba guide with
  advanced environment management
* :doc:`computing-environment` -- Linux essentials and SLURM job submission
* :doc:`test-datasets` -- download test data to validate your installation
