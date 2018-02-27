#!/usr/bin/env vala --vapidir=vapi --pkg=libmongoc-1.0

void main()
{
    Mongo.init();

    var client = new Mongo.Client();
    client.set_appname( "Vala Mongo Demo" );

    var databases = client.get_database_names_with_opts();    
    foreach ( var database in databases )
    {
        print( @"$database\n" );
        var db = client.get_database( database );
        var collections = db.get_collection_names_with_opts();
        foreach ( var collection in collections )
        {
            print( @" |--- $collection\n" );
        }
    }
}
