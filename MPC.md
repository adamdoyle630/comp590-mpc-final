# MPC Calculation Process
To complete MPC calculations our system follows a leader-follow heuristic where Party 1 is the leader and instructs all the other parties on their computation. Although Party 1 is the leader, this party learns nothing than if we were to do this calculations remotely and then put the data is a public sharing location. Each party's privacy is protected by properly placed encryption and use of MPC computation techniques such as beaver triples. Instead of using APIs and discrete servers, our team decided to use a serverless computing architecture where all of our computation happens through the invocation of cloud functions, reducing the complexity, cost, and managment of an MPC system.

## Mean
1. **Party 1** calculates its local sum for the given statistic.
2. **Party 1** calls API endpoings that provide the local sum for **Party 2** and **Party 3**
3. Finally **Party 1** sums up the aggregated shares from each party and divides by the number of data points
4. Returns that value as a json object

## Standard Deviation
1. **Party 1** first calculates the mean using the steps detailed above (calls the cloud function)
2. **Party 1** now generates beaver triples for every multiplication that will occur (one for each row as we are calculating the squared difference)
3. The beaver triple shares for **Party 1** are unencrypted but the shares for **Party 2** and **Party 3** are encrypted under their public key (PKE done using PyNaCl), respectively
4. **Party 1** will calculate the beaver mask using its beaver triples and shares of data
5. **Party 1** calls cloud functions providing **Party 2** and **Party 3** with the encrypted beaver triple shares which are decrypted using the party's secret key, returning the masked values of e and d
6. **Party 1** computes the complete value of e and d then uses this to calculate the squared difference of all its shares
7. **Party 2** and **Party 3** do a similar computation using the collaboratively calculated e and d values to calculate each squared difference and return the aggregated sum. This provides the security of the data as no individual's share can be determined from the aggregation of sums.
8. **Party 1** sums the aggregated sums from each party dividing this by the number of rows and square rooting to find the standard deviation
9. Returns the standard deviation as json object

## Correlation
1. **Party 1** gets information regarding two statistics and will work to calculate the correlation between these variables.
2. To calculate this, we need the dot product between the two statistics, complete sum of statistic 1, complete sum of statistic 2, mean of statistic 1, mean of statistc 2, sd of statistic 1, and sd of statistic 2.
3. **Party 1** calls predefined cloud end points to get the data of each of these values as the MPC setup is made to return summations of statistics, means of statistics, standard deviations of statistics, and beaver multiplication between two statistics.
4. Using the correlation formula we calculate the correlation and return this value.