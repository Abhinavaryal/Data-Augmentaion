# Datasheet for dataset "Assignment 2"


## Motivation

### For what purpose was the dataset created?

The purpose of the dataset is to augment police incident records in order to obtain deeper insights into patterns and correlations within the data to view the data in a different way than in exciting manner. The new creation like ranking will help in obtaining better insights about what incidents are taking place in a certain place.


### Who created the dataset and on behalf of which entity?

Abhinav Aryal, A student at University of Florida undertaking Data Engeering class created this dataset from the help of pre exciting incident dataset from Norman PD.

### Who funded the creation of the dataset?

The bonus obtained from google map($200) and the semester start bonus ($50) obtained from Dr. Grant was used for this project. 


## Composition


### What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)?

Each instance is an enhanced record of a police event that includes more information compaired to the pre-exiciting data on the location, weather, and time of the incident. Compared to the previous data, Weather is complete new to this data set while the other records are augmented records of pre-existing data like location rank for frequency of location, incident rank for frequency of incident

### How many instances are there in total?

This dataset contains all the instance of the previous data set. This isn't a smaller instance of larger dataset but is a augment version of previous dataset. This data set was made by calculating the number of locations for location rank, number of incidents for incident rank and for Weather and Side of town external API's were used.


### What data does each instance consist of?
Day of the Week, Time of Day, Weather, Location Rank, Side of Town, Incident Rank, Nature, EMSSTAT

EMSSTAT is either true or false. True if the incident ori is emssat or the time and location is similar to any record with emsstat as incident ori


### Is there a label or target associated with each instance?

Each incident is for a time and for a location and incident took place, so the nature of the incident can be seen as target to analyse many other things.

### Is any information missing from individual instances?
If the API are not able to calcualte the side of the town then we may an missing information in the instance. 

### Are relationships between individual instances made explicit?
There can be relationship with the case of the same time the incident took place at the same location but the incident ORI is different.

### Are there recommended data splits?

Since the data is not sorted on any basis as seen in the final output, we can have a standard 70, 30 split.

### Are there any errors, sources of noise, or redundancies in the dataset?
The Side of the Town information is not constant with the direction in the location and in the SIDE OF THE TOWN information itself, so that can be a redundancy in the dataset.

### Is the dataset self-contained, or does it link to or otherwise rely on external resources?
The building of the dataset is relied on the working of the Norman PD dataset and the API used to find the side of town and weather at a location at a particular time. The API can have it's own charges based on the usuage and there is no gurantee that the dataset obtained from norman pd will be the internet forever. 

### Does the dataset contain data that might be considered confidential ?
NO

### Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?
Yes, if any type of incident can trigger anxiety in someone, than this dataset containes a wide range of nature of incident data in it.

### Does the dataset relate to people?
Yes, while it doesn't point to a person, it is associated with an incident people have been a part of. 

### Does the dataset identify any subpopulations?
No

### Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset?
No

### Does the dataset contain data that might be considered sensitive in any way?
Most number of incidents in a particular location can be seen in this dataset. 


## Collection process

### How was the data associated with each instance acquired?

For the day of week, time, nature and emssat it was directly taken from the Norman PD dataset. While the weather and side of town is obtioned by using the data from Norman PD and passing it to an API. 

### What mechanisms or procedures were used to collect the data?

Google Map API and Historical Weather API was used for the dataset.

### If the dataset is a sample from a larger set, what was the sampling strategy ?
Not a sample. 

### Who was involved in the data collection process and how were they compensated ?
Students and they were compensated with educational learning. 

### Over what timeframe was the data collected?
It was created and used for learning in the same time. 

### Were any ethical review processes conducted (e.g., by an institutional review board)?
No

### Does the dataset relate to people?
No, not directly collected form people.

### Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources (e.g., websites)?
No 

### Were the individuals in question notified about the data collection?
N/A

### Did the individuals in question consent to the collection and use of their data?
N/A

### If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses?
N/A

### Has an analysis of the potential impact of the dataset and its use on data subjects (e.g., a data protection impact analysis) been conducted?
N/A


## Preprocessing/cleaning/labeling

### Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)?
In various cases, tokenization was done and regex was used to seperate needed informations.

### Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data?
No 

### Is the software used to preprocess/clean/label the instances available?
Yes the API's are available.

## Uses

### Has the dataset been used for any tasks already?
No

### Is there a repository that links to any or all papers or systems that use the dataset?
No

### What (other) tasks could the dataset be used for?
The dataset may have use in research on crime analysis, predictive policing, or urban studies, in addition to academic pursuits.

### Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?
There might be reporting biases in the way the reporting might have taken place.

### Are there tasks for which the dataset should not be used?
The data should't be used for policing to assign police to the place that has more cases to avoid bias. 


## Distribution

### Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created?
No

### How will the dataset will be distributed (e.g., tarball on website, API, GitHub)?
No

### When will the dataset be distributed?
No

### Have any third parties imposed IP-based or other restrictions on the data associated with the instances?
NO

### Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?
No


Maintenance

### Who is supporting/hosting/maintaining the dataset?
The creater, Abhinav Aryal

### How can the owner/curator/manager of the dataset be contacted (e.g., email address)?
Email: abhinavaryal@ufl.edu

### Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)?
If there are changes in the dataset it can be obtain from my github. Abhinavaryal(repo concerned with cis6930-assignment2)

### If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g., were individuals in question told that their data would be retained for a fixed period of time and then deleted)?
No

### Will older versions of the dataset continue to be supported/hosted/maintained?
Yes

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?
Running the code and extracting the dataset will be the first set, this can be seen from my README file. For any other help you should contact me on my email[abhinavaryal@ufl.edu]

