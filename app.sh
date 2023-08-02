#! /bin/sh
cd backend
python ./BackendApp.py &
cd ../frontend
npm run start
