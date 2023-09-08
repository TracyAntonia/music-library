# Boombox Music Library Management System

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Future Plans](#future-plans)
- [Resources](#resources)
- [Feedback](#feedback)

## Introduction

The Boombox Music Library Management System is a Python-based application that allows users to organize, manage, and enjoy their music collections effortlessly. This system provides a user-friendly interface for adding, searching, creating playlists, and performing various operations on songs, artists, and playlists.

## Problem Statement

Managing a music collection efficiently can be a challenging task. Users often struggle with organizing songs, creating playlists, and keeping track of their favorite artists. This system aims to solve these problems by providing a centralized platform for music management.

## Solution

The Boombox Music Library Management System offers a comprehensive solution for music organization and management. It allows users to:

- Add songs with details like title, artist, duration, and creation date.
- Search for songs by title, making it easy to find specific tracks.
- Create personalized playlists by selecting their favorite songs.
- Display a list of available songs and artists.
- Edit playlists by adding or removing songs.
- Delete songs by title or entire playlists.

## Key Features

- User-friendly command-line interface (CLI) for easy navigation.
- Integration with an SQLite database to store music-related data.
- Object-Relational Mapping (ORM) using SQLAlchemy for efficient database interactions.
- Seamless creation and management of playlists.
- Robust search functionality for songs.
- Flexibility to add new songs and artists.
- Future-ready design with potential for further enhancements.

## Technology Stack

- Python: The primary programming language for developing the application.
- SQLAlchemy: Used for database management, ORM, and interaction with the SQLite database.
- SQLite: The database management system used to store user data, artist information, songs, and favorites.
- Command-Line Interface (CLI): Provides a user-friendly interface for interaction.

## Getting Started

Follow these steps to set up and run the Boombox Music Library Management System:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/TracyAntonia/music-library.git

2. Navigate to the project directory:   

    cd boombox-music-library

3. Create a virtual environment (optional but recommended):
    
     python -m pipenv install
     python -m pipenv shell

4. Run the application:

    python main.py

Now, you're ready to start managing your music collection using the Boombox Music Library Management System.

## Usage
Launch the application and follow the on-screen instructions.
Use the CLI to perform actions such as adding songs, searching, creating playlists, and more.
Explore the features and enjoy an organized music collection.

## Future Plans
We are committed to continuous improvement and plan to enhance the Boombox Music Library Management System with the following features:

- User account management for personalized experiences.
- Enhanced playlist management with sorting and customization options.
- Integration with external music streaming services.
- Cross-platform compatibility for wider accessibility.
- Improved error handling and user notifications.

## MIT License

Copyright (c) [2023] [Antonia Njuguna]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


