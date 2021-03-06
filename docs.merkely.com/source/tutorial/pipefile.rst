Defining Your Pipeline
----------------------

Merkely uses a declarative Pipefile to define the DevOps Change Management needs of a pipeline.  It is a JSON file, typically stored in your source code repository that tells Merkely about your software delivery process and what process and control evidence to expect.


.. literalinclude:: ../app/tests/unit/test-pipefile.json
    :language: JSON
    :linenos:


To make integration with Merkely easy to implement in devops pipelines we provide a docker image `merkely/change
<https://github.com/merkely-development/change>`_.  Using commands in this image you can define, log and control different aspects of your software delivery process automatically.

For example, to declare the pipeline definition in Merkely you use the command :ref:`declare_pipeline <declare_pipeline>`
like so:

.. describe_command:: declare_pipeline invocation_minimum docker

You send this Pipefile at the start of every CI run.  This allows changes made in the pipefile to automatically propagate to Merkely; with the added benefit that these changes can go through your standard peer review process.
