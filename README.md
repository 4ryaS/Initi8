# NGO Management System

This project is an NGO Management System built with Python and PyQt5, providing a user-friendly graphical interface for managing users, donations, and NGO information.

## Features

* **Secure Authentication:** User login with username and password, securely stored using MySQL.
* **User Registration:** New users can register with validation, storing their information in the MySQL database.
* **Profile Management:** Users can view and update their profile details, including their display picture.
* **Donation Management:**
    * Users can donate items, which are stored in the MySQL database along with their images.
    * Users can browse through available donated items.
* **NGO Information:** Access details about registered NGOs, including name, location, contact information, and more.
* **Random Facts:**  Displays interesting facts on the main screen and after user login.

## Technologies Used

* **Python:**  Core programming language for backend logic and application functionality.
* **PyQt5:** Python bindings for the Qt framework, used to create the graphical user interface.
* **MySQL:** Relational database management system for storing user data, donation records, and NGO information.

**Prerequisites:**
   * **Python:** Ensure you have Python installed ([https://www.python.org/downloads/](https://www.python.org/downloads/)).
   * **MySQL:** Install and set up a MySQL server ([https://dev.mysql.com/downloads/](https://dev.mysql.com/downloads/)).
   * **PyQt5:** Install using pip: `pip install PyQt5`
   * **MySQL Connector:** Install using pip: `pip install mysql-connector-python` 
