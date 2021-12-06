# Group_Diffie-Hellman
Group Diffie-Hellman tree scheme<br><br>
Input Format<br><br>
The first line of the input file will contain two integers, p and g, separated by spaces. Both 
integers will be less than 100 digits long and will represent a prime 
number and a generator for that prime number, respectively.<br><br>
The following line will contain a single integer, n (n < 1000), representing the number of 
modifications to the tree structure in the Group Diffie-Hellman protocol or queries for particular 
keys.<br><br>
The first of these lines will have a unique format because it will add two users at once. Its format 
is as follows:<br>
USER1 secretkey1 USER2 secretkey2 KeyID<br><br>
Both users will be uppercase strings of length 20 or less and both secretkeys will be positive 
integers less than p. These two users will be added to the group first and share a single secret 
key. KeyID will be a string of 1 to 20 uppercase characters labeling that particular shared key.
The following n-1 lines will have one of the three following formats:<br><br>
ADD USER1 secretkey1 USER2 secretkey2 KeyID<br>
DEL USER1 secretkey2<br>
QUERY KeyID<br><br>
The first format specifies adding a user. USER1 represents the sponsor for the new user while 
USER2 represents the new user to be added. Both users must pick new secret keys, which are 
secretkey1 and secretkey2, respectively. KeyID will be a string of 1 to 20 uppercase characters 
labeling that particular shared key.<br><br>
The second format describes deleting USER1. <br><br>
The third format makes a query for a particular shared key with the id KeyID. For each of these 
lines, your program should output on a single line the value of the specified key at that point in 
time.<br><br>
You are guaranteed that all queries are for valid keys in the tree, that all add commands list a 
valid user for USER1 and a new user for USER2. Each different user will have a unique 
identifying string as will each key. After the first operation, the tree will always have at least two 
users. (Thus, the second request in the file must either be a query or an add and no deletes can be 
made until there are at least three users.)<br><br>
Output Format<br>
For each query, output a single integer on a line by itself satisfying the given query.<br><br>
Sample Input<br>
29 3 12<br>
21 18<br>
ALICE 7 BOB 5 K0 15<br>
QUERY K0 3<br>
ADD ALICE 3 CAROL 13 K1 17<br>
QUERY K0 7<br>
QUERY K1 20<br>
ADD CAROL 6 DAVID 20 K2 20<br>
QUERY K0 24<br>
QUERY K1 4<br>
QUERY K2 8<br>
ADD CAROL 2 EARL 17 K3 27<br>
QUERY K0 1<br>
QUERY K1 11<br>
QUERY K2 1<br>
QUERY K3<br>
DEL CAROL 21<br>
QUERY K0<br>
QUERY K1<br>
QUERY K2<br>
DEL ALICE 23<br>
QUERY K0<br>
QUERY K2<br>
