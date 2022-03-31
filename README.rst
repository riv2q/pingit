PingIt
=================

Samll Flask API application, build just for fun.


.. contents:: Contents

Installation and start of the application
----------------------

Installation is simple. Just run this command with *docker*:

.. code:: bash

    $ docker build --tag pingit .

Run application:

.. code:: bash

    $ docker run -p 5000:5000 pingit


Usage examples:
---------------------

Checking etag

.. code:: bash

   curl -i http://localhost:5000/
   HTTP/1.1 200 OK
   Server: Werkzeug/2.1.0 Python/3.9.2
   Date: Thu, 31 Mar 2022 10:49:41 GMT
   Content-Type: application/json
   Content-Length: 27
   ETag: "190663285f8fdfa614e17a026609aa77015033e7"
   Date: Thu, 31 Mar 2022 10:49:41 GMT


Checking if etag works

.. code:: bash

   curl -i http://localhost:5000/ -H 'If-None-Match: 190663285f8fdfa614e17a026609aa77015033e7'
   HTTP/1.1 304 NOT MODIFIED
   Server: Werkzeug/2.1.0 Python/3.9.2
   Date: Thu, 31 Mar 2022 10:46:44 GMT
   ETag: "190663285f8fdfa614e17a026609aa77015033e7"
   Date: Thu, 31 Mar 2022 10:46:44 GMT
   Transfer-Encoding: chunked
