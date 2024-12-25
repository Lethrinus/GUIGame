## **Project: Escape the House Game**

This project is  an immersive Escape the House game developed in Python using the Tkinter library for GUI, with integration of multiple features like multilingual support, game statistics, and dynamic gameplay elements. The game consists of multiple interconnected rooms, puzzles, and challenges to provide players with an engaging experience.

## **Key Features**

**1. Game Rooms and Challenges**

The game is divided into four rooms (Room1, Room2, Room3, and Room4), each presenting unique challenges.

**Challenges include:	**	

**Pathfinding Puzzle:** Navigate a dynamic grid to reach the goal while avoiding traps and obstacles.

**Card Matching Game:** Match pairs of cards within a limited number of attempts.

**Food Chemistry Lab:** Experiment with ingredients to discover recipes.

**Mastermind Game:** Decode a hidden color sequence within a fixed number of attempts.

## **2. Dynamic Progression**

Players need to collect keys by successfully completing challenges in rooms to unlock new areas.
An in-game timer tracks player performance.

## **3. Leaderboards**

**Local and Global Leaderboards:**

Track player scores and completion times.
Compare your scores globally or view personal records.

## **4. Internationalization (i18n)**

Multilingual support using the i18n.py module:
Language files stored in languages folder.
Players can select their preferred language at the start or via the options menu.

## **5. Graphics and Interactive UI**

The game employs custom images for visual elements (e.g., doors, arrows, cards).
Interactive gameplay with buttons and animations.
Images are dynamically loaded and positioned using the add_images.py module.

## **6. Database Management**

Stores player scores and leaderboard data in a local SQLite database (game_times.db).
The database_scores.py module handles:
Inserting player times.
Updating global top times.
Fetching data for leaderboards.
Project Structure

## **File Overview**

_game.py_

Core game logic.
Contains classes for each room and the main game window.
Manages interactions, navigation, and in-game elements.

_add_images.py_

Helper functions for loading and adding images to the game canvas.

_database_scores.py_

Handles the SQLite database for player scores and leaderboards.

_i18n.py_

Implements multilingual support by loading translations from .lng files.

**Language Files (languages/data_*.lng)**

Store key-value pairs for translations in supported languages.


## ****How to Run the Game****

**Prerequisites**

_Python 3.8 or higher._
_Required libraries: tkinter, Pillow, sqlite3._

**Steps to Run**

Clone the repository and navigate to the project directory.

**Install required dependencies:**
_**pip install pillow**_
**Run the game:**
**_python game.py_**

## **Future Enhancements**

Add more rooms with advanced puzzles.
Support for online multiplayer leaderboards.
Enhanced animations and sound effects.
Inclusion of more languages.


##  **Sources we used in this project :**
https://penzilla.itch.io/top-down-retro-interior
