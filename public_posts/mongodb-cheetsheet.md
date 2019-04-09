---
Title: MongoDB Cheetsheet
Author: Xiaoxue Wang<xxwjoy@hotmail.com >
Versions:
    - 2019-04-09: newly created
---


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

* [MongoDB cheetsheet](#mongodb-cheetsheet)
	* [MongoDB dump & restore](#mongodb-dump-restore)
		* [MongoDB dump & restore -- default format](#mongodb-dump-restore-default-format)
		* [Dump/Restore collections with mongoexport/mongoimport in JSON format](#dumprestore-collections-with-mongoexportmongoimport-in-json-format)
		* [How to restore a db with dump file (gzip) ?](#how-to-restore-a-db-with-dump-file-gzip)
	* [MongoDB Shell Usage](#mongodb-shell-usage)
		* [How to gather the db, collection names ?](#how-to-gather-the-db-collection-names)
		* [How to describe a collection's schema in MongoDB?](#how-to-describe-a-collections-schema-in-mongodb)
		* [How to delete a db in MongoDB ?](#how-to-delete-a-db-in-mongodb)
	* [How to manipulate it via Python ?](#how-to-manipulate-it-via-python)
	* [Mongo DB has no "show all" command.](#mongo-db-has-no-show-all-command)

<!-- /code_chunk_output -->


# MongoDB cheetsheet

Doc: https://docs.mongodb.com


## MongoDB dump & restore

### MongoDB dump & restore -- default format
- To dump your database for backup you call this command on your terminal

```bash
$ mongodump --db database_name --collection collection_name
```

- To import your backup file to mongodb you can use the following command on your terminal

```bash
$ mongorestore --db database_name path_to_bson_file
```


### Dump/Restore collections with mongoexport/mongoimport in JSON format

Export JSON File:
```bash
mongoexport --db <database-name> --collection <collection-name> --out output.json
```
Import JSON File:
```bash
mongoimport --db <database-name> --collection <collection-name> --file input.json
```

NoteByJoy: export: must specify the collection)


### How to restore a db with dump file (gzip) ?

If db is dumped with `--gzip` option,
```bash
$ mongorestore -d taoism --gzip /tmp/taoism.tar.gz
```
else:
```bash
$ mongorestore -d taoism /tmp/taoism
```



## MongoDB Shell Usage

### How to gather the db, collection names ?

~~~
1. Connect to dbshell
	$ mongo
2. List all dbs
	> db.adminCommand( { listDatabases: 1, nameOnly: true} )
3. Use a db
  	> use <db-name>
4. List all collections in this used DB
  	> db.getCollectionInfos();
~~~

```bash
> db.adminCommand( { listDatabases: 1, nameOnly: true} )
{
	"databases" : [
		{
			"name" : "admin"
		},
		{
			"name" : "local"
		},
		{
			"name" : "taoism"
		}
	],
	"ok" : 1
}
> db
test
> use taoism
switched to db taoism
> db.getCollectionInfos();
[
	{
		"name" : "activities",
		"type" : "collection",
		"options" : {

		},
		"info" : {
			"readOnly" : false
		},
		"idIndex" : {
			"v" : 2,
			"key" : {
				"_id" : 1
			},
			"name" : "_id_",
			"ns" : "taoism.activities"
		}
	},
	{
		"name" : "openshift",
		"type" : "collection",
		"options" : {

		},
		"info" : {
			"readOnly" : false
		},
		"idIndex" : {
			"v" : 2,
			"key" : {
				"_id" : 1
			},
			"name" : "_id_",
			"ns" : "taoism.openshift"
		}
	},
	{
		"name" : "proactiveissues",
		"type" : "collection",
		"options" : {

		},
		"info" : {
			"readOnly" : false
		},
		"idIndex" : {
			"v" : 2,
			"key" : {
				"_id" : 1
			},
			"name" : "_id_",
			"ns" : "taoism.proactiveissues"
		}
	},
	{
		"name" : "reviewedkcs",
		"type" : "collection",
		"options" : {

		},
		"info" : {
			"readOnly" : false
		},
		"idIndex" : {
			"v" : 2,
			"key" : {
				"_id" : 1
			},
			"name" : "_id_",
			"ns" : "taoism.reviewedkcs"
		}
	},
	{
		"name" : "tracktrellos",
		"type" : "collection",
		"options" : {

		},
		"info" : {
			"readOnly" : false
		},
		"idIndex" : {
			"v" : 2,
			"key" : {
				"_id" : 1
			},
			"name" : "_id_",
			"ns" : "taoism.tracktrellos"
		}
	},
	{
		"name" : "users",
		"type" : "collection",
		"options" : {

		},
		"info" : {
			"readOnly" : false
		},
		"idIndex" : {
			"v" : 2,
			"key" : {
				"_id" : 1
			},
			"name" : "_id_",
			"ns" : "taoism.users"
		}
	}
]
```


### How to describe a collection's schema in MongoDB?

Query one item in collection, then show it's title/conent of each <key/value> pair.
Refer to: https://stackoverflow.com/a/24311636/7398389

```
var col_list=db.collectionName.findOne()
for (var col in col_list) { print (col_list[col]) ; }
```

Simple describe version:
```bash
# get a item as an example:
> var col_list= db.proactiveissues.findOne();
# print the keys:
> for (var col in col_list) { print (col) ; }
# print values:
> for (var col in col_list) { print (col_list[col]) ; }
```

Example with test-data:
```bash
> use test
switched to db test
> db.inventory.insertMany([
...    // MongoDB adds the _id field with an ObjectId if _id is not present
...    { item: "journal", qty: 25, status: "A",
...        size: { h: 14, w: 21, uom: "cm" }, tags: [ "blank", "red" ] },
...    { item: "notebook", qty: 50, status: "A",
...        size: { h: 8.5, w: 11, uom: "in" }, tags: [ "red", "blank" ] },
...    { item: "paper", qty: 100, status: "D",
...        size: { h: 8.5, w: 11, uom: "in" }, tags: [ "red", "blank", "plain" ] },
...    { item: "planner", qty: 75, status: "D",
...        size: { h: 22.85, w: 30, uom: "cm" }, tags: [ "blank", "red" ] },
...    { item: "postcard", qty: 45, status: "A",
...        size: { h: 10, w: 15.25, uom: "cm" }, tags: [ "blue" ] }
... ]);
{
	"acknowledged" : true,
	"insertedIds" : [
		ObjectId("5cac7d8a321b358fd2d77d99"),
		ObjectId("5cac7d8a321b358fd2d77d9a"),
		ObjectId("5cac7d8a321b358fd2d77d9b"),
		ObjectId("5cac7d8a321b358fd2d77d9c"),
		ObjectId("5cac7d8a321b358fd2d77d9d")
	]
}
> var col_list= db.inventory.findOne();
> col_list
{
	"_id" : ObjectId("5cac7d8a321b358fd2d77d99"),
	"item" : "journal",
	"qty" : 25,
	"status" : "A",
	"size" : {
		"h" : 14,
		"w" : 21,
		"uom" : "cm"
	},
	"tags" : [
		"blank",
		"red"
	]
}
> for (var col in col_list) { print (col) ; }
_id
item
qty
status
size
tags
>
```


### How to delete a db in MongoDB ?

The `dropDatabase()` Method:
MongoDB db.dropDatabase() command is used to drop a existing database.

This will delete the selected database. If you have not selected any database, then it will delete default 'test' database.

Example:
- First, check the list of available databases by using the command, show dbs.
```bash
>show dbs
local      0.78125GB
mydb       0.23012GB
test       0.23012GB
>
```
- If you want to delete new database <mydb>, then dropDatabase() command would be as follows −
```bash
>use mydb
switched to db mydb
>db.dropDatabase()
>{ "dropped" : "mydb", "ok" : 1 }
>
```
- Now check list of databases.
```bash
>show dbs
local      0.78125GB
test       0.23012GB
>
```


## How to manipulate it via Python ?

https://docs.mongodb.com/manual/tutorial/query-documents/
https://docs.mongodb.com/manual/reference/command/listDatabases/
https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/

```Python
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["db-name"]
mycol = mydb["collection-name"]

query_condition_filter = {}
query_return_filter = {
    "id": 1,
    "reviewState": 1,
    "kcsState": 1,
    "lastReviewedBy": 1,
    "sbr": 1,
    }

# This following query pramas are used like(meaning):
#    select <query_return_filter> from mycol where query_condition_filter
reviewed_kcs_cursor = mycol.find(query_condition_filter, query_return_filter)

reviewed_kcs_info = list(reviewed_kcs_cursor)

print(len(reviewed_kcs_info))
for x in reviewed_kcs_info:
  print(x)
```

## Mongo DB has no "show all" command.
https://newbiedba.wordpress.com/2016/06/01/mongodb-101-tips-how-to-view-current-configuration-on-a-running-system/

```bash
PostgreSQL => show all;
Oracle => show parameters;
```

In MongoDB, it is not as straightforward. You have to know what you want to look for exactly. The entire database configuration is not in a single place.

 - To get the configuration file that the current MongoDB instance is using, use `db.serverCmdLineOpts();` .
 - To get the current server parameters, use `db.runCommand( { getParameter : '*' } )` against the admin database in any replica set .
