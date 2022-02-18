orchard consists of the following components:

 - `parse`: translate an .rdlevel file into standards-compliant JSON
 - `vitals`: extract metadata from an .rdzip
 - `scan`: scrape sources for levels and update an SQL database with the levels
 - `bot`: administration interface for approving levels, as a discord bot + web page
 - `package`: build a Docker image of the final API 


# install

Run `pip install -e .` in this directory.