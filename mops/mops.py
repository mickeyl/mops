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
import clint

#############################################################################
class MongoJSONEncoder( json.JSONEncoder ):

    """
    Our custom JSON encoder to facilitate encoding some of the mongodb types which are not standard JSON.
    """

    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return repr( obj )
        return json.JSONEncoder.default(self, obj)

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

    def shutdown( self ):
        print( self.outro )

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
            components = origline.split( " " )

            if len( components ) < 2:
                allmatches = self.db.databaseNames()
            elif len( components ) == 2:
                allmatches = self.db.collectionNames( components[0] )
            else:
                allmatches = []

            self.matches = [ match for match in allmatches if match.startswith( text )]

        return self.matches[state] if state < len( self.matches ) else None

    def run( self ):
        """
        Implementation of the command loop
        """
        print( self.intro )
        readline.set_completer_delims( readline.get_completer_delims().replace( '-', '' ) )
        readline.parse_and_bind( "tab:complete")
        readline.set_completer( self.complete )
        while True:
            line = input( self.prompt )
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

            print( json.dumps( result, sort_keys=True, indent=2, separators=( ',', ': ' ), cls=MongoJSONEncoder ) )


#############################################################################
if __name__ == '__main__':
    console = Mops()
    try:
        console.run()
    except ( EOFError, KeyboardInterrupt ):
        console.shutdown()
