# Data Model for Todo Web Application

This document describes the database schema for the application.

## Entities

### User

Represents a registered user of the application.

**Fields**:

| Name          | Type           | Constraints                  | Description                   |
|---------------|----------------|------------------------------|-------------------------------|
| `id`          | Integer        | Primary Key, Auto-increment  | Unique identifier for the user|
| `email`       | String         | Not Null, Unique             | User's email address (for login)|
| `password_hash`| String         | Not Null                     | Hashed password for the user  |

**Relationships**:

-   Has many `Task`s.

### Task

Represents a single to-do item created by a user.

**Fields**:

| Name          | Type           | Constraints                  | Description                        |
|---------------|----------------|------------------------------|------------------------------------|
| `id`          | Integer        | Primary Key, Auto-increment  | Unique identifier for the task   |
| `title`       | String         | Not Null                     | The title of the task              |
| `description` | String         | Nullable                     | A more detailed description        |
| `completed`   | Boolean        | Not Null, Default: `false`   | Whether the task is completed    |
| `user_id`     | Integer        | Foreign Key (User.id)        | The ID of the user who owns the task|

**Relationships**:

-   Belongs to one `User`.
