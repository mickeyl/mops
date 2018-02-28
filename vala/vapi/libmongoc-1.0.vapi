/* libmongoc-1.0.vapi
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

[CCode (cheader_filename = "mongoc.h", lower_case_cprefix = "mongoc_")]
namespace Mongo
{
    // global
    public static void init();
    public static void cleanup();

    // enums
    [CCode (cname = "mongoc_read_mode_t", prefix = "MONGOC_READ_", has_type_id = false)]
    public enum ReadMode
    {
        PRIMARY,
        SECONDARY,
        PRIMARY_PREFERRED,
        SECONDARY_PREFERRED,
        NEAREST
    }

    // classes
    [CCode (cname = "mongoc_client_t", free_function = "mongoc_client_destroy", has_type_id = false)]
    [Compact]
    public class Client
    {
        [CCode (cname = "mongoc_client_new")]
        public Client( string uri = "mongodb://localhost:27017");

        public Database get_database( string dbname );
        [CCode (array_length = false, array_null_terminated = true)]
        public string[] get_database_names_with_opts( BSON.Document? opts = null, out BSON.Error? error = null );
        public Collection get_collection( string dbname, string collname );

        public void set_appname( string appname );
    }

    [CCode (cname = "mongoc_collection_t", free_function = "mongoc_collection_destroy", has_type_id = false)]
    [Compact]
    public class Collection
    {
        public Cursor find_with_opts( BSON.Document filter, BSON.Document? opts = null, ReadPrefs? read_prefs = null );
    }

    [CCode (cname = "mongoc_cursor_t", free_function = "mongoc_cursor_destroy", has_type_id = false)]
    [Compact]
    public class Cursor
    {
        public bool next( out unowned BSON.Document document );

        public unowned Cursor iterator()
        {
            return this;
        }

        [CCode (cname = "_vala_hash_set_next_value")]
        public unowned BSON.Document? next_value ()
        {
            unowned BSON.Document doc;
            return next( out doc ) ? doc : null;
        }
    }

    [CCode (cname = "mongoc_database_t", free_function = "mongoc_database_destroy", has_type_id = false)]
    [Compact]
    public class Database
    {
        public Collection get_collection( string name );
        [CCode (array_length = false, array_null_terminated = true)]
        public string[] get_collection_names_with_opts( BSON.Document? opts = null, out BSON.Error? error = null );
    }

    [CCode (cname = "mongoc_read_prefs_t", copy_function = "mongoc_read_prefs_copy", free_function = "mongoc_read_prefs_destroy", has_type_id = false)]
    [Compact]
    public class ReadPrefs
    {
        public ReadPrefs( ReadMode read_mode );
    }
}
