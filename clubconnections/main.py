import pandas as pd
from numpy import random as r
import numpy as np
import os

if os.path.exists('OUTPUT iNDy Club Connections Participation - Master.csv'):
    os.remove('OUTPUT iNDy Club Connections Participation - Master.csv')
if os.path.exists('Match Table.csv'):
    os.remove('Match Table.csv')


# import data
df = pd.read_csv('iNDy Club Connections - Master.csv',
                 index_col='ID')

# convert prior pairings list to np.array
for i in range(df.shape[0]):
    eList = df.iloc[i]['prior_pairings']
    eList = list(map(int, eList.split(',')))
    df.at[i+1, 'prior_pairings'] = eList


# get list of all IDs
ID_list = df.index.values

# TODO: create list of participating IDs
participantIDs = []
for i in range(len(ID_list)):
    testID = ID_list[i]
    optStatus = df.loc[testID]['opt_in']

    if optStatus:
        participantIDs.append(testID)
    else:
        pass

pot_matches = participantIDs.copy()

# flag for odd num of participants
oddNum = len(pot_matches) % 2

# create match column
monthPairName = 'Current Period'

# set values for match columns to blank
df[monthPairName] = None

# TODO: exception for odd number of participants, create group of 3 first
# create match df
dfmatch = pd.DataFrame(columns=['First Name', 'Last name', 'Email', '&',
                            'First Name', 'Last name', 'Email', '&',
                            'First Name', 'Last Name', 'Email',
                                'ID1','ID2','ID3'])
j = 0

while len(pot_matches) > 0:
    currentID = r.choice(pot_matches)
    currentOptStatus = df.loc[currentID]['opt_in']
    excludeIDs = df.loc[currentID]['prior_pairings']
    cEmail = df.loc[currentID]['email']
    cFirstName = df.loc[currentID]['first_name']
    cLastName = df.loc[currentID]['last_name']
    pot_matches.remove(currentID)

# get info for pick if picks remain
    pickID = r.choice(pot_matches)
    excludePickIDs = df.loc[pickID]['prior_pairings']
    pickOptStatus = df.loc[pickID]['opt_in']
    pEmail = df.loc[pickID]['email']
    pFirstName = df.loc[pickID]['first_name']
    pLastName = df.loc[pickID]['last_name']

    validPick = False

    while not validPick:
    # verify that current match is not set, potentially unnecessary
        if df.loc[currentID][monthPairName] != None:
            validPick = True
    # # verify pick != currentID (unnecessary)
        elif currentID == pickID:
            pickID = r.choice(pot_matches)
    # verify pick not in exclude list
        elif pickID in excludeIDs:
            if len(pot_matches) == 1:
                print(f'{pot_matches}\nRerun\ncID: {currentID}\npID: {pickID}\ncExcl: {excludeIDs}')
                break
            else:
                pickID = r.choice(pot_matches)
    # TODO: exit when pick is valid
        else:
            pot_matches.remove(pickID)
            validPick = True

    # odd number exception
    if oddNum > 0:
        pick2valid = False
        pickID2 = r.choice(pot_matches)

        while not pick2valid:
            # check for match in excluded list
            if str(pickID2) in excludeIDs or str(pickID2) in excludePickIDs:
                pickID2 = r.choice(pot_matches)

            else:
                pot_matches.remove(pickID2)
                pick2valid = True

        # get pick 2 info
        p2Email = df.loc[pickID2]['email']
        p2FirstName = df.loc[pickID2]['first_name']
        p2LastName = df.loc[pickID2]['last_name']
        excludePickID2s = df.loc[pickID2]['prior_pairings']

        # update info on master table
        df.at[currentID, monthPairName] = f'{pickID},{pickID2}'
        df.at[pickID, monthPairName] = f'{currentID},{pickID2}'
        df.at[pickID2, monthPairName] = f'{currentID},{pickID}'

        # add info to match table
        dfmatch.loc[j] = [cFirstName, cLastName, cEmail, '&',
                      pFirstName, pLastName, pEmail, '&',
                      p2FirstName, p2LastName, p2Email,
                          currentID, pickID, pickID2]
        j += 1

        oddNum = 0

    else:
        # update info on master table
        df.at[currentID, monthPairName] = pickID
        df.at[pickID, monthPairName] = currentID

        # add info to match table
        dfmatch.loc[j] = [cFirstName, cLastName, cEmail, '&',
                      pFirstName, pLastName, pEmail, None,
                      None, None, None,
                          currentID, pickID, None]
        j += 1

# export master table and match table

df.to_csv('OUTPUT iNDy Club Connections Participation - Master.csv')
dfmatch.to_csv('Match Table.csv', index=False)