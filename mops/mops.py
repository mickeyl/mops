"""
MOPS - MongoDB Prototyping Shell

(C) 2015 Dr. Michael 'Mickey' Lauer <mickey@vanille.de>

https://github.com/mickeyl/mops
"""

import pymongo
import bson
import json
import readline
import cmd
import os
import sys
import inspect

from clint.textui import progress

#############################################################################
class MongoJSONEncoder( json.JSONEncoder ):

    """
    Our custom JSON encoder to facilitate encoding some of the mongodb types which are not standard JSON.
    """

    def default( self, obj ):
        try:
            return json.JSONEncoder.default( self, obj )
        except TypeError:
            return repr( obj )

#############################################################################
class DatabaseWrapper():

    """
    Implementation of the mongodb commands
    """

    def __init__( self ):
        self.mc = pymongo.MongoClient()

    def databaseNames( self ):
        return self.mc.database_names()

    def collectionNames( self, dbname ):
        return self.mc[dbname].collection_names()

    def queryDocuments( self, dbname, collection, limit, query={} ):
        return list( self.mc[dbname][collection].find( query ).limit( limit ) )

    def distinctValuesForField( self, dbname, collection, fieldname ):
        return self.mc[dbname][collection].distinct( fieldname )

    def copyDatabase( self, dbname, dbname2 ):
        try:
            self.mc.admin.command( "copydb", fromdb=dbname, todb=dbname2 )
        except Exception:
            return repr( sys.exc_info() )
        else:
            return "Database %s successfully copied to %s" % ( dbname, dbname2 )

    def dropDatabase( self, dbname ):
        try:
            self.mc.drop_database( dbname )
        except Exception:
            return repr( sys.exc_info() )
        else:
            return "Database %s successfully dropped" % ( dbname )

    def copyCollection( self, dbname, collname, dbname2, collname2 ):
        try:
            cursor = self.mc[dbname][collname].find( {} )
            for document in progress.bar( cursor, "Copying collection: ", expected_size=cursor.count() ):
                self.mc[dbname2][collname2].insert_one( document )
        except Exception:
            return repr( sys.exc_info() )
        else:
            return "Collection %s:%s duplicated as %s:%s" % ( dbname, collname, dbname2, collname2 )

    def duplicateCollection( self, dbname, collname, collname2 ):
        return self.copyCollection( dbname, collname, dbname, collname2 )

    def dropCollection( self, dbname, collname ):
        try:
            self.mc[dbname].drop_collection( collname )
        except Exception:
            return repr( sys.exc_info() )
        else:
            return "Collection %s:%s successfully dropped" % ( dbname, collname )

#############################################################################
class Mops():

    """
    The Shell.
    """

    def __init__(self):
        self.prompt = "mops> "
        self.intro = "Welcome to MOPS – MOngodb Prototype Shell!\n"
        self.outro = "\nThanks for using MOPS – Have a nice day!"
        self.db = DatabaseWrapper()
        commandPrefix = "handleTheCommand"
        self.commands = [ ":" + method.replace( commandPrefix, "").lower() for method in dir(self) if callable(getattr(self, method)) if method.startswith( commandPrefix ) ]

    def shutdown( self ):
        print( self.outro )

    def matchesForExplorationMode( self ):
        components = readline.get_line_buffer().split()
        if len( components ) < 2:
            return self.db.databaseNames()
        elif len( components ) == 2:
            return self.db.collectionNames( components[0] )
        else:
            return []

    def matchesForCommandMode( self ):
        numberOfSpaces = readline.get_line_buffer().count( " " )
        if numberOfSpaces == 0:
            return self.commands
        components = readline.get_line_buffer().split()
        command = components[0][1:]
        parameterNames = inspect.getargspec( getattr( self, "handleTheCommand%s" % command.upper() ) ).args
        if numberOfSpaces > len( parameterNames ) - 1:
            return []

        if numberOfSpaces == 1:
            return self.db.databaseNames()
        elif numberOfSpaces == 2:
            if "atabase" in parameterNames[2]:
                return self.db.databaseNames()
            else:
                return self.db.collectionNames( components[1] )
        elif numberOfSpaces == 3:
            if "atabase" in parameterNames[3]:
                return self.db.databaseNames()
            else:
                return self.db.collectionNames( components[1] )
        elif numberOfSpaces == 4:
            return self.db.collectionNames( components[3] )

    def complete( self, text, state ):
        """
        Readline completion
        """
        # print( "%s (%s)" % ( text, state ) )
        if state == 0:
            origline = readline.get_line_buffer()
            #begin = readline.get_begidx()
            #end = readline.get_endidx()
            #being_completed = origline[begin:end]
            if len( origline ) > 0 and origline[0] == ":":
                allmatches = self.matchesForCommandMode()
            else:
                allmatches = self.matchesForExplorationMode()

            self.matches = [ match for match in allmatches if match.startswith( text )]

        return self.matches[state] if state < len( self.matches ) else None

    def handleLine( self, line ):
        if line.startswith( ":" ):
            return self.handleCommandLine( line )
        else:
            return self.handleExplorationLine( line )

    def handleCommandLine( self, line ):
        components = line.strip().split()
        command, parameters = components[0][1:], components[1:]
        try:
            commandMethod = getattr( self, "handleTheCommand%s" % command.upper() )
            argspec = inspect.getargspec( commandMethod )
            numberOfExpectedArguments = len( argspec.args ) - 1  # self is implicit
            if numberOfExpectedArguments != len( parameters ):
                return getattr( commandMethod, "__doc__" ).strip()
            result = commandMethod( *parameters )
        except AttributeError:
            return "Sorry, command '%s' is not implemented." % command
        else:
            return result

    def handleExplorationLine( self, line ):
        components = line.strip().split()
        if len( components ) == 0:
            result = self.db.databaseNames()
        elif len( components ) == 1:
            dbname = components[0]
            result = self.db.collectionNames( dbname )
        elif len( components ) == 2:
            dbname = components[0]
            collection = components[1]
            result = self.db.queryDocuments( dbname, collection, limit=15 )
        elif len( components ) == 3:
            dbname = components[0]
            collection = components[1]
            query = components[2]

            if query.startswith( "{" ):
                try:
                    dictionary = eval( components[2] )
                    result = self.db.queryDocuments( dbname, collection, limit=15, query=dictionary )
                except Exception:
                    result = repr( sys.exc_info() )
            else:
                result = self.db.distinctValuesForField( dbname, collection, fieldname=query )
        else:
            result = "?"
        return result

    def handleTheCommandQ( self ):
        raise EOFError()

    def handleTheCommandHELP( self ):
        result = """To be done (Read from README.md, so we don't have to maintain two set of docs)."""
        return result

    def handleTheCommandCOPYDB( self, sourceDatabase, destDatabase ):
        """
        Syntax: copydb <sourceDatabase> <destDatabase>

        Insert everything from the source database into the destination database.
        """
        return self.db.copyDatabase( sourceDatabase, destDatabase )

    def handleTheCommandDUPLICATECOLL( self, sourceDatabase, sourceCollection, destCollection ):
        """
        Syntax: duplicatecoll <sourceDatabase> <sourceCollection> <destCollection>

        Insert everything from the source collection into the destination collection.
        """
        return self.db.duplicateCollection( sourceDatabase, sourceCollection, destCollection )

    def handleTheCommandCOPYCOLL( self, sourceDatabase, sourceCollection, destDatabase, destCollection ):
        """
        Syntax: copycoll <sourceDatabase> <sourceCollection> <destDatabase> <destCollection>

        Insert everything from the source collection into another database's collection.
        """
        return self.db.copyCollection( sourceDatabase, sourceCollection, destDatabase, destCollection )

    def handleTheCommandDROPDB( self, database ):
        """
        Syntax: dropdb <database>

        Delete a database.
        """
        return self.db.dropDatabase( database )

    def handleTheCommandDROPCOLL( self, database, collection ):
        """
        Syntax: dropcoll <database> <collection>

        Delete a collection.
        """
        return self.db.dropCollection( database, collection )

    def run( self ):
        """
        Implementation of the command loop
        """
        print( self.intro )
        readline.set_completer_delims( readline.get_completer_delims().replace( '-', '' ).replace( ":", "" ) )
        readline.parse_and_bind( "tab:complete" )
        readline.set_completer( self.complete )
        while True:
            line = input( self.prompt )
            result = self.handleLine( line )
            print( json.dumps( result, sort_keys=True, indent=2, separators=( ',', ': ' ), cls=MongoJSONEncoder ) )


#############################################################################
if __name__ == '__main__':
    console = Mops()
    try:
        console.run()
    except ( EOFError, KeyboardInterrupt ):
        console.shutdown()
