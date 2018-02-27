/* libbson-1.0.vapi
 *
 * Copyright (C) 2018 Dr. Michael 'Mickey' Lauer <mlauer@vanille-media.de>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.

 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.

 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
 */

[CCode (cheader_filename = "bson.h")]
namespace BSON
{
    [CCode (cname = "bson_error_t", destroy_function = "", has_type_id = false)]
    public struct Error
    {
        uint32 domain;
        uint32 code;
        string message;
    }

    [CCode (cname = "bson_oid_t", has_type_id = false)]
    public struct ObjectId
    {
        uint8 bytes[12];
        //void bson_oid_init_from_string (bson_oid_t *oid, const char *str);
        //void bson_oid_to_string (const bson_oid_t *oid, char str[25]);
    } 

    [CCode (cname = "bson_type_t", prefix = "BSON_TYPE_", has_type_id = false)]
    public enum Type
    {
        EOD,
        DOUBLE,
        UTF8,
        DOCUMENT,
        ARRAY,
        BINARY,
        UNDEFINED,
        OID,
        BOOL,
        DATE_TIME,
        NULL,
        REGEX,
        DBPOINTER,
        CODE,
        SYMBOL,
        CODEWSCOPE,
        INT32,
        TIMESTAMP,
        INT64,
        DECIMAL128,
        MAXKEY,
        MINKEY
    }

    [CCode (cname = "bson_subtype_t", prefix = "BSON_SUBTYPE_", has_type_id = false)]
    public enum Subtype
    {
        BINARY,
        FUNCTION,
        BINARY_DEPRECATED,
        UUID_DEPRECATED,
        UUID,
        MD5,
        USER,
    }

    [CCode (cname = "bson_value_t", copy_function = "bson_value_copy", has_type_id = false, free_function = "bson_value_destroy")]
    [Compact]
    public class Value
    {

    }

    [CCode (cname = "bson_t", cprefix = "BSON", lower_case_cprefix = "bson_", has_type_id = false, free_function = "bson_destroy")]
    [Compact]
    public class Document
    {
        [CCode (cname = "bson_new")]
        public Document();

        [CCode (cname = "bson_new_from_json")]
        public Document.from_json( string json, uint length = json.length, out Error error = null );

        public bool append_utf8( string key, uint keylength, string value, uint length = -1 );
        public bool append_array( string key, uint keylength, Document document );
        public bool append_bool( string key, uint keylength, bool b );
        public bool append_double( string key, uint keylength, double d );
        public bool append_document( string key, uint keylength, Document document );
        public bool append_int32( string key, uint keylength, int32 i );
        public bool append_int64( string key, uint keylength, int64 i );
        public bool append_null( string key, uint keylength );
        public bool append_oid( string key, uint keylength, ObjectId oid );
        public bool append_time_t( string key, uint keylength, time_t time );
        public bool append_timeval( string key, uint keylength, Posix.timeval time );
        public bool append_date_time( string key, uint keylength, int64 time );
        public bool append_now_utc( string key, uint keylength );

        public string as_json( out size_t length = null );
        public string as_canonical_extended_json( out size_t length = null );
        public string as_relaxed_extended_json( out size_t length = null );

        public uint32 count_keys();
        public bool has_field( string key );

        public string to_string()
        {
            return as_canonical_extended_json();
        }

        public bool array_append_int32( int32 i )
        {
            return append_int32( count_keys().to_string(), -1, i );
        }

        public bool array_append_utf8( string utf8 )
        {
            return append_utf8( count_keys().to_string(), -1, utf8, -1 );
        }
    }
}
