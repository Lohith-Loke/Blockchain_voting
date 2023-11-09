# Blockchain Voting using Blind signatures 
 The aim is to make elections more transparent and add a verifiability to system ensuring all votes will be considered for votes.
we try to adhere to ideal voting system suggested by [1].
we used RSA encription scheme for signing,encripting,this can be extended to other encription schemes


## The Idea 
Elections are conducted by an Authority offfen called **Election Commision** usally relaying on centralized datbase of all voters with personal infomation to identify them. we expect same to be handled by Election commition to authenticate Voter with their keys 

Election Candidates generate their keypairs and make public keys avalble on the VoteBank server.The Part about storing private keys of cantidates needs to be cenralized.This is to prevent early results on elections.

Blockchain 
The vote with signature Votebank encripted with candidate's key is presented by voters to Miner pool's.
miners verify the signature,check for Dubble vote and add to public blockchain.With longest chain rule present it makes easy to get single longest chain.

results are Computed using candiates's private keys reveled at end of election.The vote is decripted reveling whom the vote was casted to.

## Mathy stuff 
### RSA
key terminologys

P,Q -> very large prime number <br>
n -> (P x Q)<br>
d -> also refferd as Φ(n) is (P-1)*(Q-1)<br>
e ->  1< e < d and Not be a factor of d<br>
Private key <d, n> <br>
Public key <e, n> <br>

#### Encription 
    c=(mᵉ)mod n # m -> messege 
#### Decription 
    (cᵈ)mod n

#### Blind signature 
    m'= (m*rᵉ)mod n
    s'= m'ᵈ mod n
    s= (s'*r') mod n
    s= mᵈ mod n as  rᵉᵈ=r mod N

__Note__ : To mitigate risk of unblinding [2] messege we add salt to messege and encript with public key of cantidates.and candidates keep their keys private till end of election.

## how to Run
Structure of project 
its divided into folder for each roal in the elections  

Create super user in all 3 servers 
using 
````
python manage.py createsuperuser
````
__Note__ : To run the server use 'r' file present in root folder along with manage.py this is to prevent port clash from servers


### Filling Data

using admin credenatial login to admin page. 
 - Auth server fill details of all voters. Add Elction type details to prevent resuse of same keys  
 - Votebank add all cadidates that are contesting
 - Miner create a genis Block with Top hash being "genisis"

what each server's do 

In Authserver fill details of the voter that are elibale to vote. accepts a get request with details to provider signed tocken that is used in elcetion.

In Votebank create a candidates and thair affiliation (party tey represent) and Symbol they use this auto-generates candidates keys.
It accepts get request for candidates and provides their detals to voter(incuding public keys). 
It accepts a post request to verify and sign the blind messege.This will provide Public keys for verification of this vote till end of election

Miner accepts all votes that is submitted to them. vote is signed messege is unblinded with r'. Miners Mine all votes to build longest Blockchain.
we can add a reward function to system similar to Block chain.

## Future work 
additon of ring signatures to the system to improve decuppling of voter's identity and vote

## Reffrences
```
[1] Taş, Ruhi, and Ömer Özgür Tanrıöver. 2020. "A Systematic Review of Challenges and Opportunities of Blockchain for E-Voting" Symmetry 12, no. 8: 1328. https://doi.org/10.3390/sym12081328
