import datetime as dt
import pandas as pd


def fols_at_followtime(user_id):
    current_friend_count = 53

    activity_fp = open('../data/hiriactivity.log')
    act_dat = []
    format_day = '%Y-%d-%m'
    format_time = '%H-%M-%S'

    for line in activity_fp:
	    day, time, action, usr_id = line.strip().split(' ')
	    act_dat.append({'day':day, 'time':time, 'action':action, 'usr_id':usr_id})

    act_dat = pd.DataFrame(act_dat, columns = ['day', 'time', 'action', 'usr_id'])

    rev = range(len(act_dat))
    rev.reverse()

    no_fols = []

    for idx in rev:
	    if act_dat['action'][idx] == 'unfol':
	    	current_friend_count += 1
	    elif act_dat['action'][idx] == 'fol':
		    current_friend_count -= 1
	    no_fols.append(current_friend_count)

    no_fols.reverse()
    act_dat['no_fols'] = no_fols
    return act_dat[act_dat['usr_id']==user_id]



