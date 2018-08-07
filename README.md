# Gellish
Objective:  
1. Building a reference application for validating, verificating and demonstrating the application of the Gellish family of formalized natural languages for data integration and data exchange.  
2. Developing open source tools for supporting implementations of universal system independent data storage, data integration and data exchange between systems using a formalized natural language.  

The formal language can be any of the language variants of the Gellish family of formalized natural languages. For example Formal English, Formal Dutch (Formeel Nederlands) or any other formalized natural language in the Gellish family. The Gellish formalized languages are defined in a Taxonomic Dictionary - Ontology, which allows for extensions and combination with other dictionaries as well as for addition of translations in other languages.  

I am an information modeler/ontologist with an engineering background and I worked for about 35 years in IT for Shell. Because of Shell's urgent need for data integration, data exchange and interoperability of internal systems and systems of suppliers, I worked for over 20 years on international interoperability standards and IM consultancy.  
As a result I have developed the Gellish family of universal formal languages for data exchange and data integration. Formal English is the English variant of that family. Formal English is a formalization of a natural English, which means that Formal English is machine interpretable as well as human readable. The Gellish formal languages (such as Formal English and Formal Dutch) are widely applicable and are proven to be suitable for modeling the whole life-cycle of all kinds of facilities and infrastructure and their components design, operation and maintenace, as well as for modeling business processes, and knowledge and requirements about them.  
  
The language definition includes a language defining ontology and taxonomic dictionary, together with a syntax that is called the Gellish Expression Format. The language principles are described in my PhD and its application is documented in various books and documents and a wiki, see: www.gellish.net. The Gellish Syntax is available as pdf-file in this project and is summarized in par 17 of the Gellish wiki (http://www.gellish.net/index.php/dokuwiki.html).  
  
For testing tools and applications the following data is available as CSV (semicolon ";" separated) files that use Unicode UTF-8, that are compliant with the above mentioned Gellish Syntax for expressions in any of the formal languages:  
1. A representative subset of the language defining ontology of Formal English (and Formeel Nederlands). The full taxonomic dictionary-ontology can be licensed via the Gellish website.  
2. A subset of the UoMs (units of measure) and currencies definitions section of the taxonomic dictionary.  
3. A subset with definitions and knowledge about roads, selected from the Building, civil and furniture section of the taxonomic dictionary and knowledge base.  
4. An example of a product model of a road network, expressed in Formal English.  

The Application software allows to select creation of a new database or querying an existing database. On 'n' (new) the program will (1) first import the 'base_ontology' file, containing the core language definition (subset), in order to enable formulation and interpretation of expressions in the formal language. This enables (2) importing the second and third files (and similar taxonomic dictionary files), because it enables verifying and interpreting the kinds of relations and build the taxonomy and object models. Then (3) product and process models, knowledge models and requirements models can be imported, verified and interpreted. The fourth file is an example of a product model (being a model of a simplified road network).


## Installation

Make sure you have the Python-Tkinter libraries installed.

On Mac OSX using Mac Ports::

    sudo port install py36-tkinter

If you want to use a virtualenv, make sure to also include system site packages:

    mkvirtualenv --system-site-packages --python=/opt/local/bin/python3.6 env

The Application software starts with the Communicator.py module. To run from a shell:

    cd CommunicatorSource/
    python3.6 Communicator.py

## Example usage procedure

The following steps illustrate a possible usage of the Communicator app.
In the example a file with information about electric cables is loaded into a semantic network. Then a search for data about electric cables results in a presentation of various kinds of data.

0. Starting the app implies that a semantic network is created that defines the core of the Gellish Formal English language. 
1. From the Main menu, select the 'Read file' option. This opens a file selection window.
2. Select one or more CSV files and UTF-8 encoding. The content of the selected files should comply with the Gellish Expression Format. For example, from the directory GellishData select the file 'Electric cables-UTF-8.csv' with example data about electric cables. Or select your own file(s) in Gellish Expression Format. Then press the 'Open' button. This will initiate importing en verifying the files content and integrating that content with the semantic network that defines the Gellish language.
3. From the Main menu, select the 'Search' option. This opens a Search Window.
4. Enter a search term in the field under the text 'Search term'. For example enter 'elec', which will initiate the search for concepts which name starts with 'elec'. The names that satisfy the search term will be displayed in the field under the text 'Select one of the following options'.
5. Select one of the displayed options. For example, select 'electric cable'. This will initiate the display of its UID (unique identifier), a textual definition and possible characteristics and their oprional or real vales.
6. Press the 'Confirm' button, to confirm the selection. This will open a series of windows with further information about the selected concept, including a.o. a taxonomy of subtypes of electric cable and a product model that includes a decomposition of electric cables.
7. Open the 'Documents' tag. This will display a list of textual documents about electric cables. Clicking on one of the lines will open the applicable document.
Further example actions on that further information will be described later.
