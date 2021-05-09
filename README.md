# nomind
A rapid program to convert gene name list to a desired format

MANUAL: NOMIND
Nomind is an application that was developed to convert a large list of gene names to three common nomination formats.

Input:
•	Nomind takes gene names preferably separated by a newline character. Additionally, any list that separates gene names by any blank character can be given as input. 
•	In the input, various formats are accepted. (synonyms, previous symbols, etc.)
•	Gene names can be converted to NCBI, Ensembl, approved symbol formats.
Output:
•	Nomind yields converted gene names as a list which can be selected in the website.
•	Nomind creates a .csv file that can be downloaded. The file includes converted list as well as the input.
Options:
•	“Download .csv file” option is used for creating a .csv file link.
•	“Include problematic names in the converted list” option is used whether to include the gene names that have multiple outputs and the ones that were not named in the selected format.
IN CASE:
If one wishes to update the database:
1.	Please create a txt file that contains gene names in the following order “1-Approved symbol 2-Previous symbols 3-Synonyms 4-NCBI Gene ID(supplied by NCBI) 5-Ensembl ID(supplied by Ensembl) “. Gene names in the file must be separated by a tab(\t). 
  a.	The file can be downloaded from HUGO: https://www.genenames.org/download/custom/
  b.	The file can be modified manually, however, this can damage the file. Please be careful modifying the file.
2.	Please run 3.py and 4.py in the folder.
  a.	1.py and 2.py are backup files. Please do not change them.
  b.	file.csv in the folder must be deleted. 
3.	Please start the application.
  a.	App.py uses the sqlite3 database whereas app_test.py uses a dictionary. App.py is more convenient yet much slower. 

Developer: Gün Kaynar, September 2019, @Ciceklab, Bilkent University.
