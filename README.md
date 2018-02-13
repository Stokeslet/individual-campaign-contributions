Donation-Analytic by Amir Mirbagheri
================

Table of Contents
=================

1.  [Introduction](README.md#introduction)
2.  [Packages](README.md#packages)
3.  [Code Details](README.md#code%20details)
4.  [Test](README.md#test)
5.  [Summary](README.md#summary)

Introduction
============

As a data engineer I am interested to analyze loyalty trends in campaign contributions. I have written a clean and scalable python code to find repeat donors and calculated how much they are spending. In my code, I have considered that we are working with streaming data and also these data can be malformed or empty.

Packages
========

I used python 3.5 for developing this code. Needed packages are shown as follow:

1.  numpy
2.  sys

Code Details
============

The code has three major parts: data cleaning, finding repeat donors and calculating repeat donor's contribution.

1. Data Cleaning
----------------

When streaming data is read line by line, needed features (CMTE\_ID, NAME, ZIP\_CODE, TRANSACTION\_DT, TRANSACTION\_AMT, OTHER\_ID) are stored. There are different conditions that if we see them we ignore these data. The rules are as follow

OTHER\_ID must be empty and values for other features must not be empty.

ZIP\_CODE must be digits and at least five digits. Then only the first five digits are stored.

TRANSACTION\_DT must be 8 digits. Then the year is stored.

TRANSACTION\_AMT must be digits. Then this number is rounded and stored.

I have also made 2 new features to have different unique ids for donors ('ID\_DONOR') and ('ID\_UNIQUE\_CMTE' ) recipient. They are made by the following structure:

'ID\_DONOR'='ZIP\_CODE'+'NAME'

'ID\_UNIQUE\_CMTE'=YEAR+ZIP\_CODE+'CMTE\_ID'

Now we can be sure that if 'ID\_DONOR' is the same for an input data, we are dealing with one person (Name and Zip Code are the same for that donor). 'ID\_UNIQUE\_CMTE' is made from year, zip code and CMTE\_ID. This process can help us easily find recipient with the same 'CMTE\_ID' and zip code in the desire year.

2. Finding repeat donors
------------------------

With the new feature 'ID\_DONOR' that I defined, we can easily match them for every input data to check if it is repeated in the prior year and call it as repeat donor. All of 'ID\_DONOR' are stored in a dictionary and if it repeats again in the next year I call that donor as repeat donor.

3. Calculating repeat donor's contribution
------------------------------------------

When the algorithm found the contribution comes from a repeat donor, the code stores the amount of contribution in a new dictionary. Then we have the amount of contribution to every recipient (per year) for every repeat donor. After that we can measure different things such as summation of contributions, number of contributions and percentile ( which is read as an input file).

In the following table you can see what different functions in my code do:

<table style="width:39%;">
<colgroup>
<col width="19%" />
<col width="19%" />
</colgroup>
<thead>
<tr class="header">
<th>Function Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Read_Files</td>
<td>read input files</td>
</tr>
<tr class="even">
<td>Get_Data</td>
<td>make a dictionary and store input data with their keys (names of features) and values</td>
</tr>
<tr class="odd">
<td>Clean_Data</td>
<td>apply different rules to ignore data that do not obey rules, make new features</td>
</tr>
<tr class="even">
<td>Find_Repeat_Donor</td>
<td>match 'ID_DONOR', check the year and report repeat donors</td>
</tr>
<tr class="odd">
<td>Save_Recipient</td>
<td>store amount of contribution for repeat donors to every recipient</td>
</tr>
<tr class="even">
<td>Make_Output</td>
<td>calculate number of contributions, summation and percentile</td>
</tr>
</tbody>
</table>

Test
====

In order to become sure, the code works well, I have tested it with different data. Test\_1: Given test data

Test\_2\_year: In the section FAQ, some data are given to check if the second donation came later in the file what the result is.

Test\_3\_zipcode: I changed the zip code of sixth line from 02895 to 02899. So, we should not consider this as a repeat donor.

Test\_4\_otherid: The OTHER\_ID for seventh data is set to be some value and these data should be ignored.

Test\_5\_percentile: I made some data to have five repeat donors with contributions equal to \[15,20,35,40,50\] and I checked %50 and %75 percentile.

Summary
=======

I have analyzed the contribution of repeat donors from different recipient per year. Percentile, summation and number of contributions are calculated and reported in the output file "repeat\_donors.txt". Different data have given to the code to check consistency of the code facing malformed data and it has passed all tests.
