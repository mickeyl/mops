MOngo Prototyping Shell
=======================

MOPS is a simple shell written for interactive exploring and maintaining your mongodb databases, collections, and documents.

MOPS is *not* meant to be a replacement for the mongo shell (and will never be), but rather a simple tool for quick interrogation.

Usage
-----

MOPS contains two modes of commands, the exploration mode, and the maintenance mode.

### Exploration mode

In this mode, you can query the available databases, the available collections in a database,
documents in the database, and a list of values given a fieldname.

Syntax:

    <databaseName> <collectionName> <jsonQueryOrFieldname>

### Maintenance mode

In this mode, you can operate (destructive) commands on the database, such as copying, moving, removing, as well as inserting
documents or individual values.

Syntax: 

    :<command> <databaseName> [parameter] [parameter] [parameter]...

Todo before releasing 1.0
-------------------------
* Implement skip and limit for query mode with default parameter 0:15 (iterating through cursor like in mongo shell)
* Implement more commands
* Implement interactive commands also for the commandline

Roadmap
-------
* Colored output?
* Bash completion?
