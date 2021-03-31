Creating Approvals
==================

Many software development processes require an active decision to document an approval for deployment.
This Human-in-the-Loop decision must be taken by someone responsible for accepting the risk of a given deployment.
In order to be able to accept the risk, two criteria must be fulfilled:

1. The change must be understood.
2. The acceptance must be documented.

Merkely creates the documentation for approvals automatically in your pipelines.

.. image:: ../images/approvals.png

Merkely makes a dashboard for the cumulative change in the deployment, based on a list of the source git commits.
You simply provide two git references: one for what is currently in production, and one for what you would like to deploy.
Merkely will generate the git commit list between these two commits.
In this example from the image above, to document the approval for deploying the artifact created at the master commit you would use the following parameters.

+------------------------------+--------------------+
| MERKELY_OLDEST_SRC_COMMITISH | production         |
+------------------------------+--------------------+
| MERKELY_NEWEST_SRC_COMMITISH | master             |
+------------------------------+--------------------+


Merkely provides two methods for documenting deployment approvals:

* Pipeline approval: The :ref:`approve_deployment-label` command documents an approval accepted externally to Merkely, for example in a CI pipeline .yml file.
* Merkely approval: The :ref:`request_approval-label` command documents an approval to be accepted in Merkely. Once the command has completed the approval can be accepted within the Merkely application.


In a typical setup, you need to add a :code:`production` tracking branch in git that is updated on every deployment. For example:

.. code-block:: bash

    git checkout production
    git merge --ff-only master
    # YOUR DEPLOYMENT COMMAND HERE
    git push origin production



