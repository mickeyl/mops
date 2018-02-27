#!/usr/bin/env vala --vapidir=vapi --pkg=libbson-1.0

void main()
{
    var doc = new BSON.BSON();

    doc.append_utf8( "foo", -1, "bar", -1 );

    print( "number of keys in document: %u\n", doc.count_keys() );

    print( @"doc = $doc\n" );
}
