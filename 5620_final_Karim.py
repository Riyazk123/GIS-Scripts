##      During this semester, for my Geography 5510 final project, I had to create an original project where I
##  elected to perform analysis on an ACS Block Group that had tabular data for economic and demographic
##  in a seperate table. After joining the tables of interest manually, there were around ~1,000 fields and they all
##  had alpha-numeric codes for fields. However, there was a metadata table that contained a key for fields,
##  where the "Short_Name" field equated to the alpha-numeric codes and "Full_Name" field equated to proper
##  names that describe the relevant fields.
##
##      I was unable to get the batch field update tool to work, so I resorted to looking at the metadata codes
##  and manually changing a few aliases, but the overwhelming majority remained unchanged. Thus, I felt like
##  this issue could be solved with python. For full transparency, this script does run into a few errors to
##  which I was unable to resolve, but around 95% of the field aliases were successfully updated, which if I
##  could travel back in time, would have been very helpful. While I only joined five tables of interest, there
##  are ~20 total tables that can be joined, and as more tables are joined to the feature class, it becomes
##  much more difficult to manually swap the alias' out.
##
##      I elected not to update field names, as I was running into an issue where the field names could not exceed
##  31 characters. I tried truncating the names to below 31 characters, but some of fields then had identical
##  names as the ACS key has very long base names. Thus, I chose to update aliases instead. 
    

#import statement, setting workplace, and enabling overwrite output
import arcpy
arcpy.env.workspace = "C:/GIS_data/ACS_2021_5YR_BG_09_CONNECTICUT.gdb"
arcpy.env.overwriteOutput = True

#setting variables to use in the script
input_fc = "ACS_2021_5YR_BG_09_CONNECTICUT"

tables = ["X01_AGE_AND_SEX", "X02_RACE",  "X17_POVERTY", "X19_INCOME", "X22_FOOD_STAMPS"]

join_fields = "GEOID_Data"

#for loop to join the five tables above to the block group layer
for table in tables:
    table_path = arcpy.env.workspace + "/" + table
    join_field = "GEOID"
    arcpy.JoinField_management(input_fc, join_fields, table_path, join_field)


#creating variables to select for records in the metadata key table for the five tables that have been joined
sql_exp = "Short_Name LIKE '%B01%' Or Short_Name LIKE '%B02%' Or Short_Name LIKE '%C02%' Or Short_Name LIKE '%B17%' Or Short_Name LIKE '%C17%' Or Short_Name LIKE '%B19%' Or Short_Name LIKE '%B22%'"
table = "BG_METADATA_2021"
out_table = "BG_METADATA_2021_Select"

#selecting records from the metadata 
arcpy.TableSelect_analysis(table, out_table, sql_exp)

#setting an alias dictionairy for mappings
alias_mappings = {}

#Search cursor to iterate through the metadata table to populate the dictionary
with arcpy.da.SearchCursor(out_table, ["Short_Name", "Full_Name"]) as cursor:
    for row in cursor:
        Short_Name = row[0]
        Full_Name = row[1]
        alias_mappings[Short_Name] = Full_Name

#batch updating the alias names using the alterfield tool with error handling and for loop
fields = arcpy.ListFields(input_fc)
for field in fields:
    if field.name in alias_mappings:
        new_alias = alias_mappings[field.name]
        try:
            arcpy.AlterField_management(input_fc, field.name, new_field_alias=new_alias)
        except arcpy.ExecuteError as e:
            print(e)
print("All processes are complete")

        
    
