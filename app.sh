#! /bin/sh
python ./backend/BackendApp.py &
cd frontend
npm run start
