#!/usr/bin/env vala --vapidir=vapi --pkg=libbson-1.0

void main()
{
    var doc = new BSON.Document();

    BSON.Document d2 = null;

    doc.append_array_begin( "array", -1, d2 );

    doc.append_utf8( "foo", -1, "bar", -1 );

    print( "number of keys in document: %u\n", doc.count_keys() );

    print( @"doc = $doc\n" );
}
