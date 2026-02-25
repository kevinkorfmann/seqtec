Docker
======

Overview
--------

**Docker** packages software and all of its dependencies into a portable
*container image* that runs identically on any machine. The
`BioContainers <https://biocontainers.pro>`_ project maintains Docker images
for most bioinformatics tools, giving you single-command access to pre-built,
version-locked binaries.

Docker is best suited for local workstations and cloud VMs. For shared HPC
clusters see :doc:`singularity-apptainer`.

Installation
------------

Install Docker Engine following the official instructions for your platform:

* **Linux** -- https://docs.docker.com/engine/install/
* **macOS** -- https://docs.docker.com/desktop/install/mac-install/
* **Windows (WSL 2)** -- https://docs.docker.com/desktop/install/windows-install/

Verify the installation:

.. code-block:: bash

   docker --version
   docker run hello-world

Basic Usage
-----------

Pulling and running a BioContainers image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Pull and run a Docker image for FastQC
   docker pull biocontainers/fastqc:v0.12.1
   docker run --rm -v $(pwd):/data biocontainers/fastqc:v0.12.1 \
     fastqc /data/sample_R1.fastq.gz /data/sample_R2.fastq.gz

   # BioContainers provides images for most bioinformatics tools
   # See: https://biocontainers.pro

``--rm`` removes the container after it exits. ``-v $(pwd):/data`` mounts
your current directory into the container at ``/data`` so that input files
are visible and output files are written back to the host.

Running an interactive shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   docker run --rm -it -v $(pwd):/data biocontainers/samtools:v1.19 bash

This drops you into a shell inside the container where ``samtools`` is
available.

Key Parameters
--------------

``docker run``
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag
     - Description
   * - ``--rm``
     - Automatically remove the container when it exits.
   * - ``-v host:container``
     - Bind-mount a host directory into the container.
   * - ``-it``
     - Allocate a pseudo-TTY and keep stdin open (interactive mode).
   * - ``-w``
     - Set the working directory inside the container.
   * - ``--cpus``
     - Limit CPU cores (e.g. ``--cpus 4``).
   * - ``--memory``
     - Limit memory (e.g. ``--memory 8g``).
   * - ``-e``
     - Set an environment variable inside the container.

``docker image``
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Command
     - Description
   * - ``docker images``
     - List downloaded images.
   * - ``docker image rm <image>``
     - Delete a local image to free disk space.
   * - ``docker system prune``
     - Remove all stopped containers, unused networks, and dangling images.

Expected Output
---------------

After running the FastQC container, the host directory will contain:

.. code-block:: text

   sample_R1_fastqc.html
   sample_R1_fastqc.zip
   sample_R2_fastqc.html
   sample_R2_fastqc.zip

Open the HTML files in a browser to inspect quality metrics.

See Also
--------

* :doc:`singularity-apptainer` -- convert Docker images for HPC use
* :doc:`conda-mamba` -- alternative installation path using Conda packages
* :doc:`../getting-started/installation` -- quick-start Miniforge setup
