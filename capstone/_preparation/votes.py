#!/usr/bin/env python
import sys
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, bernoulli

TARGET_CUT_PERC = 80.
MAX_GOOD_VAR = 0.35
VOTES_PER_USER_RANGE = [5., 30.]
BAD_USERS_RATIO = [0.001, 0.005]

def compute_n_votes(df):
    df['p_el_bis'] = df['p_el_debiased']
    df['p_cs_bis'] = df['p_cs_debiased']
    
    df.loc[df['p_cs_debiased'] >= 0.8, 'p_el_bis'] = 1 - df[df['p_cs_debiased'] >= 0.8]['p_cs_debiased']
    df.loc[df['p_el_debiased'] >= 0.8, 'p_cs_bis'] = 1 - df[df['p_el_debiased'] >= 0.8]['p_el_debiased']

    df['p_el_bis'] = df.apply(fill_p_el, axis=1)
    df['p_cs_bis'] = df.apply(fill_p_cs, axis=1)


def fill_p_el(row):

    if max(row['p_el_debiased'], row['p_cs_debiased']) > 0.2:
        if row['p_el_debiased'] <= row['p_cs_debiased']:
            return 1 - row['p_cs_debiased']
        else:
            return row['p_el_debiased']
    else:
        return row['p_el_debiased'] + (1 - row['p_el_debiased'] - row['p_cs_debiased'])/2.

def fill_p_cs(row):

    if max(row['p_el_debiased'], row['p_cs_debiased']) > 0.2:
        if row['p_el_debiased'] > row['p_cs_debiased']:
            return 1 - row['p_el_debiased']
        else:
            return row['p_cs_debiased']
    else:
        return row['p_cs_debiased'] + (1 - row['p_el_debiased'] - row['p_cs_debiased'])/2.



def compute_votes(row):

    votes_cs = int(row['p_cs_bis']*row['nvote'])
    votes_el = int(row['p_el_bis']*row['nvote'])
    new_nvotes = votes_el + votes_cs

    new_p_el = float(votes_el) / float(new_nvotes) 
    new_p_cs = float(votes_cs) / float(new_nvotes)
    
    if row['p_el_bis'] > 0.8:
        if new_p_el < 0.8:
            votes_el = np.ceil(new_nvotes*0.8)
            votes_cs = new_nvotes - votes_el
        elif new_p_el == 0.8:
            votes_el += 1
            votes_cs -= 1
    elif row['p_cs_bis'] > 0.8:
        if new_p_cs < 0.8:
            votes_cs = np.ceil(new_nvotes*0.8)
            votes_el = new_nvotes - votes_cs
        elif new_p_cs == 0.8:
            votes_cs += 1
            votes_el -= 1
    else:

        while new_p_cs > 0.8:
            votes_cs -=1
            votes_el +=1
            new_p_cs = float(votes_cs) / float(new_nvotes)

        while new_p_el > 0.8:
            votes_el -=1
            votes_cs +=1
            new_p_el = float(votes_el) / float(new_nvotes)
            
    return votes_cs, votes_el

def fill_votes_cs(row):

    votes_cs, votes_el = compute_votes(row)

    return votes_cs

def fill_votes_el(row):

    votes_cs, votes_el = compute_votes(row)

    return votes_el


def build_votes(df, n_users):

    list_of_votes = []
    for ind, (objid, votes_cs, votes_el) in df[['dr7objid', 'n_votes_cs', 'n_votes_el']].iterrows():
        list_of_votes += [(objid, 1, np.random.randint(1, n_users + 1)) for i in range(votes_cs)]
        list_of_votes += [(objid, 0, np.random.randint(1, n_users + 1)) for i in range(votes_el)]

    new_df = pd.DataFrame(np.array(list_of_votes), columns=['dr7objid', 'vote', 'user_id'])
    return new_df.sample(frac=1).reset_index(drop=True)


def compute_user_variances(votes_df, user_id=None):

    means_df = pd.DataFrame(votes_df.groupby('dr7objid')['vote'].mean())
    means_df['dr7objid'] = means_df.index

    vars_df = pd.merge(votes_df, means_df, on='dr7objid')
    vars_df['diff_votes'] = (vars_df['vote_y'] - vars_df['vote_x'])
    vars_df['diff_votes_2'] = vars_df['diff_votes']**2

    user_vars_df_mean = vars_df.groupby('user_id')['diff_votes_2'].mean()
    user_vars_df_sum = vars_df.groupby('user_id')['diff_votes'].sum()
    user_vars_df = pd.concat([user_vars_df_mean, user_vars_df_sum], axis=1)

    if user_id:
        user_vars_df = user_vars_df.loc[user_id]
    return user_vars_df

def correct_user_votes(votes_df, n_users, max_niter=5, max_good_var=None):

    votes_df = votes_df.copy()

    n_iter = 0
    while n_iter < max_niter:

        # identify bad users
        bad_users = get_bad_users(votes_df, max_good_var)

        if len(bad_users) == 0:
            print('cleaned bad users at {} iteration'.format(n_iter + 1))
            break

        # correct bad users
        for user_id in bad_users:
            correct_bad_user(votes_df, user_id, n_users)
        
        n_iter += 1

    if n_iter >= max_niter:
        print('failed to clean bad users!!\n {}'.format(get_bad_users(votes_df)))

    return votes_df

def get_bad_users(votes_df, max_good_var=None):

    vars_df = compute_user_variances(votes_df)
    if max_good_var is None:
        n = norm(loc=vars_df['diff_votes_2'].mean(), scale=vars_df['diff_votes_2'].std())
        max_good_var = n.ppf(0.99)
    bad_users = vars_df[vars_df['diff_votes_2'] > max_good_var].index
    return bad_users


def correct_bad_user(votes_df, user_id, n_users):

    n_votes_user = (votes_df['user_id'] == user_id).sum()
    votes_df.loc[votes_df['user_id'] == user_id, 'user_id'] = np.random.randint(1, n_users + 1, n_votes_user)


def create_bad_user(votes_df, user_id, min_value=None):

    vars_df = compute_user_variances(votes_df)
    if min_value is None:
        n = norm(loc=vars_df['diff_votes_2'].mean(), scale=vars_df['diff_votes_2'].std())
        min_value = n.ppf(0.99)

    means_df = pd.DataFrame(votes_df.groupby('dr7objid')['vote'].mean()).sample(frac=1)
    means_df['dr7objid'] = means_df.index

    var_user = - np.inf

    bad_user = pd.DataFrame([], columns=['dr7objid', 'vote', 'user_id'])
    init_index = 0
    while var_user < min_value:
        chunk_size = np.random.randint(5, 10)
        new_votes = means_df.iloc[init_index:init_index + chunk_size].copy()
        new_votes['vote'] = new_votes.apply(shitty_shit, axis=1)
        new_votes['user_id'] = user_id 
        init_index += chunk_size
        bad_user = pd.concat([bad_user, new_votes], ignore_index=True)

        prov_votes = pd.concat([votes_df, bad_user], ignore_index=True)
        prov_votes['vote'] = pd.to_numeric(prov_votes['vote'])
        df_var_user = compute_user_variances(prov_votes, user_id=user_id)
        var_user = df_var_user['diff_votes_2']

    return bad_user
        
def shitty_shit(row):

    p = 1 - row['vote']
    return int(bernoulli.rvs(p, size=1))


def add_bad_users(votes_df, n_bad_users, min_value):

    init_user_id = votes_df['user_id'].max() + 1
    max_user_id = init_user_id + n_bad_users
    votes_df_with_bads = votes_df.copy()

    for user_id in range(init_user_id, max_user_id):
        bad_user = create_bad_user(votes_df_with_bads, user_id)
        votes_df_with_bads = pd.concat([votes_df_with_bads, bad_user], ignore_index=True)
        votes_df_with_bads['vote'] = pd.to_numeric(votes_df_with_bads['vote'])
    return votes_df_with_bads

def remove_users(votes_df, user_id_list):

    for user_id in user_id_list:
        votes_df = votes_df[votes_df['user_id'] != user_id]

    return votes_df


def shuffle_user_id(votes_df):

    new_votes_df = votes_df.sample(frac=1).reset_index(drop=True)

    user_ids = new_votes_df['user_id'].unique()
    new_user_ids = np.random.permutation(user_ids)
    d = dict(zip(user_ids, new_user_ids))
    
    new_votes_df['user_id'] = new_votes_df.apply(lambda x, d: d[x['user_id']], axis=1, args=(d,))

    return new_votes_df

def generate_good_votes(args):
    
    np.random.seed(0)

    input_csv = args.or_csv_file
    or_df = pd.read_csv(input_csv)
    old_n_el = (or_df['p_el_debiased'] > TARGET_CUT_PERC/100.).sum()
    old_n_cs = (or_df['p_cs_debiased'] > TARGET_CUT_PERC/100).sum()

    # Modify p_el an p_cs to make them add up to 1
    # check that the percentages for each galaxy type are not changed
    compute_n_votes(or_df)
    new_n_el = (or_df['p_el_bis'] > TARGET_CUT_PERC/100.).sum()
    new_n_cs = (or_df['p_cs_bis'] > TARGET_CUT_PERC/100.).sum()
    check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)

    # Compute the number of votes to keep the number of galaxies of each type
    or_df['n_votes_el'] = or_df.apply(fill_votes_el, axis=1)
    or_df['n_votes_cs'] = or_df.apply(fill_votes_cs, axis=1)
    new_n_el = (or_df['n_votes_el']/(or_df['n_votes_el'] + or_df['n_votes_cs']) > TARGET_CUT_PERC/100.).sum()
    new_n_cs = (or_df['n_votes_cs']/(or_df['n_votes_el'] + or_df['n_votes_cs']) > TARGET_CUT_PERC/100.).sum()
    check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)

    # generate votes DataFrame
    n_votes = (or_df['n_votes_el'] + or_df['n_votes_cs']).sum()
    min_users = int(n_votes/VOTES_PER_USER_RANGE[1])
    max_users = int(n_votes/VOTES_PER_USER_RANGE[0])
    n_users = np.random.randint(min_users, max_users)
    print('initial number of users = {}'.format(n_users))
    votes_df = build_votes(or_df, n_users)
    votes_df = correct_user_votes(votes_df, n_users, 20, MAX_GOOD_VAR)
    print('final number of good users = {}'.format(len(votes_df['user_id'].unique())))
    max_good_user_id = votes_df['user_id'].max()
    
    # Check that the number of galaxies of each type is coherent
    votes_p_df = pd.DataFrame(votes_df.groupby('dr7objid')['vote'].mean())
    new_n_el = (votes_p_df['vote'] < (100. - TARGET_CUT_PERC)/100.).sum()
    new_n_cs = (votes_p_df['vote'] > TARGET_CUT_PERC/100.).sum()
    check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)
    
    # save votes Dataframe to csv
    votes_df.to_csv(args.dest_csv_file, index=False)

def add_bad_votes(args):
    
    votes_df = pd.read_csv(args.or_csv_file)
    n_users = len(votes_df['user_id'].unique())
    max_good_user_id = votes_df['user_id'].max()
    votes_p_df = pd.DataFrame(votes_df.groupby('dr7objid')['vote'].mean())
    old_n_el = (votes_p_df['vote'] < (100. - TARGET_CUT_PERC)/100.).sum()
    old_n_cs = (votes_p_df['vote'] > TARGET_CUT_PERC/100.).sum()
    
    # Add some bad users to be filtered out
    n_bad_users = np.random.randint(int(BAD_USERS_RATIO[0]*n_users), int(BAD_USERS_RATIO[1]*n_users))
    votes_df = add_bad_users(votes_df, n_bad_users, MAX_GOOD_VAR)
    print('inserted {} bad users'.format(n_bad_users))

    # pop bad users with variance lower than limit and shuffle user ids
    user_vars_df = compute_user_variances(votes_df)
    bad_to_pop = user_vars_df[(user_vars_df.index > max_good_user_id) & (user_vars_df['diff_votes_2'] <= MAX_GOOD_VAR)]
    print('found {} bad users with low variances. Going to remove them'.format(len(bad_to_pop)))
    votes_df = remove_users(votes_df, bad_to_pop.index)
    votes_df = shuffle_user_id(votes_df)

    #Plot the distribution of the variances
    user_vars_df = compute_user_variances(votes_df)
    ax = user_vars_df['diff_votes_2'].hist(bins=100)
    plt.show()
    
    # Check that the number of galaxies of each type is coherent after filtering bad users
    bad_users_ids = user_vars_df[user_vars_df['diff_votes_2'] > MAX_GOOD_VAR].index
    good_votes_df = votes_df[~votes_df['user_id'].isin(bad_users_ids)]      
    votes_p_df = pd.DataFrame(good_votes_df.groupby('dr7objid')['vote'].mean())
    new_n_el = (votes_p_df['vote'] < (100. - TARGET_CUT_PERC)/100.).sum()
    new_n_cs = (votes_p_df['vote'] > TARGET_CUT_PERC/100.).sum()
    check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)

    # Dump votes_df to file
    votes_df.to_csv(args.dest_csv_file, index=False)

def check_votes(args):
    
    # read csvs
    class_df = pd.read_csv(args.or_csv_file, index_col='dr7objid')
    votes_df = pd.read_csv(args.votes_file, index_col='dr7objid')
    target_cut = args.target_cut
    
    # compute classes from vote percentage
    votes_p_df = pd.DataFrame(votes_df.groupby('dr7objid')['vote'].mean())
    
    votes_p_df['votes_el'] = 0
    mask_el = (votes_p_df['vote'] < (100. - target_cut)/100.)
    votes_p_df.loc[mask_el, 'votes_el'] = 1
    
    votes_p_df['votes_cs'] = 0
    mask_cs = (votes_p_df['vote'] > target_cut/100.)
    votes_p_df.loc[mask_cs, 'votes_cs'] = 1
    
    votes_p_df['votes_uc'] = 0
    mask_uc = (~mask_el) & (~mask_cs) 
    votes_p_df.loc[mask_uc, 'votes_uc'] = 1
    
    
    # Compute class from original probabilities
    class_df['or_el'] = 0
    mask_el = (class_df['p_el_debiased'] > target_cut/100.)
    class_df.loc[mask_el, 'or_el'] = 1
    
    class_df['or_cs'] = 0
    mask_cs = (class_df['p_cs_debiased'] > target_cut/100.)
    class_df.loc[mask_cs, 'or_cs'] = 1
    
    class_df['or_uc'] = 0
    mask_uc = (~mask_el) & (~mask_cs) 
    class_df.loc[mask_uc, 'or_uc'] = 1
    
    # join class_df and votes_df
    joined_df = pd.concat([class_df, votes_p_df], axis=1)
    
    # Check the equality between images classification
    check_df_equality(joined_df, 'votes_el', 'or_el')
    check_df_equality(joined_df, 'votes_cs', 'or_cs')
    check_df_equality(joined_df, 'votes_uc', 'or_uc')
    
    
def check_df_equality(df, field_1, field_2):
    
    type1 = df[field_1].dtype
    type2 = df[field_2].dtype
    
    if type1 != type2:
        raise Exception("Types don't match {} != {}".format(type1, type2))
    elif type1 == np.int64:
        mask = df[field_1] != df[field_2]
    elif type1 == np.float64:
        mask = ~np.isclose(df[field_1], df[field_2])
        
    n_errors = len(df[mask])
    if n_errors == 0:
        print('NO errors for fields {} and {}'.format(field_1, field_2))
    else:
        print('Errors for fields {} and {}: {}'.format(field_1, field_2, n_errors))
    

def define_arguments():
    
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(help='sub-command help')
    
    # parser for the generate_good_votes action
    parser_good_votes = subparsers.add_parser('generate_good_votes',
        help='generates a csv with a simulates votes sample from the original Galaxy Zoo data')
    parser_good_votes.add_argument('--or_csv_file', '-o', required=True,
        help='input csv file with ZooSpec data')
    parser_good_votes.add_argument('--dest_csv_file', '-d', required=True,
        help='output csv file with correct votes data')
    parser_good_votes.set_defaults(func=generate_good_votes)
    
    # parser to generate bad votes
    parser_bad_votes = subparsers.add_parser('add_bad_votes',
        help='Generate csv of simulated votes containing good and bad votes')
    parser_bad_votes.add_argument('--or_csv_file', '-o', required=True,
        help='csv with good votes')
    parser_bad_votes.add_argument('--dest_csv_file', '-d', required=True,
        help='csv with good and bad votes')
    parser_bad_votes.set_defaults(func=add_bad_votes)
    
    # parser to check ZooSpec data against votes
    parser_check_votes = subparsers.add_parser('check_votes',
        help='Check that the objects have the same target in the original dataset and the votes data')
    parser_check_votes.add_argument('--or_csv_file', '-o', required=True,
        help='csv file with original ZooSpec data')
    parser_check_votes.add_argument('--votes_file', '-v', required=True,
        help='csv file with simulated votes data')
    parser_check_votes.add_argument('--target_cut', '-t', required=False, default=TARGET_CUT_PERC,
        type=float, help='minimum percentage of votes to decide that the class of an object has been determined')
    parser_check_votes.set_defaults(func=check_votes)
    
    return parser


def check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs):
    if new_n_el != old_n_el:
        raise Exception('Number of elliptics galaxies does not match new = {}, old = {}'.format(new_n_el, old_n_el)) 
    if new_n_cs != old_n_cs:
        raise Exception('Number of spiral galaxies does not match new = {}, old = {}'.format(new_n_cs, old_n_cs)) 
    print('Number of galaxies of each type is preserved:\n elliptics={} spirals={}'.format(new_n_el, new_n_cs))

if __name__ == '__main__':

    parser = define_arguments()
    args = parser.parse_args()
    args.func(args)

        


