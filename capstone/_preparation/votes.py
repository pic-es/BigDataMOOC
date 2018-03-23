#!/usr/bin/env python
import sys
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, bernoulli


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
    
    if row['p_el_bis'] >= 0.8:
        if new_p_el < 0.8:
            votes_el = np.ceil(new_nvotes*0.8)
            votes_cs = new_nvotes - votes_el
            
    elif row['p_cs_bis'] >= 0.8:
        if new_p_cs < 0.8:
            votes_cs = np.ceil(new_nvotes*0.8)
            votes_el = new_nvotes - votes_cs
    else:

        while new_p_cs >= 0.8:
            votes_cs -=1
            votes_el +=1
            new_p_cs = float(votes_cs) / float(new_nvotes)

        while new_p_el >= 0.8:
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
            print 'cleaned bad users at {} iteration'.format(n_iter + 1)
            break

        # correct bad users
        for user_id in bad_users:
            correct_bad_user(votes_df, user_id, n_users)
        
        n_iter += 1

    if n_iter >= max_niter:
        print 'failed to clean bad users!!\n {}'.format(get_bad_users(votes_df))

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


def define_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', '-a', required=True,
                        help='Action to perform')
    parser.add_argument('--or_csv_file', '-o', required=False)
    parser.add_argument('--dest_csv_file', '-d', required=False)
    return parser

def check_mandatory_arg(args, argument_list):
    for arg in argument_list:
        if not getattr(args, arg):
            raise Exception('{} needed for action {}'.format(arg, args.action))

def check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs):
    if new_n_el != old_n_el:
        raise Exception('Number of elliptics galaxies does not match new = {}, old = {}'.format(new_n_el, old_n_el)) 
    if new_n_cs != old_n_cs:
        raise Exception('Number of spiral galaxies does not match new = {}, old = {}'.format(new_n_cs, old_n_cs)) 



if __name__ == '__main__':

    parser = define_arguments()
    args = parser.parse_args()

    if args.action == 'generate_votes':

        check_mandatory_arg(args, ['or_csv_file', 'dest_csv_file'])
        
        TARGET_CUT_PERC = 80.
        MAX_GOOD_VAR = 0.35
        VOTES_PER_USER_RANGE = [5., 30.]
        BAD_USERS_RATIO = [0.001, 0.005]

        np.random.seed(0)

        input_csv = args.or_csv_file
        or_df = pd.read_csv(input_csv)
        old_n_el = (or_df['p_el_debiased'] >= TARGET_CUT_PERC/100.).sum()
        old_n_cs = (or_df['p_cs_debiased'] >= TARGET_CUT_PERC/100).sum()
        print 'original number of elliptics={} spirals={}'.format(old_n_el, old_n_cs)

        # Modify p_el an p_cs to make the add up to 1
        # check that the percentages for each galaxy type are not changed
        compute_n_votes(or_df)
        new_n_el = (or_df['p_el_bis'] >= TARGET_CUT_PERC/100.).sum()
        new_n_cs = (or_df['p_cs_bis'] >= TARGET_CUT_PERC/100.).sum()
        check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)

        # Compute the number of votes to keep the number of galaxies of each type
        or_df['n_votes_el'] = or_df.apply(fill_votes_el, axis=1)
        or_df['n_votes_cs'] = or_df.apply(fill_votes_cs, axis=1)
        new_n_el = (or_df['n_votes_el']/(or_df['n_votes_el'] + or_df['n_votes_cs']) >= TARGET_CUT_PERC/100.).sum()
        new_n_cs = (or_df['n_votes_cs']/(or_df['n_votes_el'] + or_df['n_votes_cs']) >= TARGET_CUT_PERC/100.).sum()
        check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)

        # generate votes DataFrame
        n_votes = (or_df['n_votes_el'] + or_df['n_votes_cs']).sum()
        min_users = int(n_votes/VOTES_PER_USER_RANGE[1])
        max_users = int(n_votes/VOTES_PER_USER_RANGE[0])
        n_users = np.random.randint(min_users, max_users)
        print 'initial number of users = {}'.format(n_users)
        votes_df = build_votes(or_df, n_users)
        votes_df = correct_user_votes(votes_df, n_users, 20, MAX_GOOD_VAR)
        print 'final number of good users = {}'.format(len(votes_df['user_id'].unique()))
        max_good_user_id = votes_df['user_id'].max()
        
        # Check that the number of galaxies of each type is coherent
        votes_p_df = pd.DataFrame(votes_df.groupby('dr7objid')['vote'].mean())
        new_n_el = (votes_p_df['vote'] <= (100. - TARGET_CUT_PERC)/100.).sum()
        new_n_cs = (votes_p_df['vote'] >= TARGET_CUT_PERC/100.).sum()
        check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)
        
        # Add some bad users to be filtered out
        n_bad_users = np.random.randint(int(BAD_USERS_RATIO[0]*n_users), int(BAD_USERS_RATIO[1]*n_users))
        votes_df = add_bad_users(votes_df, n_bad_users, MAX_GOOD_VAR)
        print 'inserted {} bad users'.format(n_bad_users)

        # pop bad users with variance lower than limit and shuffle user ids
        user_vars_df = compute_user_variances(votes_df)
        bad_to_pop = user_vars_df[(user_vars_df.index > max_good_user_id) & (user_vars_df['diff_votes_2'] <= MAX_GOOD_VAR)]
        print 'found {} bad users with low variances. Going to remove them'.format(len(bad_to_pop))
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
        new_n_el = (votes_p_df['vote'] <= (100. - TARGET_CUT_PERC)/100.).sum()
        new_n_cs = (votes_p_df['vote'] >= TARGET_CUT_PERC/100.).sum()
        check_type_numbers(old_n_el, new_n_el, old_n_cs, new_n_cs)  

        # Dump votes_df to file
        votes_df.to_csv(args.dest_csv_file, index=False)

