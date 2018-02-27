#!/usr/bin/env vala --vapidir=vapi --pkg=libbson-1.0

void main()
{

    var d2 = new BSON.Document();
    d2.array_append_utf8( "zero" );
    d2.array_append_utf8( "one" );
    d2.array_append_utf8( "two" );
    d2.array_append_utf8( "three" );

    var doc = new BSON.Document();
    doc.append_array( "array", -1, d2 );

    string json = "{ \"yo\": [ 0, 2, 3] }";
    BSON.Error e = BSON.Error() { domain = 10 };
    var d3 = new BSON.Document.from_json( json, json.length, out e );
    if ( e.domain != 0 )
    {
        error( @"$(e.message)" );
    }
    doc.append_document( "d3", -1, d3 );

    print( "number of keys in document: %u\n", doc.count_keys() );

    print( @"doc = $doc\n" );
}
