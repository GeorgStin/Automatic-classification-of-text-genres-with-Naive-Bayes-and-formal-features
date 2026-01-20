This is a genre classifier, that uses Naive Bayes algorithm and has two main modes:

a. TRAIN-mode
b. CLASSIFY-mode
----------------------------------------------------------------------------------------------------

### HOW TO RUN? ###

You can run the programm from your command-line (make sure that NLTK is installed on your computer).
It looks like:
	python script.py classify dataset_de.txt Science/01.txt DE None
	or
	python script.py train my_dataset.txt Science DE science

Here you find more information about required parameters.
The following parameters are required to run, e.g.:

| ------ |   SCRIPT   |   MODE   |    DATASET     |     TEXT/S     | LANGUAGE |  GENRE  | 
| ------ | ---------- | -------- | -------------- | -------------- | -------- | ------- |
| python | script.py  | classify | dataset_de.txt | Science/01.txt | de       | None    |
| python | script.py  | train    | my_dataset.txt | Science_ru     | ru       | science |

-----------------------------------------     SCRIPT     -------------------------------------------
The name of the python script with the source code (script.py per default).

-----------------------------------------      MODE      -------------------------------------------
1. classify - to classify one or more texts.
   The result(s) will be shown in the console and will be saved in the result.txt.

2. train - to train your own dataset, which you will use to classify other texts.

-----------------------------------------     DATASET     ------------------------------------------
You should write the filename (with .txt extension) for a dataset with trained features.

- In the CLASSIFY-MODE you should select a dataset with already trained features
  on the basis of which the classification of the new text will be made.
  You can also use two default datasets:
  dataset_de.txt (for German language) or dataset_ru.txt (for Russian).

- In the TRAIN-MODE you should write a filename for your own dataset
  where the new data from the new text(s) will be saved.
  For example: my_dataset.txt
  If you select a file that already contains some feature-information,
  then it will be supplemented with new data from new text(s).
  If there is no file, it will be created automatically.

----------------------------------------     TEXT(S)     -------------------------------------------
You should select a target text (or a folder with many texts) for your training or classifying.

If you train/classify only one text, write the filename with .txt extension.
For example: Science/01.txt

If you train/classify many texts, write the name of folder.
For example: Science

NOTE: If you use the TRAIN-MODE for many texts, be sure that your folder contains ONLY texts
      of the SAME genre.

You can also select one of the default text or text sets for your training or classification:
    
    ##################                    TEXT/S                       ##################
    SCIENCE DE:         FICTION DE:                 SCIENCE RU:         FICTION RU:
    Science/01.txt      Fiction/01_Martin.txt       Science_ru/01.txt   Fiction_ru/01.txt
    Science/02.txt      Fiction/02_Carroll.txt      Science_ru/02.txt   Fiction_ru/02.txt
    Science/03.txt      Fiction/03_Doyle.txt        Science_ru/03.txt   Fiction_ru/03.txt
    Science/04.txt      Fiction/04_Meyer.txt        Science_ru/04.txt   Fiction_ru/04.txt
    Science/05.txt      Fiction/05_Christie.txt     Science_ru/05.txt   Fiction_ru/05.txt
    Science/06.txt      Fiction/06_Lewis.txt        Science_ru/06.txt   Fiction_ru/06.txt
    Science/07.txt      Fiction/07_Dumas.txt        Science_ru/07.txt   Fiction_ru/07.txt
    Science/08.txt      Fiction/08_Kafka.txt        Science_ru/08.txt   Fiction_ru/08.txt
    Science/09.txt      Fiction/09_Hesse.txt        Science_ru/09.txt   Fiction_ru/09.txt
    Science/10.txt      Fiction/10_Mann.txt         Science_ru/10.txt   Fiction_ru/10.txt
    Science/11.txt      Fiction/11_Dickens.txt      Science_ru/11.txt   Fiction_ru/11.txt
    Science/12.txt      Fiction/12_Remarque.txt     Science_ru/12.txt   Fiction_ru/12.txt
    Science/13.txt      Fiction/13_Rowling.txt      Science_ru/13.txt   Fiction_ru/13.txt
    Science/14.txt      Fiction/14_Twain.txt        Science_ru/14.txt   Fiction_ru/14.txt
    Science/15.txt      Fiction/15_Dostojewski.txt  Science_ru/15.txt   Fiction_ru/15.txt
    Science/16.txt      Fiction/16_Wilde.txt        Science_ru/16.txt   Fiction_ru/16.txt

    ##################                   TEXT SETS                     ##################
    testset_1_de	testset_2_de		   testset_3_de		testset_4_de
    testset_1_ru	testset_2_ru		   testset_3_ru		testset_4_ru
    #####################################################################################

---------------------------------------     LANGUAGE     -------------------------------------------
Select the language of text(s).
For example: de or RU

---------------------------------------      GENRE      --------------------------------------------
You should write the genre of your target text(s).
- In the CLASSIFY-MODE it plays no role, (but you STILL NEED WRITE something, e.g. just "None").

- In the TRAIN-MODE write the genre that your target text has.
  For example: science or fiction
----------------------------------------------------------------------------------------------------

### HOW TO EVALUATE? ###

There are two ways:
1. You can just classify one of the (new) texts separately and compare the result with the real genre.

2. You can create a folder with many texts and run the script in the same way (in the classify-mode).
   Then compare the results in the result.txt file.
   It is a smart decision to name your files like "name_genre.txt", because the results look like:
   ['testset/name_genre.txt', 'science'].
   
   Before evaluation you must CLEAR or just DELETE result.txt.
   In this way you will not confuse new results with old evaluations.

   For the cross-validation be sure, that your target texts are NOT in the dataset.