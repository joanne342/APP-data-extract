

Documentation: https://docs.google.com/document/d/155I1McJ3je3egCSLT63L2SABek5XWXWY/

What the program does in greater detail: https://docs.google.com/document/d/1Kn1VOlA_CnJBTAo3SMbEacWtqAULBLBW/

*What the program does*

For simplicity, the program processes the contents of the unzipped "activeplacescsvs.zip" but specifically

sites.csv

and

artificialgrasspitches.csv
athletics.csv
cycling.csv
golf.csv
grasspitches.csv
healthandfitnessgym.csv
icerinks.csv
indoorbowls.csv
indoortenniscentre.csv
outdoortenniscourts.csv
skislopes.csv
sportshalls.csv
squashcourts.csv
studios.csv
swimmingpools.csv

It also handles gymnastics.csv which isn’t available yet but will become available in due course.  In the meantime, the lack of gymnastics.csv doesn’t make the program throw an error.

----------------------------------

All of the sports subtype CSV’s (“artificialgrasspitches” etc) are appended together then merged with sites.csv on the “Site ID” column.

Closed facilities are filtered out.

Local authorities that do not match the Local Authority Code input by the user are also filtered out. 

The site name is converted to title case

The facility type IDs are changed to their correct text labels e.g. 1 to "Standard Oval Outdoor".

The facility subtype IDs are changed to their correct text labels e.g. 100 to "Athletics".

The full specification of Active Places facility types and facility subtypes can be found in the .csv files “facilitytype.csv” and “facilitysubtype.csv”

These files can be found with the unzipped "activeplacescsvs.zip" files.

----------------------------------

The columns are rearranged to the following:

Site Name
Thoroughfare Name
Town
Site ID
Postcode
Facility Type
Facility Subtype
Facility ID
Unit
Number
Management Type (Text)
Ownership Type (Text)
Accessibility Type (Text)
Local Authority Code
Local Authority Name
Easting
Northing
Latitude
Longitude

Unit and number are new.  Unit is populated with the facility subtype and number is populated with the number of them.

----------------------------------

The merged dataframe is output to “[Local Authority Name] active_places.csv” ", e.g., "Adur active_places.csv” in the same folder as APP Data Extract.



