# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay_table;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song_table;"
artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
time_table_drop = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES

# It should probably have been PRIMARY KEY(songplay_id, user_id, song_id, artist_id) but due to incomplete data (i.e. the provided logfiles entries does not contain songs that are present in the song table after insertion of song data) it would render the songplay table empty
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay_table(
   songplay_id SERIAL PRIMARY KEY,
   start_time TIMESTAMP,
   user_id VARCHAR,
   song_id VARCHAR,
   artist_id VARCHAR,
   level VARCHAR,
   session_id INT,
   location VARCHAR,
   user_agent VARCHAR
);
""")


user_table_create = ("""
CREATE TABLE IF NOT EXISTS user_table(
   user_id VARCHAR PRIMARY KEY,
   first_name VARCHAR,
   last_name VARCHAR,
   gender VARCHAR,
   level VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song_table(
   song_id VARCHAR PRIMARY KEY,
   artist_id VARCHAR,
   title VARCHAR,
   year INT,
   duration NUMERIC(7,3)
);
""")

# The position is stated to be split into its elements (lat, long) but I will use POINT instead
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artist_table(
   artist_id VARCHAR PRIMARY KEY,
   artist_name VARCHAR,
   location VARCHAR,
   latitude NUMERIC(9,5),
   longitude NUMERIC(9,5)
);
""")

# It is a bit strange to vaste space in the database to store hour, date, week, ... since it is implicit part of the TIMESTAMP and easily deducted from it. 
time_table_create = ("""
CREATE TABLE IF NOT EXISTS time_table(
   start_time TIMESTAMP PRIMARY KEY,
   hour INT,
   day INT,
   week INT,
   month INT,
   year INT,
   weekday VARCHAR
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplay_table (start_time, user_id, song_id, artist_id, level, session_id, location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
INSERT INTO user_table(user_id, first_name, last_name, gender, level) VALUES (%s,%s,%s,%s,%s)  ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO song_table(song_id, artist_id, title, year, duration) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artist_table(artist_id, artist_name,location, latitude, longitude) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time_table(start_time, hour, day, week, month, year, weekday)  VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
""")

# FIND SONGS

# Implement the song_select to find the song ID and artist ID based on the title, artist name, and duration of a song.

song_select = ("""
SELECT song_table.song_id, artist_table.artist_id, song_table.duration FROM song_table JOIN artist_table ON song_table.artist_id=artist_table.artist_id WHERE song_table.title=%s AND artist_table.artist_name=%s AND song_table.duration=%s
""")

songtitle_select = ("""SELECT * FROM song_table WHERE title=%s""")
artist_select = ("""SELECT * FROM artist_table WHERE artist_id=%s""")

#MISC

table_def = ("""
SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'artist_table'
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, time_table_create, song_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]