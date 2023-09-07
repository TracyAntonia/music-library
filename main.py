import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import ForeignKey, Column, Integer, String

# A declarative Base for Inheritance
Base = declarative_base()

class User(Base):
    # Table name
    __tablename__ = 'users'
    # Columns(T.attributes)
    id = Column(Integer(), primary_key=True)
    userName = Column(String())
    email = Column(String())
    dateOfBirth = Column(Integer())
    
    def __repr__(self):
        return f'userName = {self.userName}'

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer(), primary_key=True, autoincrement=True)  # Auto-increment artist ID
    artistName = Column(String())
    creationDate = Column(Integer())
    
    def __repr__(self):
        return f'Artist(id={self.id}), artistName={self.artistName}'

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer(), primary_key=True)
    artist_id = Column(Integer(), ForeignKey('artists.id'))
    song_title = Column(String())
    duration = Column(Integer())
    creationDate = Column(Integer())  # Use an integer data type for creationDate

    # Define the relationship between Song and Artist
    artist = relationship("Artist", backref=backref("songs", cascade="all, delete-orphan"))

    def __repr__(self):
        return f'Song(id = {self.id}), song_title = {self.song_title}'

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    song_id = Column(Integer(), ForeignKey('songs.id'))
    timestamp = Column(Integer())
    
    def __repr__(self):
        return f'Favorite(id={self.id}), user_id={self.user_id}'
    
def create_artist(artist_name, creation_date):
    # Check if the artist exists; if not, create a new artist
    artist = session.query(Artist).filter(Artist.artistName == artist_name).first()
    if not artist:
        artist = Artist(artistName=artist_name, creationDate=creation_date)
    return artist
   
def create_playlist(songs):
    print("Create a Favorites Playlist")
    playlist_name = input("Enter the name of your favorites playlist: ")
    playlist = []

    # Display available songs
    print("Available songs:")
    for i, song in enumerate(songs, start=1):
        print(f"{i}. {song.song_title} by {song.artist.artistName}")

    while True:
        print("Add songs to your favorites playlist  (Enter 'done' to finish):")
        song_number = input("Enter the number of the song to add (or 'done' to finish): ")

        if song_number.lower() == 'done':
            break

        try:
            song_index = int(song_number) - 1
            if 0 <= song_index < len(songs):
                playlist.append(songs[song_index])
                print(f"Song '{songs[song_index].song_title}' added to the playlist.")
            else:
                print("Invalid song number.")
        except ValueError:
            print("Invalid input. Please enter a valid number or 'done'.")

    with open(f"{playlist_name}.txt", 'w') as playlist_file:
        for song in playlist:
            playlist_file.write(f"Song Title: {song.song_title}, Duration: {song.duration}\n")
    print(f"{playlist_name} playlist created!")

def delete_song_by_title(song_title):
    # Find and delete the song by title
    song = session.query(Song).filter(Song.song_title == song_title).first()
    if song:
        session.delete(song)
        session.commit()
        print(f"Song '{song_title}' has been deleted.")
    else:
        print("Song not found!")

def edit_playlist(playlist_name):
    print(f"Editing {playlist_name} Playlist")
    playlist = []

    # Load the existing playlist data
    try:
        with open(f"{playlist_name}.txt", 'r') as playlist_file:
            for line in playlist_file:
                parts = line.strip().split(', Duration: ')
                if len(parts) == 2:
                    song_title, duration = parts[0].split('Song Title: ')[1], parts[1]
                    playlist.append((song_title, duration))
    except FileNotFoundError:
        print("Playlist not found.")
        return

    while True:
        print("1) Add songs to the playlist")
        print("2) Remove songs from the playlist")
        print("3) Save and exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Add songs to the playlist (Enter 'done' to finish):")
            song_title = input("Enter the name of the song: ")
            if song_title.lower() == 'done':
                continue

            song_duration = input("Enter the duration of the song: ")
            playlist.append((song_title, song_duration))
            print(f"Song '{song_title}' added to the playlist.")
        elif choice == '2':
            print("Remove songs from the playlist (Enter 'done' to finish):")
            song_title = input("Enter the name of the song: ")
            if song_title.lower() == 'done':
                continue

            removed = False
            for song in playlist:
                if song[0] == song_title:
                    playlist.remove(song)
                    removed = True
                    print(f"Song '{song_title}' removed from the playlist.")
                    break

            if not removed:
                print("Song not found in the playlist.")
        elif choice == '3':
            with open(f"{playlist_name}.txt", 'w') as playlist_file:
                for song in playlist:
                    playlist_file.write(f"Song Title: {song[0]}, Duration: {song[1]}\n")
            print(f"{playlist_name} playlist updated and saved.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def delete_playlist(playlist_name):
    try:
        # Remove the playlist file
        os.remove(f"{playlist_name}.txt")
        print(f"Playlist '{playlist_name}' has been deleted.")
    except FileNotFoundError:
        print("Playlist not found.")


if __name__ == '__main__':
    engine = create_engine('sqlite:///tracker.db')
    Base.metadata.create_all(engine)

    # Use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # Use 'Session' class to create 'session' object
    session = Session()

    def create_artist(artist_name):
        # Check if the artist exists; if not, create a new artist
        artist = session.query(Artist).filter(Artist.artistName == artist_name).first()
        if not artist:
            artist = Artist(artistName=artist_name, creationDate=None)  # You can set the creation date as needed
        return artist

    def main():
        choice = 0
        while choice != 7:
            print("**<<KARIBU||WELCOME TO BOOMBOX MUSIC LIBRARY>>**")
            print("1) Add Song")
            print("2) Search Song")
            print("3) Create a Favorites playlist")
            print("4) Display Songs")
            print("5) Display Artists")
            print("6) Edit Playlist or Delete Song")
            print("7) Delete Playlist")
            print("8) Quit program")
            choice = int(input("Enter your choice: "))

            # Adds song details
            if choice == 1:
                print("**<<Adding a Song...>>**")
                song_title = input("Enter the name of the song: ")
                artist_name = input("Enter the name of the artist: ")
                duration = input("Enter the duration of the song: ")
                creation_date = input("Enter the creation date of the song as an integer: ")

                # Convert the creation date to an integer
                try:
                    creation_date = int(creation_date)
                except ValueError:
                    print("Invalid integer format for the creation date.")
                    continue

                # Create a new artist or retrieve an existing one
                artist = create_artist(artist_name)

                # Create a new Song record in the database
                new_song = Song(song_title=song_title, duration=duration, artist=artist, creationDate=creation_date)
                session.add(new_song)
                session.commit()

            # Search for a song
            elif choice == 2:
                print("**<<Searching for a song...>>**")
                keyword = input("Enter name: ")

                # Query songs based on the keyword
                songs = session.query(Song).filter(Song.song_title.ilike(f"%{keyword}%")).all()

                if songs:
                    print("Search results:")
                    for song in songs:
                        print(f"Song Title: {song.song_title}, Artist: {song.artist.artistName}, Duration: {song.duration}")
                else:
                    print("Song not found!")

            # Create a Favorites playlist
            elif choice == 3:
                print("**<<Creating a Favourites Playlist...>>**")
                # Pass the list of songs to the create_playlist function
                create_playlist(session.query(Song).all())

            # Display Songs
            elif choice == 4:
                print("**<<Displaying Songs...>>**")
                songs = session.query(Song).all()
                if songs:
                    for song in songs:
                        print(f"Song Title: {song.song_title}, Artist: {song.artist.artistName}, Duration: {song.duration}, Creation Date: {song.creationDate}")
                else:
                    print("No songs in the library.")

            # Display Artists
            elif choice == 5:
                print("**<<Displaying Artists...>>**")
                artists = session.query(Artist).all()
                for artist in artists:
                    print(f"Artist Name: {artist.artistName}, Creation Date: {artist.creationDate}")

            # Edit Playlist or Delete Song
            elif choice == 6:
                print("**<<Editing a Playlist or Deleting a Song...>>**")
                print("1) Edit Playlist")
                print("2) Delete Song by Title")
                sub_choice = int(input("Enter your choice: "))

                if sub_choice == 1:
                    playlist_name = input("Enter the name of the playlist to edit: ")
                    edit_playlist(playlist_name)
                elif sub_choice == 2:
                    song_title = input("Enter the title of the song to delete: ")
                    delete_song_by_title(song_title)
                else:
                    print("Invalid choice. Please select 1 or 2.")

            # Inside your main function, add this block for the new option
            elif choice == 7:
                print("**<<Deleting a Playlist...>>**")
                playlist_name = input("Enter the name of the playlist to delete: ")
                delete_playlist(playlist_name)
                    

            # Quit program
            elif choice == 8:
                print("**<<You are no longer on the main menu.>>**")
                print("**<<Thank you for choosing BOOMBOX MUSIC LIBRARY.>>**")
                print("**<<Run the program again to get back to the main menu.>>**")

            # Unrecognized input and validates user's input
            else:
                print("*<<Incorrect Input.>>**")

    if __name__ == "__main__":
        main()




















# import sqlite3
# from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref, sessionmaker
# from sqlalchemy import ForeignKey, Column, Integer, String, Date

# # A declarative Base for Inheritance
# Base = declarative_base()

# class User(Base):
#     # Table name
#     __tablename__ = 'users'
#     # Columns(T.attributes)
#     id = Column(Integer(), primary_key=True)
#     userName = Column(String())
#     email = Column(String())
#     dateOfBirth = Column(Integer())
    
#     def __repr__(self):
#         return f'userName = {self.userName}'

# class Artist(Base):
#     __tablename__ = 'artists'
#     id = Column(Integer(), primary_key=True, autoincrement=True)  # Auto-increment artist ID
#     artistName = Column(String())
#     creationDate = Column(Integer())
    
#     def __repr__(self):
#         return f'Artist(id={self.id}), artistName={self.artistName}'

# class Song(Base):
#     __tablename__ = 'songs'
#     id = Column(Integer(), primary_key=True)
#     artist_id = Column(Integer(), ForeignKey('artists.id'))
#     song_title = Column(String())
#     duration = Column(Integer())
#     creationDate = Column(Integer())  # Add the creationDate column of type Date

#     # Define the relationship between Song and Artist
#     artist = relationship("Artist", backref=backref("songs", cascade="all, delete-orphan"))

#     def __repr__(self):
#         return f'Song(id = {self.id}), song_title = {self.song_title}'


# class Favorite(Base):
#     __tablename__ = 'favorites'
#     id = Column(Integer(), primary_key=True)
#     user_id = Column(Integer(), ForeignKey('users.id'))
#     song_id = Column(Integer(), ForeignKey('songs.id'))
#     timestamp = Column(Integer())
    
#     def __repr__(self):
#         return f'Favorite(id={self.id}), user_id={self.user_id}'

# def create_playlist(songs):
#     print("Create a Favorites Playlist")
#     playlist_name = input("Enter the name of your favorites playlist: ")
#     playlist = []

#     while True:
#         print("Add songs to your favorites playlist  (Enter 'done' to finish):")
#         song_title = input("Enter the name of the song: ")
#         if song_title.lower() == 'done':
#             break
#         for song in songs:
#             if song_title in song.song_title:
#                 playlist.append(song)
#         else:
#             print("Song not found in the library.")

#     with open(f"{playlist_name}.txt", 'w') as playlist_file:
#         for song in playlist:
#             playlist_file.write(f"Song Title: {song.song_title}, Duration: {song.duration}\n")
#     print(f"{playlist_name} playlist created!")

# def delete_song_by_title(song_title):
#     # Find and delete the song by title
#     song = session.query(Song).filter(Song.song_title == song_title).first()
#     if song:
#         session.delete(song)
#         session.commit()
#         print(f"Song '{song_title}' has been deleted.")
#     else:
#         print("Song not found!")

# def edit_playlist(playlist_name):
#     print(f"Editing {playlist_name} Playlist")
#     playlist = []

#     # Load the existing playlist data
#     try:
#         with open(f"{playlist_name}.txt", 'r') as playlist_file:
#             for line in playlist_file:
#                 parts = line.strip().split(', Duration: ')
#                 if len(parts) == 2:
#                     song_title, duration = parts[0].split('Song Title: ')[1], parts[1]
#                     playlist.append((song_title, duration))
#     except FileNotFoundError:
#         print("Playlist not found.")
#         return

#     while True:
#         print("1) Add songs to the playlist")
#         print("2) Remove songs from the playlist")
#         print("3) Save and exit")
#         choice = input("Enter your choice: ")

#         if choice == '1':
#             print("Add songs to the playlist (Enter 'done' to finish):")
#             song_title = input("Enter the name of the song: ")
#             if song_title.lower() == 'done':
#                 continue

#             song_duration = input("Enter the duration of the song: ")
#             playlist.append((song_title, song_duration))
#             print(f"Song '{song_title}' added to the playlist.")
#         elif choice == '2':
#             print("Remove songs from the playlist (Enter 'done' to finish):")
#             song_title = input("Enter the name of the song: ")
#             if song_title.lower() == 'done':
#                 continue

#             removed = False
#             for song in playlist:
#                 if song[0] == song_title:
#                     playlist.remove(song)
#                     removed = True
#                     print(f"Song '{song_title}' removed from the playlist.")
#                     break

#             if not removed:
#                 print("Song not found in the playlist.")
#         elif choice == '3':
#             with open(f"{playlist_name}.txt", 'w') as playlist_file:
#                 for song in playlist:
#                     playlist_file.write(f"Song Title: {song[0]}, Duration: {song[1]}\n")
#             print(f"{playlist_name} playlist updated and saved.")
#             break
#         else:
#             print("Invalid choice. Please select 1, 2, or 3.")

# if __name__ == '__main__':
#     engine = create_engine('sqlite:///tracker.db')
#     Base.metadata.create_all(engine)

#     # Use our engine to configure a 'Session' class
#     Session = sessionmaker(bind=engine)
#     # Use 'Session' class to create 'session' object
#     session = Session()

#     def create_artist(artist_name):
#         # Check if the artist exists; if not, create a new artist
#         artist = session.query(Artist).filter(Artist.artistName == artist_name).first()
#         if not artist:
#             artist = Artist(artistName=artist_name, creationDate=None)  # You can set the creation date as needed
#         return artist

#     def main():
#         choice = 0
#         while choice != 7:
#             print("**<<KARIBU||WELCOME TO BOOMBOX MUSIC LIBRARY>>**")
#             print("1) Add Song")
#             print("2) Search Song")
#             print("3) Create a Favorites playlist")
#             print("4) Display Songs")
#             print("5) Display Artists")
#             print("6) Edit Playlist or Delete Song")
#             print("7) Quit program")
#             choice = int(input("Enter your choice: "))

#             # Adds song details
#             if choice == 1:
#                 print("**<<Adding a Song...>>**")
#                 song_title = input("Enter the name of the song: ")
#                 artist_name = input("Enter the name of the artist: ")
#                 duration = input("Enter the duration of the song: ")
#                 creation_date = input("Enter the creation date of the song (YYYY/MM/DD): ")

#                 try:
#                     creation_date = datetime.strptime(creation_date, "%Y-%m-%d").date()  # Corrected date format
#                 except ValueError:
#                     print("Invalid date format. Use YYYY-MM-DD.")
#                 continue

#                 # Create a new artist or retrieve an existing one
#                 artist = create_artist(artist_name)

#                 # Create a new Song record in the database
#                 new_song = Song(song_title=song_title, duration=duration, artist=artist, creationDate=creation_date)
#                 session.add(new_song)
#                 session.commit()


#             # Search for a song
#             elif choice == 2:
#                 print("**<<Searching for a song...>>**")
#                 keyword = input("Enter name: ")

#                 # Query songs based on the keyword
#                 songs = session.query(Song).filter(Song.song_title.ilike(f"%{keyword}%")).all()

#                 if songs:
#                     print("Search results:")
#                     for song in songs:
#                         print(f"Song Title: {song.song_title}, Artist: {song.artist.artistName}, Duration: {song.duration}")
#                 else:
#                     print("Song not found!")

#             # Create a Favorites playlist
#             elif choice == 3:
#                 print("**<<Creating a Favourites Playlist...>>**")
#                 # Pass the list of songs to the create_playlist function
#                 create_playlist(session.query(Song).all())

#             # Display Songs
#             elif choice == 4:
#                 print("**<<Displaying Songs...>>**")
#                 songs = session.query(Song).all()
#                 if songs:
#                     for song in songs:
#                         print(f"Song Title: {song.song_title}, Artist: {song.artist.artistName}, Duration: {song.duration}")
#                 else:
#                     print("No songs in the library.")

#             # Display Artists
#             elif choice == 5:
#                 print("**<<Displaying Artists...>>**")
#                 artists = session.query(Artist).all()
#                 for artist in artists:
#                     print(f"Artist Name: {artist.artistName}, Creation Date: {artist.creationDate}")

#             # Edit Playlist or Delete Song
#             elif choice == 6:
#                 print("**<<Editing a Playlist or Deleting a Song...>>**")
#                 print("1) Edit Playlist")
#                 print("2) Delete Song by Title")
#                 sub_choice = int(input("Enter your choice: "))

#                 if sub_choice == 1:
#                     playlist_name = input("Enter the name of the playlist to edit: ")
#                     edit_playlist(playlist_name)
#                 elif sub_choice == 2:
#                     song_title = input("Enter the title of the song to delete: ")
#                     delete_song_by_title(song_title)
#                 else:
#                     print("Invalid choice. Please select 1 or 2.")

#             # Quit program
#             elif choice == 7:
#                 print("**<<You are no longer on the main menu.>>**")
#                 print("**<<Thank you for choosing BOOMBOX MUSIC LIBRARY.>>**")
#                 print("**<<Run the program again to get back to the main menu.>>**")

#             # Unrecognized input and validates user's input
#             else:
#                 print("*<<Incorrect Input.>>**")

#     if __name__ == "__main__":
#         main()















# import sqlite3
# from sqlalchemy import create_engine, func
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref, sessionmaker
# from sqlalchemy import ForeignKey, Column, Integer, String

# # A declarative Base for Inheritance
# Base = declarative_base()

# class User(Base):
#     # Table name
#     __tablename__ = 'users'
#     # Columns(T.attributes)
#     id = Column(Integer(), primary_key=True)
#     userName = Column(String())
#     email = Column(String())
#     dateOfBirth = Column(Integer())
    
#     def __repr__(self):
#         return f'userName = {self.userName}'

# class Artist(Base):
#     __tablename__ = 'artists'
#     id = Column(Integer(), primary_key=True, autoincrement=True)  # Auto-increment artist ID
#     artistName = Column(String())
#     creationDate = Column(Integer())
    
#     def __repr__(self):
#         return f'Artist(id = {self.id}), artistName = {self.artistName}'

# class Song(Base):
#     __tablename__ = 'songs'
#     id = Column(Integer(), primary_key=True)
#     artist_id = Column(Integer(), ForeignKey('artists.id'))
#     song_title = Column(String())
#     duration = Column(Integer())

#     # Define the relationship between Song and Artist
#     artist = relationship("Artist", backref=backref("songs", cascade="all, delete-orphan"))

#     def __repr__(self):
#         return f'Song(id = {self.id}), song_title = {self.song_title}'

# class Favorite(Base):
#     __tablename__ = 'favorites'
#     id = Column(Integer(), primary_key=True)
#     user_id = Column(Integer(), ForeignKey('users.id'))
#     song_id = Column(Integer(), ForeignKey('songs.id'))
#     timestamp = Column(Integer())
    
#     def __repr__(self):
#         return f'Favorite(id = {self.id}), user_id = {self.user_id}'

# def create_playlist(songs):
#     print("Create a Favorites Playlist")
#     playlist_name = input("Enter the name of your favorites playlist: ")
#     playlist = []

#     while True:
#         print("Add songs to your favorites playlist  (Enter 'done' to finish):")
#         song_title = input("Enter the name of the song: ")
#         if song_title.lower() == 'done':
#             break
#         for song in songs:
#             if song_title in song.song_title:
#                 playlist.append(song)
#         else:
#             print("Song not found in the library.")

#     with open(f"{playlist_name}.txt", 'w') as playlist_file:
#         for song in playlist:
#             playlist_file.write(f"Song Title: {song.song_title}, Duration: {song.duration}\n")
#     print(f"{playlist_name} playlist created!")

# def delete_song_by_title(song_title):
#     # Find and delete the song by title
#     song = session.query(Song).filter(Song.song_title == song_title).first()
#     if song:
#         session.delete(song)
#         session.commit()
#         print(f"Song '{song_title}' has been deleted.")
#     else:
#         print("Song not found!")

# def edit_playlist(playlist_name):
#     print(f"Editing {playlist_name} Playlist")
#     playlist = []

#     # Load the existing playlist data
#     try:
#         with open(f"{playlist_name}.txt", 'r') as playlist_file:
#             for line in playlist_file:
#                 parts = line.strip().split(', Duration: ')
#                 if len(parts) == 2:
#                     song_title, duration = parts[0].split('Song Title: ')[1], parts[1]
#                     playlist.append((song_title, duration))
#     except FileNotFoundError:
#         print("Playlist not found.")
#         return

#     while True:
#         print("1) Add songs to the playlist")
#         print("2) Remove songs from the playlist")
#         print("3) Save and exit")
#         choice = input("Enter your choice: ")

#         if choice == '1':
#             print("Add songs to the playlist (Enter 'done' to finish):")
#             song_title = input("Enter the name of the song: ")
#             if song_title.lower() == 'done':
#                 continue

#             song_duration = input("Enter the duration of the song: ")
#             playlist.append((song_title, song_duration))
#             print(f"Song '{song_title}' added to the playlist.")
#         elif choice == '2':
#             print("Remove songs from the playlist (Enter 'done' to finish):")
#             song_title = input("Enter the name of the song: ")
#             if song_title.lower() == 'done':
#                 continue

#             removed = False
#             for song in playlist:
#                 if song[0] == song_title:
#                     playlist.remove(song)
#                     removed = True
#                     print(f"Song '{song_title}' removed from the playlist.")
#                     break

#             if not removed:
#                 print("Song not found in the playlist.")
#         elif choice == '3':
#             with open(f"{playlist_name}.txt", 'w') as playlist_file:
#                 for song in playlist:
#                     playlist_file.write(f"Song Title: {song[0]}, Duration: {song[1]}\n")
#             print(f"{playlist_name} playlist updated and saved.")
#             break
#         else:
#             print("Invalid choice. Please select 1, 2, or 3.")
  

# if __name__ == '__main__':
#     engine = create_engine('sqlite:///tracker.db')
#     Base.metadata.create_all(engine)

#     # Use our engine to configure a 'Session' class
#     Session = sessionmaker(bind=engine)
#     # Use 'Session' class to create 'session' object
#     session = Session()

#     def create_artist(artist_name):
#         # Check if the artist exists; if not, create a new artist
#         artist = session.query(Artist).filter(Artist.artistName == artist_name).first()
#         if not artist:
#             artist = Artist(artistName=artist_name, creationDate=None)  # You can set the creation date as needed
#         return artist

#     def main():
#         choice = 0
#         while choice != 7:
#             print("**<<KARIBU||WELCOME TO BOOMBOX MUSIC LIBRARY>>**")
#             print("1) Add Song")
#             print("2) Search Song")
#             print("3) Create a Favorites playlist")
#             print("4) Display Songs")
#             print("5) Display Artists")
#             print("7) Quit program")
#             choice = int(input())

#             # Adds song details
#             if choice == 1:
#                 print("**<<Adding a Song...>>**")
#                 song_title = input("Enter the name of the song: ")
#                 artist_name = input("Enter the name of the artist: ")
#                 duration = input("Enter the duration of the song: ")

#                 # Create a new artist or retrieve an existing one
#                 artist = create_artist(artist_name)

#                 # Create a new Song record in the database
#                 new_song = Song(song_title=song_title, duration=duration, artist=artist)
#                 session.add(new_song)
#                 session.commit()

#             # Search for a song
#             elif choice == 2:
#                 print("**<<Searching for a song...>>**")
#                 keyword = input("Enter name....")

#                 # Query songs based on the keyword
#                 songs = session.query(Song).filter(Song.song_title.ilike(f"%{keyword}%")).all()

#                 if songs:
#                     for song in songs:
#                         print(f"Song Title: {song.song_title}, Duration: {song.duration}")
#                 else:
#                     print("Song not found!")

#             # Create a Favorites playlist
#             elif choice == 3:
#                 print("**<<Creating a Favourites Playlist...>>**")
#                 # Pass the list of songs to the create_playlist function
#                 create_playlist(session.query(Song).all())

#             # Display Songs
#             elif choice == 4:
#                 print("**<<Displaying Songs...>>**")
#                 songs = session.query(Song).all()
#                 for song in songs:
#                     print([f"Song Title: {song.song_title}, Duration: {song.duration}"])

#             # Display Artists
#             elif choice == 5:
#                 print("**<<Displaying Artists...>>**")
#                 artists = session.query(Artist).all()
#                 for artist in artists:
#                     print(f"Artist Name: {artist.artistName}, Creation Date: {artist.creationDate}")

#             elif choice == 6:
#                 print("**<<Editing or Deleting a Song...>>**")
#                 print("1) Edit Playlist")
#                 print("2) Delete Song")
#                 sub_choice = int(input("Enter your choice: "))

#                 if sub_choice == 1:
#                     playlist_name = input("Enter the name of the playlist to edit: ")
#                     edit_playlist(playlist_name)
#                 elif sub_choice == 2:
#                     song_id = int(input("Enter the ID of the song to delete: "))
#                     delete_song(song_title)
#                 else:
#                     print("Invalid choice. Please select 1 or 2.")
#             # Quit program
#             elif choice == 7:
#                 print("**<<You are no longer on the main menu.>>**")
#                 print("**<<Thank you for choosing BOOMBOX MUSIC LIBRARY.>>**")
#                 print("**<<Run the program again to get back to the main menu.>>**")

#             # Unrecognized input and validates user's input
#             else:
#                 print("*<<Incorrect Input.>>**")


#     if __name__ == "__main__":
#         main()























# Working CODE
# import sqlite3
# from sqlalchemy import create_engine, func
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref, sessionmaker
# from sqlalchemy import ForeignKey, Column, Integer, String

#  # A declarative Base for Inheritance
# Base = declarative_base()
# class User(Base):
# # Table name
#     __tablename__ = 'users'
# # Columns(T.attributes)
#     id = Column (Integer(), primary_key= True)
#     userName = Column(String())
#     email = Column(String())
#     dateOfBirth = Column(Integer())
#     # users = relationship ('User', backref=backref('budget'))
# # respresentation of class objects as strings
#     def __repr__(self):
#         return f'userName= {self.userName}'

# class Artist(Base):
#     __tablename__ = 'artists'
#     id = Column(Integer(), primary_key=True, autoincrement=True)
#     artistName = Column(String())
#     creationDate = Column(Integer())

#     def __repr__(self):
#         return f'Artist(id = {self.id}), artistName = {self.artistName}'
    
# # class Artist(Base):
# #     __tablename__ = 'artists'
# #     id = Column (Integer(), primary_key=True)
# #     song_id = Column(Integer())
# #     artistName = Column(String())
# #     creationDate = Column(Integer())
# #     # artists = relationship('Artist', backref=backref('song'))
# #     def __repr__(self):
# #         return f'Artist(id = {self.id})'+\
# #            f'artistName ={self.artistName}'
   
# class Song(Base):
#     __tablename__ = 'songs'
#     id = Column(Integer(), primary_key= True)
#     artist_id = Column(Integer(), ForeignKey('artists.id'))
#     song_title = Column(String())
#     duration = Column(Integer())
#     def __repr__(self):
#         return f'Song(id = {self.id})'+\
#            f'song_titlr= {self.song_title}'
   
# class Favorite(Base):
#     __tablename__ = 'favorites'
#     id = Column (Integer(), primary_key=True)
#     user_id = Column(Integer(), ForeignKey('users.id'))
#     song_id = Column(Integer(), ForeignKey('songs.id'))
#     timestamp = Column(Integer())
#     def __repr__(self):
#         return f'Favorite(id = {self.id})'+\
#            f'user_id={self.user_id}'
       


# if __name__ == '__main__':
#     engine = create_engine('sqlite:///tracker.db')
#     Base.metadata.create_all(engine)
#      # use our engine to configure a 'Session' class
#     Session = sessionmaker(bind=engine)
#     # use 'Session' class to create 'session' object
#     session = Session()
    

# def add_song(session, artist_id, song_title, duration):
#     # Create a new Song instance
#     song = Song(artist_id=artist_id, song_title=song_title, duration=duration)
    
#     # Add the song to the session
#     session.add(song)
    
#     # Commit the changes to the database
#     session.commit()


# # User Instances
#     user1 = User(
#         userName = "Alvin",
#         email = "alvinbee@gmail.com",
#         dateOfBirth = "2/2/2010"
#         )
#     user2 = User(
#         userName = "Alvin",
#         email = "alvinbee@gmail.com",
#         dateOfBirth = "2/2/2010"
#         )
#     user3 = User(
#         userName = "Alvin",
#         email = "alvinbee@gmail.com",
#         dateOfBirth = "2/2/2010"
#         )
   
#     # Create Artist(Instances)
#     artist1 = Artist(
#         song_id = 1,
#         artistName = "Alvin",
#         creationDate = "12/03/2004"
#         )
#     artis2 = Artist(
#         song_id = 1,
#         artistName = "Alvin",
#         creationDate = "12/03/2004"
#         )
   
#     # Create Song(Instances)
#     song1 = Song(
#         artist_id = 1,
#         song_title = "Can I be Him ",
#         duration = 10,
#         )
#     song2 = Song(
#         artist_id = 1,
#         song_title = "Can I be Him ",
#         duration = 10,
#         )
#     # Create Favorites(Instances)
#     favorite1 = Favorite(
#         user_id = 1,
#         song_id = 1,
#         timestamp = "6/09/2023",
#         )

#     favorite2 = Favorite(
#         user_id = 1,
#         song_id = 2,
#         timestamp = "6/09/2023",
#         )

# #Saving  the session in the database and applying the committed modifications
#     session.add_all([user1,user2,user3])
#     session.add_all([artist1,artis2])
#     session.add_all([song1,song2])
#     session.add_all([favorite1,favorite2])

#     session.commit()

# def create_playlist(songs):
#     print("Create a Favorites Playlist")
#     playlist_name = input("Enter the name of your favorites playlist: ")
#     playlist = []

#     while True:
#         print("Add songs to your favorites playlist  (Enter 'done' to finish):")
#         song_title = input("Enter the name of the song: ")
#         if song_title.lower() == 'done':
#             break
#         for song in songs:
#             if song_title in song.song_title:
#                 playlist.append(song.song_title)

#     with open(f"{playlist_name}.txt", 'w') as playlist_file:
#         for song in playlist:
#             playlist_file.write(song + "\n")
#     print(f"{playlist_name} playlist created!")

# # def create_playlist(songs):
# #         print("Create a Favorites Playlist")
# #         playlist_name = input("Enter the name of your favorites playlist: ")
# #         playlist = []

# #         while True:
# #             print("Add songs to your favorites playlist  (Enter 'done' to finish):")
# #             song_title = input("Enter the name of the song: ")
# #             if song_title.lower() == 'done':
# #                 break
# #             for song in songs:
# #                 if song_title in song:
# #                     playlist.append(song)
# #             else:
# #                 print("Song not found in library.")

# #         with open(f"{playlist_name}.txt", 'w') as playlist_file:
# #             for song in playlist:
# #                 playlist_file.write(",".join(song) + "\n")
# #         print(f"{playlist_name} playlist created!")                        


# def main ():
#     # initialize music list
#     # trackerList = []

#     choice = 0
#     while choice !=7:
#         print("**<<KARIBU||WELCOME TO BOOMBOX MUSIC LIBRARY>>**")
#         print("1) Add Song")
#         print("2) Search Song ")
#         print("3) Create a Favorites playlist")
#         print("4) Display Songs")
#         print("5) Display Artist")
#         # print("6) Display limit 10000 and above")
#         print("7) Quit program")
#         choice = int(input())


# #   Adds song details
#         if choice == 1:
#             print("**<<Adding a Song...>>**")
#             artist_id = int(input("Enter the artist's ID: "))  # Assuming you have artist ID available
#             song_title = input("Enter the name of the song: ")
#             duration = int(input("Enter the duration of the song in seconds: "))
#             add_song(session, artist_id, song_title, duration)
#             # song_title = input("Enter the name of the song....")
#             # duration= input("Enter the duration of the song....")
#             # Song.append([song_title, duration])



# #   Search for a song
#         elif choice == 2:
#             print("**<<Searching for a song...>>**")
#             keyword = input("Enter name....")  

#             # Query songs based on the keyword
#             songs = session.query(Song).filter(Song.song_title.ilike(f"%{keyword}%")).all()

#             if songs:
#                 for song in songs:
#                     print(f"Song Title: {song.song_title}, Duration: {song.duration}")
#             else:
#                 print("Song not found!")

#             # for song in Song:
#             #     if keyword in song:
#             #         print(song)
#             #     else:
#             #         print("Song not found!")  

# #   Prints a Tuple
#         elif choice == 3:
#             print("**<<Creating a Favourites Playlist...>>**")
#             # create_playlist(Song)

#               # Pass the list of songs to the create_playlist function
#             create_playlist(session.query(Song).all())

# #  prints average limit
#         elif choice == 4:
#             print("**<<Displaying Songs...>>**")
#             songs = session.query(Song).all()
#             # for i in range(len(Song)):
#             #      print(Song[i])
#             for song in songs:
#                 print(f"Song Title: {song.song_title}, Duration: {song.duration}")

# #  displays artists
#         elif choice == 5:
#                 print("**<<Displaying Artists...>>**")
#                 # for i in range(len(Artist)):
#                 #      print(Artist[i])
#                 artists = session.query(Artist).all()
#                 for artist in artists:
#                     print(f"Artist Name: {artist.artistName}, Creation Date: {artist.creationDate}")


   
# # #  prints limit 10000 and above
# #         elif choice == 6:
# #             budgets = session.query(Budget).filter(Budget.limit >= 10000)
# #             for budget in budgets:
# #                 print("**<<Printing limit 10000 and above>>**")
# #                 print(budget.budgetName)
       
# #  Quiting program
#         elif choice == 7:
#                 print("**<<You are no longer on the main menu.>>**")
#                 print("**<<Thank you for choosing BOOMBOX MUSIC LIBRARY.>>**")
#                 print("**<<Run the program again to get back to the main menu.>>**")

# #  Unrecognized input and validates user's input
#         else:
#                 print("*<<Incorrect Input.>>**")
               
               
# # Calling the function
# if __name__ == "__main__":
#     main()


















# # Import necessary modules
# import sqlite3
# from sqlalchemy import create_engine, func
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref, sessionmaker
# from sqlalchemy import ForeignKey, Column, Integer, String 

#  # A declarative Base for Inheritance
# Base = declarative_base()
# class User(Base):
# # Table name
#     __tablename__ = 'users'
# # Columns(T.attributes)
#     user_id = Column (Integer(), primary_key= True)
#     userName = Column(String())
#     email = Column(String())
#     dateOfBirth = Column(Integer())
#     # users = relationship ('User', backref=backref('favourites'))
#     # respresentation of class objects as strings
#     def __repr__(self):
#         return f'userName= {self.userName}'
           
# class Artist(Base):
#     __tablename__ = 'artists'
#     artist_id = Column (Integer(), primary_key=True)
#     song_id = Column(Integer())
#     artistName = Column(String())
#     creationDate = Column(Integer())
#     def __repr__(self):
#         return f'Artist(id = {self.id})'+\
#            f'artistName ={self.artistName}'
    
# class Song(Base):
#     __tablename__ = 'songs'
#     song_id = Column(Integer(), primary_key= True)
#     artist_id = Column(Integer(), ForeignKey('artist_id'))
#     songTitle = Column(Integer())
#     duration = Column(Integer())
#     def __repr__(self):
#         return f'Song(id = {self.id})'+\
#            f'songTitle= {self.songTitle}'
    
# class Favorite(Base):
#     __tablename__ = 'favorites'
#     favorite_id = Column (Integer(), primary_key=True)
#     user_id = Column(Integer(), ForeignKey('user_id'))
#     song_id = Column(Integer(), ForeignKey('song_id'))
#     timestamp = Column(Integer())
#     def __repr__(self):
#         return f'Favorite(id = {self.id})'+\
#            f'user_id={self.user_id}'
        


# if __name__ == '__main__':
#     engine = create_engine('sqlite:///tracker.db')
#     Base.metadata.create_all(engine)
#      # use our engine to configure a 'Session' class
#     Session = sessionmaker(bind=engine)
#     # use 'Session' class to create 'session' object
#     session = Session()
#     # User Instances
#     user1 = User(
#         userName = "Alvin",
#         email = "alvinbee@gmail.com",
#         dateOfBirth = "2/2/2010"
#         )
#     user2 = User(
#         userName = "Roman",
#         email = "romanie24@gmail.com",
#         dateOfBirth = "12/2/2000"
#         )
#     user3 = User(
#         userName = "Grace",
#         email = "gracewalker@gmail.com",
#         dateOfBirth = "20/05/2005"
#         )
   
#     # Create Artist(Instances)
#     artist1 = Artist(
#         song_id = 1,
#         artistName = "Alvin",
#         creationDate = "12/03/2004"
#         )
#     artist2 = Artist(
#         song_id = 1,
#         artistName = "Shawn Mendes",
#         creationDate = "23/11/2014"
#         )
#     artist3 = Artist(
#         song_id = 1,
#         artistName = "Billie Eilish",
#         creationDate = "05/06/2020"
#         )
   
#     # Create Song(Instances)
#     song1 = Song(
#         artist_id = 1,
#         song_title = "Can I be Him ",
#         duration = 10,
#         )
#     song2 = Song(
#         artist_id = 1,
#         song_title = "Bruises",
#         duration = 4,
#     )
#     song3 = Song(
#         artist_id = 1,
#         song_title = "Ocean Eyes",
#         duration = 2,
#     )
    
#     # Create Favorites(Instances)
#     favorite1 = Favorite(
#         user_id = 1,
#         song_id = 1,
#         timestamp = "6/09/2023",
#         )
#     favorite2 = Favorite(
#         user_id = 2,
#         song_id = 1,
#         timestamp = "6/09/2023",
#         )
#     favorite3 = Favorite(
#         user_id = 3,
#         song_id = 1,
#         timestamp = "6/09/2023",
#         )

# #Saving  the session in the database and applying the committed modifications
#     session.add_all([user1,user2,user3])
#     session.add_all([artist1, artist2, artist3])
#     session.add_all([song1,song2,song3])
#     session.add_all([favorite1,favorite2,favorite3])
#     session.commit()


# def create_playlist(songs):
#         print("Create a Favorites Playlist")
#         playlist_name = input("Enter the name of your favorites playlist: ")
#         playlist = []

#         while True:
#             print("Add songs to your favorites playlist  (Enter 'done' to finish):")
#             song_title = input("Enter the name of the song: ")
#             if song_title.lower() == 'done':
#                 break
#             for song in songs:
#                 if song_title in song:
#                     playlist.append(song)
#             else:
#                 print("Song not found in library.")

#         with open(f"{playlist_name}.txt", 'w') as playlist_file:
#             for song in playlist:
#                 playlist_file.write(",".join(song) + "\n")
#         print(f"{playlist_name} playlist created!")                        


# def main ():
#     # initialize music list
#     # musicList = []

#     choice = 0
#     while choice !=6:
#         print("**<<KARIBU||WELCOME TO BOOMBOX MUSIC LIBRARY>>**")
#         print("1) Add Song")
#         print("2) Search Song ")
#         print("3) Create a Favorites playlist")
#         print("4) Display Songs")
#         print("5) Display Artist")
#         print("6) Quit program")
#         choice = int(input())


# #   Adds song details
#         if choice == 1:
#             print("**<<Adding a Song...>>**")
#             songTitle = input("Enter the name of the song....")
#             duration= input("Enter the duration of the song....")
#             Song.append([songTitle, duration])

# #   Search for a song
#         elif choice == 2:
#             print("**<<Searching for a song...>>**")
#             keyword = input("Enter name....")   
#             for song in Song:
#                 if keyword in song:
#                     print(song)
#                 else:
#                     print("Song not found!")  

# #   Creates a playlist
#         elif choice == 3:
#             print("**<<Creating a Favourites Playlist...>>**")
#             create_playlist(Song)

# #  Displays the songs
#         elif choice == 4:
#             print("**<<Displaying Songs...>>**")
#             for i in range(len(Song)):
#                  print(Song[i])

# #  Displays the artists in the library
#         elif choice == 5:
#                 print("**<<Displaying Artists...>>**")
#                 for i in range(len(Artist)):
#                      print(Artist[i])

    
# #  Quiting program
#         elif choice == 6:
#                 print("**<<You are no longer on the main menu.>>**")
#                 print("**<<Thank you for choosing BOOMBOX MUSIC LIBRARY.>>**")
#                 print("**<<Run the program again to get back to the main menu.>>**")

# #  Unrecognized input and validates user's input
#         else:
#                 print("*<<Incorrect Input.>>**")
                
                
# # Calling the function
# if __name__ == "__main__":
#     main()
    















# def create_playlist(songs):
#         print("Create a Favorites Playlist")
#         playlist_name = input("Enter the name of your playlist: ")
#         playlist = []
#         while True:
#             print("Add songs to your playlist  (Enter 'done' to finish):")
#             songName = input("Enter the name of the song: ")
#             if songName.lower() == 'done':
#                 break
#             for song in songs:
#                 if songName in song:
#                     playlist.append(song)
#             else:
#                 print("Song not found in library.")
#         with open(f"{playlist_name}.txt", 'w') as playlist_file:
#             for song in playlist:
#                 playlist_file.write(",".join(song) + "\n")
#         print(f"{playlist_name} playlist created!")                        


# def main():

#     try:
#         mySongs = []
#         inFile = open("mySongsList.txt", "r")
#         line = inFile.readline()
#         # will continue to append and read until there is nothong else to read
#         while line:
#             mySongs.append(line.strip("\n").split(","))
#             line = inFile.readline()
#         inFile.close()  

#     except FileNotFoundError: 
#         print("mySongsList.txt is not found")  
#         print("A new songs list!!")   
#         mySongs = []
    

#     choice = 0
#     while choice != 5:
#         print("Music Library Manager")
#         print("1) Add a song")
#         print("2) Search a song")
#         print("3) Create a Favorites Playlist")
#         print("4) Display songs")
#         print("5) Exit")
#         choice = int(input())


#         if choice == 1:
#             print("Add a song")
#             songName = input("Enter the name of the song....")
#             songArtist = input("Enter the name of the artist...")
#             songGenre = input("Enter the genre of the song....")
#             mySongs.append([songName, songArtist, songGenre])

#         elif choice == 2:
#             print("Search a song") 
#             keyword = input("Enter name....")   
#             for song in mySongs:
#                 if keyword in song:
#                     print(song)
#                 else:
#                     print("Song not found!")    

#         elif choice == 3:
#             create_playlist(mySongs)            

#         elif choice == 4:
#             print("Display songs")
#             for i in range(len(mySongs)):
#                 print(mySongs[i])

#         elif choice == 5:
#             print("Exit")       

#     print("Program ended") 


   
#     # # saved to textfile
#     # outfile = open("mySongsList.txt", 'w')
#     # for song in mySongs:
#     #     outfile.write(",".join(song) + "\n")
#     #     outfile.close()


# if __name__ == "__main__":
#     main()