<<<<<<< HEAD
#Intersnack Aufgaben import anpassung

Set the directories\
![img.png](img.png)\
*moddir* - is the direcrory for modified xml datasets \
*candir* - is the direcrory for modified xml cancelled \
*rootdir* - is the main direcrory \
*importdir* - is the direcrory for final editing xml datasets complete for import\
![img_2.png](img_2.png)\
Check directory - is a function to check if the needed directory exists, if not the function will create one.
![img_3.png](img_3.png)\
Function Clear data - will move everything what we don't need to the specified folders.\
![img_4.png](img_4.png)\
Function *Configure* - is the main part of the code, we start here with the looping throu the whole directory.\
![img_5.png](img_5.png)\
Here we select all files in the directory that match the criteria end with ".xml"\
![img_6.png](img_6.png)\
Now we parse every file\
![img_7.png](img_7.png)\
Than we check if the file had beed edited previously, in our case we check if the numer contains the digits "*0104*"\ 
becese after running the code thet returns this number in this field. \
![img_8.png](img_8.png)\
As next we have to set unique id's to the fields for our purposes, in case when we run thou the whole xml we will get \
any fields with this name. When the id's are setted we dump it to the xml tree.\
![img_9.png](img_9.png)\
Now we set an increment to measure how meny fields we have to change, the value of the number tell us this. \
![img_10.png](img_10.png)\
Here we split the data that we need for our fields in this case that are the number of pallets that have been separated \
from the info text.\
![img_11.png](img_11.png)\
Now we apply the data from Meter1 that are our pallets to our field Meter1 (the field Meter1 have an generated id, becase \
there can be more than 1 field for editing and also it can be more fields with our values.)\
![img_12.png](img_12.png)\
Here we do the same thing as before\
![img_13.png](img_13.png)\
The same thing too, but for other values and fields.\
![img_14.png](img_14.png)\
As one of the last things we do, is the clear out the xml, here we remove all given id's.\
![img_15.png](img_15.png)\
And the last, but not list thing that we do in our code, we move the modified data to our import folder.\

.... AND thats all Folks ....



