# Call detail records (CDR) generator
## About
Call detail record (cdr) generator simulates a month of call detail records on a local level (e. g. one country). The properties of simulated features were extracted from a real-world local telco data. In addition, the generator is able to simulate two distinct situation appearing in real-life, which might be hard to capture even in real datasets.

## Usage
To run the generator, use the line 
```
python3 main.py
```
in the terminal or simply run the `main.py` in the prefered IDE.


## Parameters
There are three parameter files in the `./resources` folder: `params.json`, `situation1params.json` and `situation2params.json`. The params.json file contains all of the required parameters to generate simple cdr data. You may change the parameters in order to alter the generated data. 
- 'cutomerNum' is the number of customers in the simulation;
- 'operatorNum' is the number of operators in the simulation;
- 'callNum' is the number of maximum calls one user can make;
- 'maxFriends' is the maximum number of friends one user can have;
- 'maxAcquaintances' is the maximum number of acquaintances on user can have;
- 'startDate' is the beginning date of the simulation;
- 'situation' indicates which situation will be used in the simulation. 0 indicates normal flow.

### Situation 1
This situation simulates increased telecommunications network load in the whole area. It affects every company and every user. The default parameters (already given in the `situation1params.json` file) simulated New Years Eve. 
- 'probFriend' is the probability to call a friend during selected time period (the values are between 1 and 10, where 2 would mean a probability of calling a friend equal $P=0.2$);
- 'probAcquaintant' is a probability to call an acquaintance;
- 'probOther' is a probability to call someone that is not in the users network of people;
- 'dateTimeFrom' is a time at which the event starts;
- 'dateTimeTo' is a time at which the event ends.

### Situation 2
This situation simulates a cell tower failure. This affects mostly one company, since the people in the area of the failed tower are not able to call anyone. However, users from other companies, who are calling the users in range of the failed tower, will also fail to communicate. The generator randomly selects a company, which will be responsible for the failed tower and according to the station size, adds a number of users into the unreachable area. All the incoming and outcoming calls of those users will be failed.
- 'stationSize' is the percentage of users in the failed station company, that will be unreachable;
- 'failureStart' is the beginning of the failed station event;
- 'failureEnd' is the ending of the failed station event.

## Results
The results are given in the csv files. The main generator results are stored in the './results/cdr_data.csv' directory. Example results:

| Caller id | Caller company | Receiver id | Receiver company | Timestamp       | Duration s |
| --------- | -------------- | ----------- | ---------------- |---------------- | ---------- |
| 33498     | Kompanija3     | 41629       | Kompanija3       | 17-01-21 16:15  | 0          |
| 45450     | Kompanija3     | 35120       | Kompanija3       | 18-02-21 17:12  | 80         |
| 34971     | Kompanija2     | 23577       | Kompanija2       | 13-10-21 12:53  | 77         |
| 33498     | Kompanija3     | 42370       | Kompanija1       | 19-05-21 22:05  | 148        |
| 27409     | Kompanija1     | 33367       | Kompanija3       | 10-05-21 09:22  | 156        |

For the situation 1, there is a possibility to generate only the additional increased flow results, generated during the event period. These results are stored in the './results/cdr_situation1.csv'.

# Citation
The article describing this generator was accepted to the IVUS2021 conference.

# License
Distributed under the The MIT License.