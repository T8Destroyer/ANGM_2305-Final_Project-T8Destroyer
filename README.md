# ANGM_2305-Final_Project-T8Destroyer

## Demo
Demo Video: https://vimeo.com/1191339868

## GitHub Repository
GitHub Repo: https://github.com/T8Destroyer/ANGM_2305-Final_Project-T8Destroyer

## Description
This project is a recreation of the original arcade game PAC-MAN in python, plus some extra additions. This game uses a vector node system to connect and guide pacman and the ghosts throughout the maze. Each node is connected to others by assigning one of the cardianl directions to them.The maze itself is made from a text file, which translates certain characters into certain nodes, paths, and boundaries.

PacMan, the ghosts, and even fruit work based on an entity class, setting the ground work for how these characters would actually interact with the maze. Each character then has their own seperate classes built on the entity class, giving different behavior to each while keeping their interactions with the maze the same.

These were all things that I was guided in making thanks to the tutorial website pacmancode.com, but I do have some of my own special additions, such as recreating a glitch that happens in the orignal pacman arcade game with the ghost Pinky, and even making the transitions between the ghost's behavior modes more accurate with sudden turn around behaviors for all the ghosts. These nice touches made the game feel more like the original.

But by far the best thing I added myself were four entirely new ghosts, each with their own behaviors for chasing PacMan. Not only did this lead to more ghosts, but a whole customization system for which ghosts the player wanted to play against. This also meant a whole rework of the preexisting ghost system which only had the original four ghosts hardcoded in. This change impacted the ghost Inky the most in particular. Because his AI was originally affected by the ghost Blinky, I had to account his for the possibility of games with no Blinky, or even several Blinky's.