

Documentation: https://docs.google.com/document/d/155I1McJ3je3egCSLT63L2SABek5XWXWY/

What the program does in greater detail: https://docs.google.com/document/d/1Kn1VOlA_CnJBTAo3SMbEacWtqAULBLBW/

*What the program does*

For simplicity, the program processes the contents of the unzipped "activeplacescsvs.zip" but specifically

sites.csv

and

artificialgrasspitches.csv<br>
athletics.csv<br>
cycling.csv<br>
golf.csv<br>
grasspitches.csv<br>
healthandfitnessgym.csv<br>
icerinks.csv<br>
indoorbowls.csv<br>
indoortenniscentre.csv<br>
outdoortenniscourts.csv<br>
skislopes.csv<br>
sportshalls.csv<br>
squashcourts.csv<br>
studios.csv<br>
swimmingpools.csv<br>

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

Site Name<br>
Thoroughfare Name<br>
Town<br>
Site ID<br>
Postcode<br>
Facility Type<br>
Facility Subtype<br>
Facility ID<br>
Unit<br>
Number<br>
Management Type (Text)<br>
Ownership Type (Text)<br>
Accessibility Type (Text)<br>
Local Authority Code<br>
Local Authority Name<br>
Easting<br>
Northing<br>
Latitude<br>

Unit and number are new.  Unit is populated with the facility subtype and number is populated with the number of them.

----------------------------------

The merged dataframe is output to “[Local Authority Name] active_places.csv” ", e.g., "Adur active_places.csv” in the same folder as APP Data Extract.



