
Instrumenting Your CI Pipeline
------------------------------

To make integration with Merkely easy to implement in devops pipelines we provide a docker image `merkely/change
<https://github.com/merkely-development/change>`_.  Using commands in this image you can log and control different aspects of your software delivery process automatically.

For example, to log your artifact in Merkely you use the command :ref:`log_artifact-label`
like so:

.. highlight:: bash
.. describe_command:: log_artifact invocation_minimum docker

