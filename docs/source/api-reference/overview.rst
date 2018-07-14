*********
Overview
*********

Pyforms web works by having on the client side a javascript layer handeling all the Widgets and Controls updates occurred on the server side.
The Widgets and Controls updates are exchanged using the functions **serialize** and **deserialize** on the client side and the **serialize_form** and **deserialize_form** on the server side. Only updated controls are communicated from one side to the other.

Python when running in a Apache2 does not maintain in memory the objects created in each HTTP request, therefore everytime there is an update to a Widget, one is dumped to the disk and loaded when a new HTTP request arrive.

.. image:: /_static/imgs/pyforms-web-com.png
    :align: center