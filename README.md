Muse
====

Muse is our HackMIT 2019 project, a 24 hour hackathon held in MIT.

Contributors
- Eoin Davey
- Ian Fennell
- Killian Kelly
- Dara MacConville

What it does
-----------

Our project provides an environment for people with visual impairments to learn core computer science concepts.

Our project contains a fully featured online editor which uses text to speech technologies to make text editing accessible by speaking the code the user is interacting with back to them in an intuitive way.

The editor allows users to program in a novel, innovative language designed specifically to provide an excellent learning experience, with no setup required. With this language users can use a fun, intuitive and beginner-friendly API to create all manner of sounds and music. This language brings the instant feedback used in visual beginner languages, such as Scratch, to the domain of audio.

Users can write code in their browser, and our custom interpreter and audio engine will compile and play whatever sounds and music their hearts desire.

Components
----------

* Clio - webapp
* Calliope - Language interpreter
* Erato - Audio Engine

Running
-------

The easiest way to run the project is to build the Docker image from the Dockerfile. `docker build . -t muse`

Then run `docker run --rm -it -p 80:4200 -p 5000:5000 muse`

This will host the project at http://localhost/

Dependencies
------------

Note that simpleaudio required libasound2-dev.

If audio exporting isn't working on your machine you might not have ffmpeg installed.
