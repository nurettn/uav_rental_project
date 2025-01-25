# UAV Rental Project with Django

## Overview

The UAV Rental Project is designed to manage UAV parts and their assembly into complete aircraft.

## Features

- Users can register using their email and password.
- Assign users to specific teams such as Wing Team, Fuselage Team, Tail Team, Avionics Team, and Assembly Team.
- Create, Read, Update, and Delete UAV parts with team-based permissions.
- Track the stock of each part.
- Combine various parts to assemble complete UAVs.
- Ensure all necessary parts are available before assembly.
- Restrict editing and deleting of parts based on team assignments, preventing unauthorized access even if frontend controls are bypassed.
- Utilizes Bootstrap for a clean UI.
- Integrates datatables.
- Containerized using Docker and managed with docker-compose for easy deployment.
- Includes simple unit tests to verify core functionalities.

## Installation

### Prerequisites

- Ensure **Docker** is installed on your system.
- Verify **docker-compose:** installation with `docker-compose --version`.

### Steps

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:nurettn/uav_rental_project.git
    cd uav_rental_project
    ```

2. **Configure Environment Variables:**
    ```bash
    cp .env-example .env
    ```

3. **Build and Run Docker Containers:**

    ```bash
    docker-compose up -d --build
    ```

4. **Create Superuser:**

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
5. **Access the Application:**

    - **To frontend:** Navigate to `http://localhost:8000/` in your web browser.
    - **To admin Panel:** Access Django's admin interface at `http://localhost:8000/admin/` and log in with your superuser credentials.

## Usage


### 1. Access the Admin Panel

- **URL:** `http://localhost:8000/admin/`
- **Action:**
  - Log in using the superuser credentials created during installation.
  - From the admin dashboard, manage users and assign them to specific teams.

  
### 2. Create necessary instances first with the superuser account
- **Action:**
  - In the admin panel, navigate to the `Teams` section and create one instance of each team type: Wing Team, Fuselage Team, Tail Team, Avionics Team, Assembly Team, and No Team.
  - In the admin panel, navigate to the `Aircrafts` section and create one instance of each aircraft type: TB2, TB3, AKINCI, and KIZILELMA.


### 3. Register New Users

- **URL:** `http://localhost:8000/accounts/signup/`
- **Action:**
  - Use the registration form to create new user accounts.
  - Users will register using their email and password.
- **Note:**
  - New users are assigned to "No Team" by default. Assign them to their respective teams via the admin panel for proper access control.


### 4. Assign Teams to Users

- **Action:**
  - In the admin panel, navigate to the `Personnels` section.
  - Edit each user’s profile to assign them to their designated team (Wing Team, Fuselage Team, Tail Team, Avionics Team, Assembly Team).
  
- **Teams and Permissions:**
  - **Wing Team, Fuselage Team, Tail Team, Avionics Team:**
    - Those teams can create, edit, and delete parts related to their specific domain.
  - **Assembly Team:**
    - Can display all parts.
    - Can assemble aircraft by combining all required parts.
    - Cannot create, edit, or delete parts.

### 5. Create UAV Parts

- **URL:** `http://localhost:8000/parts/`
- **Action:**
  - Navigate to the parts management page.
  - Depending on your team:
    - **Non-Assembly Teams:** See an "Add New Part" button to create parts relevant to their team.
    - **Assembly Team:** See an "Assemble Aircraft" button to initiate the assembly process.
  
- **Creating a Part:**
  - Click "Add New Part".
  - Fill out the form with the part type, associated aircraft, and stock quantity.
  - Submit the form to create the part.

- **Validation:**
  - The system prevents duplicate parts based on `part_type`, `aircraft`, and `team`.
  - If a duplicate is attempted, an error message is displayed.

### 6. Edit or Delete Parts

- **Action:**
  - From the parts list, non-Assembly team members can edit or delete parts specific to their team.
  - Assembly team cannot edit or delete any parts, enforced both on frontend and backend.

### 7. Assemble Aircraft

- **URL:** `http://localhost:8000/assemblies/assemble/`
- **Action:**
  - Only accessible to users in the Assembly Team.
  - Select the aircraft to assemble.
  - The system checks for the availability of required parts.
  - Upon successful assembly, stock levels of parts are decremented accordingly.
  - The assembled aircraft is recorded and can be viewed in the assembly list.

### 8. View Assembled Aircraft

- **URL:** `http://localhost:8000/assemblies/`
- **Action:**
  - Accessible to the Assembly Team.
  - Displays a list of all assembled aircraft with details of the parts used and assembly timestamps.


## Bonus Content

- Docker Deployment
- Unit Testing:
    ```bash
    docker-compose exec web python manage.py test
    ```
- DataTables integration
- Utilizes Bootstrap
- Separation of relational tables

## Specifications

- The system warns Assembly Team members when attempting to assemble aircraft with missing parts.
- Registration is handled via email and password only, with usernames disabled for simplicity and security.
- Teams are assigned manually through the admin panel to ensure that a senior team member reviews and assigns teams for better security.
- Parts can be deleted to allow teams to recycle them, as per project requirements. Deletion is handled in a way that doesn't affect existing assemblies.


## Additional Notes
- The project does not expose API endpoints, aligning with the project requirements. However, several endpoints were created for development purposes.
- Implemented backend permissions to prevent unauthorized editing and deletion of parts, even if frontend controls are bypassed.

## License
This project is for demonstration purposes and is not intended for production use. No license is applied.