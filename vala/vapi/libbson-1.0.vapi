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

    [CCode (cname = "bson_value_t", copy_function = "bson_value_copy", destroy_function = "bson_value_destroy")]
    [Compact]
    public class Value
    {

    }

    public class Array : Value
    {
    }

    [CCode (cname = "bson_t", cprefix = "BSON", lower_case_cprefix = "bson_", has_type_id = false, destroy_function = "bson_destroy")]
    [Compact]
    public class BSON
    {
        [CCode (cname = "bson_new")]
        public BSON();

        public void append_utf8( string key, uint keylength, string value, uint length );
        public void append_array( string key, uint keylength, Array array );


        public string as_canonical_extended_json( out size_t length = null );
        public string as_relaxed_extended_json( out size_t length = null );

        public uint32 count_keys();
        public bool has_field( string key );


        public string to_string()
        {
            return this.as_canonical_extended_json();
        }
    }
}
