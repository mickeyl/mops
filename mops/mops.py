import pymongo
import bson
import json
import readline
import cmd
import os
import sys

class MongoJSONEncoder( json.JSONEncoder ):
     def default(self, obj):
         if isinstance(obj, bson.ObjectId):
             return repr( obj )
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)

class Mops():

    def mongoDatabaseNames( self ):
        return self.mc.database_names()

    def mongoCollectionNames( self, dbname ):
        return self.mc[dbname].collection_names()

    def mongoDocuments( self, dbname, collection, limit, query={} ):
        return list( self.mc[dbname][collection].find( query ).limit( limit ) )

    def mongoDistinct( self, dbname, collection, fieldname ):
        return self.mc[dbname][collection].distinct( fieldname )

    def __init__(self):
        self.prompt = "mops> "
        self.intro  = "Welcome to MOPS – MOngodb Prototype Shell!\n"  ## defaults to None
        self.mc = pymongo.MongoClient()

    def complete( self, text, state ):
        # print( "%s (%s)" % ( text, state ) )
        if state == 0:
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            components = origline.split( " " )

            if len( components ) < 2:
                allmatches = self.mongoDatabaseNames()
            elif len( components ) == 2:
                allmatches = self.mongoCollectionNames( components[0] )
            else:
                allmatches = []

            self.matches = [ match for match in allmatches if match.startswith( text )]

        return self.matches[state] if state < len( self.matches ) else None

    def run( self ):
        print( self.intro )
        readline.set_completer_delims( readline.get_completer_delims().replace( '-', '' ) )
        readline.parse_and_bind( "tab:complete")
        readline.set_completer( self.complete )
        while True:
            line = input( self.prompt )
            components = line.strip().split()
            if len( components ) == 0:
                result = self.mongoDatabaseNames()
            elif len( components ) == 1:
                dbname = components[0]
                result = self.mongoCollectionNames( dbname )
            elif len( components ) == 2:
                dbname = components[0]
                collection = components[1]
                result = self.mongoDocuments( dbname, collection, limit=15 )
            elif len( components ) == 3:
                dbname = components[0]
                collection = components[1]
                query = components[2]

                if query.startswith( "{" ):
                    try:
                        dictionary = eval( components[2] )
                        result = self.mongoDocuments( dbname, collection, limit=15, query=dictionary )
                    except Exception:
                        result = repr( sys.exc_info() )
                else:
                    result = self.mongoDistinct( dbname, collection, fieldname=query )
            else:
                result = "?"
            
            print( json.dumps( result, sort_keys=True, indent=2, separators=( ',', ': ' ), cls=MongoJSONEncoder ) )


if __name__ == '__main__':
    console = Mops()
    try:
        console.run()
    except ( EOFError, KeyboardInterrupt ):
        print( "\nThanks for using MOPS!" )
