# Data Modelling with Postgress

## Table of Contents

1. [Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals](#discuss)
2. [State and justify your database schema design and ETL pipeline](#justify)
3. [Provide example queries and results for song play analysis](#optional-examples)
4. [Notes](#notes)

## <a name="discuss"></a>Discuss the purpose of this database
The purpose of this database is to provide Sparkify the necessary tool to retrieve vital, business oriented, information about their service. Their current main focus is to be able to, easily and fast, to retrieve information about which songs users are listening to. They do have information about this stored in logfiles already but it is not easy to search or aggregate data from these logfiles. In this assignment we have been asked to transform data from the logfiles together with meta data about songs (also stored in files) into a database design that will allow Sparkify to meet their business need related to finding out which songs their users are listening to.

## <a name="justify"></a>State and justify your database schema design and ETL pipeline
The requirements stated by Sparkify indicates that this is an OLAP oriented problem. Given that this is an OLAP oriented problem a Star Schema design seems to be appropriate. Star schemas are used by most if not all OLAP systems. A Star schema will make it relatively straight forward to optimize queries on song play analysis.

The timestamp is broken up into day, hour, week, month etc. and this will make it easy to extract data from specific days, months, hour of day etc

Since timestamp is probably not unique (it is possible that more than one user starts to play a song at the exact same time even if the timestamp is in ms) I decided not to use it as the primary key in the songplay_table even if the instructions given vaguely indicates that it should be used as the primary key.

## <a name="optional-examples"></a>Example queries
None provided due to time constraints :-)

## <a name="notes"></a>Notes
For data integrity purposes I would have liked to add foreign keys in order to add insert constrains across tables (i.e. not possible to add to the songplay_table if the artist_id or song_id is not present in the song and artist tables.). Due to the way the etl.ipynb I droppet this idea (i.e. the song_table and artist_table are not populated first and I get insert errors)

It also looks like that NextSong entires in the provided logfiles (log_data) does not match song data (in any data/song_data files). I.e. played songs (NextSong entires) in the logfiles does not have matching songs in the provided song data files. This results in that all entries in the songplay table is added without song_id and artist_id. This makes the created songplay table useless....