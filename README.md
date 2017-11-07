# Gellish
Objective:  
1. Building a reference application for validating, verificating and demonstrating the application of the Gellish family of formalized natural languages.  
2. Developing open source tools for supporting implementations of universal system independent data storage, data integration and data exchange between systems using a formal language.  
The formal language can be any of the language variants of the Gellish family of formalized natural languages. For example Formal English, Formal Dutch (Formeel Nederlands) or any other formalized natural language in the Gellish Family. The Gellish Formalized languages are defined in a Taxonomic Dictionary - Ontology, which allows for extensions and addition of translations in other languages.
I am an information modeler/ontologist with an engineering background and I worked for about 35 years in IT for Shell. Because of Shell's urgent need for data integration, data exchange and interoperability of internal systems and systems of suppliers, I worked for over 20 years on interoperability standards and IM consultancy.  
As a result I have developed the Gellish family of universal data exchange languages. Formal English is the English variant of that family. Formal English is a formalization of a natural English, which means that Formal English is machine interpretable as well as human readable. The Gellish formal languages (such as Formal English and Formal Dutch) are widely applicable and are proven to be suitable for modeling the whole life-cycle of all kinds of facilities and infrastructure and their components design, operation and maintenace, as well as for modeling business processes, and knowledge and requirements about them.  
  
The language definition includes a language defining ontology and taxonomic dictionary, together with a syntax that is called the Gellish Expression Format. The language principles are described in my PhD and its application is documented in various books and documents and a wiki, see: www.gellish.net. The Gellish Syntax is available as pdf-file in this project and is summarized in par 17 of the Gellish wiki (http://www.gellish.net/index.php/dokuwiki.html).  
  
For testing tools and applications the following data is available as CSV (semicolon ";" separated) files that use Unicode UTF-8, that are compliant with the above mentioned Gellish Syntax for expressions in any of the formal languages:  
1. A representative subset of the language defining ontology of Formal English (and Formeel Nederlands). The full taxonomic dictionary-ontology can be licensed via the Gellish website.  
2. A subset of the UoMs (units of measure) and currencies definitions section of the taxonomic dictionary.  
3. A subset with definitions and knowledge about roads, selected from the Building, civil and furniture section of the taxonomic dictionary and knowledge base.  
4. An example of a product model of a road network, expressed in Formal English.  

The Application software allows to select creation of a new database or querying an existing database. On 'n' (new) the programn will (1) first import the 'base_ontology' file, containing the core language definition (subset), in order to enable formulation and interpretation of expressions in the formal language. This enables (2) importing the second and third files (and similar taxonomic dictionary files), because it enables to verify and interpret the relation types and build the taxonomy and object models. Then (3) product and process models, knowledge models and requirements models can be imported, verified and interpreted. The fourth file is an example of a product model (being a model of a simple road network).

The Application software starts with the Communicator.py module.
