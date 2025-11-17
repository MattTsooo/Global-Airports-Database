# Global Airports Database Management System

A database management application for exploring, searching, and editing global airport data with a GUI interface.

## Overview

This application provides a complete solution for managing aviation-related geographic and infrastructure data, including continents, countries, regions, airports, runways, frequencies, and navigation aids. Built with Python, SQLite, and Tkinter, it offers an interface for data exploration and modification.

## Features

### Data Hierarchy Management
- **Continents**: Top-level geographic organization with continent codes
- **Countries**: Country-level data with ISO codes, Wikipedia links, and keywords
- **Regions**: Sub-country administrative divisions with local and region codes
- **Airports**: Complete airport information including coordinates, elevation, and service types
- **Runways**: Detailed runway specifications with dimensions and surface information
- **Navigation Aids**: Aviation navigation equipment and frequencies

### Search Capabilities
- **Multi-Criteria Search**: Search by code, name, or multiple parameters
- **Real-Time Filtering**: Dynamic search activation based on input
- **Result Browsing**: Listbox display with easy selection for editing

### CRUD Operations
- **Create**: Add new records with validation
- **Read**: Load and display existing records
- **Update**: Modify record details with constraint checking
- **Delete**: (Supported through database operations)

### Data Integrity
- **Foreign Key Constraints**: Maintains referential integrity across tables
- **Input Validation**: Type checking for numeric fields
- **Error Handling**: Comprehensive exception management
- **Transaction Support**: Commit/rollback for data consistency

## Technical Architecture

### Design Pattern: Event-Driven MVC

```
┌─────────────────┐
│   Tkinter UI    │ ← View Layer
│  (MainView)     │
└────────┬────────┘
         │ Events
         ↓
┌─────────────────┐
│   EventBus      │ ← Controller
│  (Mediator)     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│    Engine       │ ← Business Logic
│   (Handlers)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  SQLite DB      │ ← Data Layer
│  (Persistence)  │
└─────────────────┘
```

### Project Structure

```
Global-Airports-Database/
├── p2app/
│   ├── engine/
│   │   ├── main.py              # Main engine coordinator
│   │   ├── database_handler.py  # Database connection management
│   │   ├── continent_handler.py # Continent CRUD operations
│   │   ├── country_handler.py   # Country CRUD operations
│   │   └── region_handler.py    # Region CRUD operations
│   │
│   ├── events/
│   │   ├── app.py              # Application-level events
│   │   ├── continents.py       # Continent events
│   │   ├── countries.py        # Country events
│   │   ├── regions.py          # Region events
│   │   ├── database.py         # Database events
│   │   └── event_bus.py        # Event routing system
│   │
│   └── views/
│       ├── main.py             # Main window
│       ├── continents.py       # Continent UI components
│       ├── countries.py        # Country UI components
│       ├── regions.py          # Region UI components
│       ├── menus.py            # Menu bar implementation
│       ├── events.py           # Internal UI events
│       └── event_handling.py   # Event propagation logic
│
└── airports.db                 # SQLite database file
```

## Database Schema

### Core Tables

#### continent
```sql
- continent_id (INTEGER, PRIMARY KEY)
- continent_code (TEXT, UNIQUE)
- name (TEXT)
```

#### country
```sql
- country_id (INTEGER, PRIMARY KEY)
- country_code (TEXT, UNIQUE)
- name (TEXT)
- continent_id (INTEGER, FOREIGN KEY)
- wikipedia_link (TEXT)
- keywords (TEXT, NULLABLE)
```

#### region
```sql
- region_id (INTEGER, PRIMARY KEY)
- region_code (TEXT, UNIQUE)
- local_code (TEXT)
- name (TEXT)
- continent_id (INTEGER, FOREIGN KEY)
- country_id (INTEGER, FOREIGN KEY)
- wikipedia_link (TEXT, NULLABLE)
- keywords (TEXT, NULLABLE)
```

#### airport
```sql
- airport_id (INTEGER, PRIMARY KEY)
- airport_ident (TEXT, UNIQUE)
- type (TEXT)
- name (TEXT)
- latitude_deg (REAL)
- longitude_deg (REAL)
- elevation_ft (INTEGER, NULLABLE)
- continent_id (TEXT, FOREIGN KEY)
- country_id (INTEGER, FOREIGN KEY)
- region_id (INTEGER, FOREIGN KEY)
- municipality (TEXT, NULLABLE)
- scheduled_service (INTEGER)
- gps_code, iata_code, local_code (TEXT, NULLABLE)
- home_link, wikipedia_link (TEXT, NULLABLE)
- keywords (TEXT, NULLABLE)
```

Additional tables: `airport_frequency`, `runway`, `navigation_aid`

## Key Implementation Features

### Event-Driven Architecture

The application uses a custom event system to decouple components:

```python
# Event flows:
User Action → UI Event → EventBus → Engine Handler → Database Operation → Result Event → UI Update
```

**Benefits:**
- Loose coupling between UI and business logic
- Easy to test individual components
- Extensible for new features
- Clean separation of concerns

### SQL Injection Prevention

All database queries use parameterized statements:

```python
self._connection.execute_queries(
    'SELECT * FROM country WHERE country_code = :code',
    {'code': country_code}
)
```

### Dynamic Query Building

Flexible search functionality with optional parameters:

```python
query_conditions = []
if country_code:
    query_conditions.append('country_code = :code')
if name:
    query_conditions.append('name = :name')
    
query = 'SELECT * FROM country'
if query_conditions:
    query += ' WHERE ' + ' AND '.join(query_conditions)
```

### State Management

- **Loading States**: Display "Loading..." during async operations
- **Edit States**: Track whether editing new or existing records
- **Button States**: Enable/disable based on user actions and data validity

## User Interface Components

### Main Window
- Menu bar (File, Edit, Debug)
- Dynamic view switching
- Database path display in title bar

### Search Views
- Text input fields with real-time validation
- Search button activation
- Results listbox with selection handling
- New/Edit action buttons

### Editor Views
- Auto-generated ID display
- Form fields (Entry widgets for editable, Labels for read-only)
- Save/Discard buttons
- Error message dialogs

## Usage

### Opening a Database
1. File → Open
2. Select `.db` file
3. Edit menu appears when database loads successfully

### Searching Records
1. Edit → Continents/Countries/Regions
2. Enter search criteria
3. Click "Search"
4. Select result from list
5. Click "Edit" to modify

### Creating Records
1. Navigate to desired entity view
2. Click "New [Entity]"
3. Fill in required fields
4. Click "Save"

### Editing Records
1. Search and select record
2. Click "Edit [Entity]"
3. Modify fields
4. Click "Save" to commit or "Discard" to cancel

## Debug Mode

Enable via Debug → Show Events to see:
- Event flow through the system
- User interactions
- Engine responses
- Useful for troubleshooting and understanding architecture

## Technical Stack

- **Language**: Python 3.x
- **Database**: SQLite3 (STRICT mode)
- **GUI Framework**: Tkinter
- **Architecture Pattern**: MVC with Event Bus
- **Data Format**: Structured relational database

## Security Features

- Parameterized SQL queries (prevents injection)
- Foreign key enforcement
- Type safety with STRICT tables
- Input validation on all user entries
- Transaction rollback on errors

## Performance Considerations

- Efficient indexing via PRIMARY KEY and UNIQUE constraints
- Lazy loading of records (generator-based results)
- Minimal database connections (connection pooling)
- Event-based updates (no unnecessary re-renders)


## Learning Outcomes

What I've Learned:
- Professional database design with normalization
- Event-driven architectural patterns
- GUI application development
- SQL query optimization
- Error handling and validation
- MVC pattern implementation
- Clean code organization and modularity
- Security best practices (SQL injection prevention)

## Future Enhancements

- Airport search and management UI
- Runway and frequency editors
- Map visualization of airports
- Export to CSV/JSON
- Import bulk data
- Advanced filtering and sorting
- Distance calculations between airports
- Flight path planning features
- Data analytics dashboard
- Multi-user support with authentication

## Credits

Built as part of ICS 33 coursework, demonstrating advanced Python programming, database management, and software architecture principles.
