Conda / Mamba
=============

Overview
--------

**Conda** is a cross-platform package and environment manager widely used in
bioinformatics. **Mamba** is a drop-in replacement that resolves dependencies
in C++ and is significantly faster. Together with the **Bioconda** channel
they provide pre-built packages for thousands of bioinformatics tools.

This page covers installation, environment management, and best practices for
reproducible analyses.

Installation
------------

Install Miniforge, a minimal Conda distribution that bundles Mamba and
defaults to ``conda-forge``.

.. code-block:: bash

   # Install Miniforge (includes mamba)
   curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
   bash Miniforge3-Linux-x86_64.sh

.. note::

   On macOS, replace ``Linux-x86_64`` with ``MacOSX-x86_64`` (Intel) or
   ``MacOSX-arm64`` (Apple Silicon).

After the installer finishes, restart your shell so that the ``mamba`` and
``conda`` commands are available.

Basic Usage
-----------

Creating an environment
^^^^^^^^^^^^^^^^^^^^^^^

Always create a dedicated environment per project and pin package versions.

.. code-block:: bash

   # Create an environment for an RNA-seq project
   mamba create -n rnaseq -c conda-forge -c bioconda \
     fastqc=0.12.1 fastp=0.23.4 star=2.7.11b \
     subread=2.0.6 samtools=1.19 multiqc=1.21

Activating and deactivating
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Activate the environment
   mamba activate rnaseq

   # When finished
   mamba deactivate

Exporting and sharing
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Export the environment for reproducibility
   mamba env export > environment.yml

A collaborator recreates the same environment with:

.. code-block:: bash

   mamba env create -f environment.yml

Listing environments and packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # List all environments
   mamba env list

   # List packages in the active environment
   mamba list

Removing an environment
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   mamba env remove -n rnaseq

Key Parameters
--------------

``mamba create``
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``-n``
     - Name of the new environment.
   * - ``-c``
     - Channel to search (repeat for multiple channels).
   * - ``--override-channels``
     - Ignore default channels; use only those given with ``-c``.
   * - ``--strict-channel-priority``
     - Resolve from channels in order (recommended to avoid mixed builds).

``mamba install``
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``-n``
     - Install into a named environment (instead of the active one).
   * - ``--update-deps``
     - Also update existing dependencies as needed.
   * - ``--dry-run``
     - Show what would be installed without making changes.

Best practices
^^^^^^^^^^^^^^

* **Pin versions** -- ``samtools=1.19`` ensures everyone gets the same build.
* **One environment per project** -- avoids dependency conflicts across
  unrelated tools.
* **Prefer Mamba** -- identical syntax to ``conda`` but 10--100x faster
  dependency solving.
* **Keep base clean** -- never install analysis tools into the ``base``
  environment.

Expected Output
---------------

After creating and activating the ``rnaseq`` environment:

.. code-block:: bash

   which fastqc
   # ~/miniforge3/envs/rnaseq/bin/fastqc

   fastqc --version
   # FastQC v0.12.1

   samtools --version | head -1
   # samtools 1.19

See Also
--------

* :doc:`../getting-started/installation` -- quick-start Miniforge setup
* :doc:`docker` -- containerise your pipeline with Docker
* :doc:`singularity-apptainer` -- run containers on HPC where Docker is
  unavailable
