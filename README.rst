beaker handlersocket session backend
------------------------------------



MySQL table structure
---------------------

Sample::

    CREATE TABLE `users` (
      `id` char(50) NOT NULL,
      `data` varbinary(10000) DEFAULT NULL,
      `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB


Beaker config settings
----------------------

Sample::

    {
        "type": "handlersocket",
        "read_servers": ["192.168.1.2:9998", "192.168.1.3:9998"],
        "write_servers": ["192.168.1.2:9999", "192.168.1.3:9999"],
        "database": "sessions",
        "table": "users",
        "index": "PRIMARY"
    }


Notes
-----

Requires packages not in pip. Use --process-dependency-links with pip to install properly 
