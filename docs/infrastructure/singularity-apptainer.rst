Singularity / Apptainer
=======================

Overview
--------

**Singularity** (now maintained as **Apptainer**) is the container runtime of
choice on shared HPC clusters. Unlike Docker it does not require root
privileges, making it compatible with multi-user systems. You can pull any
Docker image from BioContainers and convert it to a Singularity Image File
(``.sif``) that runs under your normal user account.

Installation
------------

On most HPC systems Apptainer is pre-installed as a module:

.. code-block:: bash

   module load apptainer   # or: module load singularity

On a personal Linux machine, install from the official packages:

.. code-block:: bash

   # Ubuntu / Debian
   sudo apt install -y apptainer

   # CentOS / RHEL / Fedora
   sudo dnf install -y apptainer

Verify the installation:

.. code-block:: bash

   singularity --version

Basic Usage
-----------

Converting a Docker image
^^^^^^^^^^^^^^^^^^^^^^^^^

``singularity pull`` downloads a Docker image and converts it into a ``.sif``
file.

.. code-block:: bash

   # On HPC: convert Docker image to Singularity/Apptainer
   singularity pull docker://biocontainers/fastqc:v0.12.1

This creates ``fastqc_v0.12.1.sif`` in the current directory.

Running a tool
^^^^^^^^^^^^^^

Use ``singularity exec`` to run a command inside the container:

.. code-block:: bash

   singularity exec fastqc_v0.12.1.sif fastqc sample_R1.fastq.gz

By default Singularity bind-mounts your home directory and the current
working directory, so input files are visible without extra flags.

Running inside a SLURM job
^^^^^^^^^^^^^^^^^^^^^^^^^^

Containers work seamlessly with SLURM. Replace direct tool calls with
``singularity exec``:

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=fastqc_singularity
   #SBATCH --cpus-per-task=4
   #SBATCH --mem=8G
   #SBATCH --time=01:00:00

   module load apptainer

   singularity exec fastqc_v0.12.1.sif \
     fastqc -t 4 sample_R1.fastq.gz sample_R2.fastq.gz

Key Parameters
--------------

``singularity exec``
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag
     - Description
   * - ``--bind src:dst``
     - Bind-mount a host path into the container (e.g. ``--bind /scratch:/scratch``).
   * - ``--pwd``
     - Set the working directory inside the container.
   * - ``--cleanenv``
     - Start with a clean environment (ignore host environment variables).
   * - ``--nv``
     - Enable NVIDIA GPU support (for GPU-accelerated tools such as Dorado).
   * - ``--contain``
     - Isolate the container -- do not auto-mount home or temp directories.

``singularity pull``
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag
     - Description
   * - ``--dir``
     - Directory to store the ``.sif`` file.
   * - ``--force``
     - Overwrite an existing ``.sif`` file.
   * - ``--disable-cache``
     - Do not cache layers (useful on systems with small ``/tmp``).

Expected Output
---------------

After pulling and running the FastQC container you will have:

.. code-block:: text

   fastqc_v0.12.1.sif         # Singularity image file (~250 MB)
   sample_R1_fastqc.html      # FastQC report
   sample_R1_fastqc.zip       # FastQC data archive

See Also
--------

* :doc:`docker` -- Docker basics and BioContainers
* :doc:`conda-mamba` -- Conda-based installation as an alternative to
  containers
* :doc:`../getting-started/computing-environment` -- SLURM job submission
  essentials
