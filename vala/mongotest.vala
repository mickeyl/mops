#!/usr/bin/env vala --vapidir=vapi --pkg=libmongoc-1.0

void main()
{
    Mongo.init();

    var client = new Mongo.Client();
}
