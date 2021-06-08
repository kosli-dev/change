Logging Controls
================

An important aspect of DevOps compliance is meeting the expectations of
risk controls in your CI pipeline. Examples include:

* Running unit tests/integration tests
* Performing security scanning
* Code coverage
* etc

As you execute these steps, you can use the following commands to log the evidence that these controls have been performed.


* :ref:`control_pull_request-label` command to control and send evidence that a pull request is approved for this commit
* :ref:`log_test-label` command to send evidence that a test has been executed
* :ref:`log_evidence-label` command to send evidence that a generic control has been performed

.. image:: ../images/controls.png

Here is an example of how to use :ref:`log_evidence-label` from your CI pipeline:

.. highlight:: bash
.. describe_command:: log_evidence invocation_minimum docker

