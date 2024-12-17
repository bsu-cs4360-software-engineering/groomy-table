**Master Doc**

* **Functional Requirements**  
  * Users can create an account  
  * Users can login/authenticate  
  * Users can CRUD Customers  
  * Users can CRUD Appointments  
  * Users can CRUD Notes  
  * Users can CRUD Services  
  * Users can CRUD Invoices  
  * Users can see a map of the local area  
  * The map shows a path from the current location to the next appointment  
  * Users can “Take Payments”  
    * (no actual payment processor involved, just a mock payment)

* **Nonfunctional Requirements**  
  * GUI based software  
  * Unit testing is the primary source of documentation  
  * Either desktop or web-based  
* **Standards/Conventions**  
  * Languages: Python/HTML  
  * Database: SQLite  
  * Directory Structure: static (CSS, JS, images) models (classes) unit tests, templates  
  * Naming conventions  
    * Python \-  Variables: *snake\_case*, methods/functions: *snake\_case* Classes: *Pascal\_Case* constants: *snake\_case*…  
    * Javascript \- Variables: camel case, methods/functions: camel case  
* **Quick start for Devs**

	Templates \- Contains the structure of each web page made in HTML.  
	Models \- Database structure and relationships made through python classes.  
	Routes \- Contains the logic for each page made in python.  
	Instance \- Folder in which the database is stored whenever the program is ran.  
	Static \- Folder that contains css, images/svg files, javascript  
	Tests \- Contain unit tests for the functions in the project

# 

# Design Doc

**General Style**

Colors:

White \- \#FFF  
Black \- \#1010  
Primary Accent \- Purple (\#7d2ecc)  
Primary Highlight \- Light-Purple (\#9760ce)

Text:

Font \- Arial, sans-serif  
Color \- Blue-Grey (\#3a4f66), or Black ( \#1010)  
Size \- 16px

Background:

Color \- White (\#fff), and Grey( \#dfdddd)

Button:

Color \- Primary Accent(\#7d2ecc), or White(\#fff)

Form Input:

Background Color \- rgba(145, 141, 141, 0.1)  
Border \- rgba(255, 255, 255, 0.3)  
Box-Shadow \- rgba(0, 0, 0, 0.1)  
Rounded Corners \- 20px

**Mobile (Assume the same as General Style unless listed)**

Color:

Highlight \- (\#8945cc)

Header:

Background Color \- Primary (\#7d2ecc)  
Text Color \- White (\#fff)  
Font Size \- large (CSS option)

Nav/Sidebar:

Background Color \- Primary (\#7d2ecc)  
Text Color \- White (\#fff)

**Dashboard**

Colors:

White \- \#FFF  
Black \- \#1010  
Primary Accent \- Grey-Blue (\#5041bc)  
Primary Highlight \- Light-Grey-Blue (\#624de3)

Text:

Font \- Montserrat, Arial, sans-serif  
Color \- White (\#fff), or Black ( \#1010)  
Size \- 16px

Header:

Size \- 2em

Background:

Color \- White (\#fff), and Grey( \#dfdddd)

Nav:

Text Color \- White (\#fff) or Primary Accent (\#5041bc)  
Color \- Primary Accent (\#5041bc)  
Selected Color \- White (\#fff)

Button:

Color \- Primary Accent (\#5041bc)

Table:

Even Row \- (\#f7f6fe)  
Odd Row \- White (\#fff)

Form Input:

Background Color \- White (\#fff)  
Border \- Black (\#1010)  
Rounded Corners \- 4px