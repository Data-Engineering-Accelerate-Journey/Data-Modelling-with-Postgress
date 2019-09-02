import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Retrieve song and artist info from a song file and insert the appropriate
    information in the song_table and artist_table

    Parameters
    ----------
    cur : 
        The database cursor
    filepath : string
        The file system path to a song files
    
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'artist_id', 'title', 'year',
                    'duration']].values
    print("Song data is: ", song_data[0].tolist())
    cur.execute(song_table_insert, song_data[0].tolist())
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location',
                      'artist_latitude', 'artist_longitude']].values
    cur.execute(artist_table_insert, artist_data[0].tolist())


def process_log_file(cur, filepath):
    """
    Retrieve time, user and songplay info from a logfile and insert the
    appropriate information in the time_table, user_table and songplay_table

    Parameters
    ----------
    cur : 
        The database cursor
    filepath : string
        The file system path to a log files
    
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # load time data 
    time_df = pd.DataFrame({'start_time':t.values, 'hour':t.dt.hour,
                            'day':t.dt.day, 'weekofyear':t.dt.weekofyear,
                            'month':t.dt.month,'year':t.dt.year,
                            'weekday':t.dt.weekday})

    #insert time records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        #print(song_select)
        #print("Find song, artist, length: <",row.song,"> <",row.artist,"> <",row.length,">")
        cur.execute(song_select, (row.song, row.artist, row.length))
        #print(songtitle_select, row.song)
        #cur.execute(songtitle_select, (row.song,))
        results = cur.fetchone()
        
        if results:
            #print("Found it!, song_id = ", song_id, " artist_id = ", artist_id)
            songid, artistid = results
            #print("Found song title! row.artist (artist name) is: ", row.artist, " artist_id is(from found): ", artistid, " duration: ", row.length)
            #print(results)
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts), row.userId, songid, artistid, row.level,
                         row.sessionId, row.location, row.userAgent)
        #print("Songplay Data is: ", songplay_data)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Retrieve filepaths for all song and logfiles and process all data
    in them and insert the relevant data into appropriate database tables

    Parameters
    ----------
    cur : 
        The database cursor
    conn:
        The connection to the database
    filepath : string
        The file system path to a log files
    func:
        The function to call to process the data for a given filetype
    
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb \
                            user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()