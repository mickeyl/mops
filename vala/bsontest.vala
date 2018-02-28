#!/usr/bin/env vala --vapidir=vapi --pkg=libbson-1.0

void test_oid()
{
    assert( BSON.OID.is_valid( "5a966a0f9dee919162b59239" ) );
    BSON.OID oid;
    oid = BSON.OID();
    time_t timestamp = oid.get_time_t();
    var str = Posix.ctime( ref timestamp );
    print( @"$oid created at $str\n" );

    oid = BSON.OID.from_string( "5a966a0f9dee919162b59239" );
    str = oid.to_string();
    assert( str == "5a966a0f9dee919162b59239" );

    oid = BSON.OID();
    time_t t = oid.get_time_t();
    str = Posix.ctime( ref timestamp );
    print( @"$oid created at $str\n" );
}

void main()
{
    test_oid();

    var d2 = new BSON.Document();
    d2.array_append_utf8( "zero" );
    d2.array_append_utf8( "one" );
    d2.array_append_utf8( "two" );
    d2.array_append_utf8( "three" );

    var doc = new BSON.Document();
    doc.append_oid( "_id", -1, BSON.OID() );
    doc.append_utf8( "Hello", -1, "World", -1 );
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

    var i = BSON.Iter.find( doc, "Hello" );
    print( @"key = \"$(i.key())\": \"$(i.utf8())\"\n" );

    print( @"doc = $doc\n" );
}
