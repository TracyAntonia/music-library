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
    playlist_name = input("Enter the name of the playlist: ")
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
                duration = input("Enter the duration of the song in seconds: ")
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
                break
            # Unrecognized input and validates user's input
            else:
                print("*<<Incorrect Input.>>**")

    if __name__ == "__main__":
        main()


