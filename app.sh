#! /bin/sh
python ./backend/BackendApp.py &
cd new_front
npm run start
