# Tlamim - Selection Process Assistant App

Tlamim is a web application that serves as an assistant for the candidates selection process. It is designed to help streamline the process of selecting candidates. The website consists of a backend written in Python and a frontend built using Node.js.

## Requirements

Before running the Tlamim app, ensure you have the following requirements installed on your system:

- Python >= 3.9
- Node.js
- MongoDB (as a service)
- requirments.txt

In addition, you will need to set up a Google project and allow it to access both google forms and gmail APIs. To do this, follow the instructions in [Google Workspace Developer Guide](https://developers.google.com/workspace/guides/get-started). Once you've completed the setup, save the credentials as credentials.json and add them to the backend folder.


## Getting Started

To get started with Tlamim, follow these steps:

1. Clone the repository to your local machine.

```
git clone https://github.com/hadasabraham/Tlamim-project.git
```

2. Navigate to the backend folder and run the BackendApp.py script.

```
cd ./backend
python BackendApp.py
```

3. Open a new terminal, navigate to the frontend folder, and start the frontend server.

```
cd ./frontend
npm run start # Start the frontend server
```

4. Open your web browser and visit `http://localhost:3000` to access the Tlamim app.


## Backend structure

In the backend folder each file defines a diffrent part of our backend.
- EmailServer.py - defines an abstraction of Gmail API
- FormServer.py - defines an abstraction of Google Forms API
- Tables.py - defines the abstraction of the database and basic operations.  
- utils.py - defines an API of the backend features. The backend server uses those wrapper functions for easier use of the dataset and the other servers.
- BackendApp.py - defines the backend server. 
- test.py - defines serveral basic tests on the system.
- pathParameters/parameters.py - defines the communication structure between the frontend and the backend.

