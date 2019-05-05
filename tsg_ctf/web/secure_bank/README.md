# About
This directory contains the files necessary to run the `Secure Bank` web challenge from [TSG CTF](https://score.ctf.tsg.ne.jp/) 2019.


# Prompt
I came up with more secure technique to store user list. Even if a cracker could dump it, now it should be of little value!!!

# Setup

 1. `docker build -t secure_bank .`
 2. `docker run --rm -it -p 4567:4567 -v "$PWD":/usr/src/app secure_bank rackup -p 4567 -o 0.0.0.0`

Then point your browser to [http://localhost:4567](http://localhost:4567)
