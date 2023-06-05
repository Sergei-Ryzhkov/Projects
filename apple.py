#---------------------------------------------------------------------------------------#
#                                   Preliminaries                                       #
#---------------------------------------------------------------------------------------#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pl = pd.read_excel(r"C:\Users\aser\OneDrive\Рабочий стол\DATASETS\Apple.xlsx", sheet_name='P&L', parse_dates=[0])
bl = pd.read_excel(r"C:\Users\aser\OneDrive\Рабочий стол\DATASETS\Apple.xlsx", sheet_name='Balance', parse_dates=[0])
cfs = pd.read_excel(r"C:\Users\aser\OneDrive\Рабочий стол\DATASETS\Apple.xlsx", sheet_name='Cash Flow', parse_dates=[0])
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#---------------------------------------------------------------------------------------#
#                                   Data Cleaning                                       #
#---------------------------------------------------------------------------------------#

pl.columns = pl.columns.str.lower()
bl['date'] = pd.to_datetime(bl['date'], format = "%Y.%d.%m")

pl['date'] = pl['date'].dt.year
bl['date'] = bl['date'].dt.year
cfs['date'] = cfs['date'].dt.year

cfs.columns
cfs = cfs.rename(columns={"operating cash flow": "ocf", " net equity repurchased": "nqr"})
cfs['dividends'] = np.where(cfs['dividends'] == 'None', 0, cfs['dividends'])

#---------------------------------------------------------------------------------------#
#                                      Analysis                                         #
#---------------------------------------------------------------------------------------#

pl['revenue_growth'] = '0' #We need empty column for the next command to work 
for i, n in enumerate(pl['revenue']):
    if i < (len(pl['revenue'])-1):
        pl['revenue_growth'][i] = (pl['revenue'][i]/ pl['revenue'][i+1]-1)*100
    else:
        pl['revenue_growth'][i] = '0'
pl['revenue_growth'] = round(pl['revenue_growth'].astype('float64'), 2)

CAGR = (pl['revenue'][0] / pl['revenue'].iloc[-1]) ** (1/(len(pl['revenue']) -1)) - 1

pl['gross_margin'] = round(pl['gross profit'] / pl['revenue'] * 100, 2)
pl['operating_margin'] = round(pl['operating income'] / pl['revenue'] * 100, 2)
pl['net_margin'] = round(pl['net income'] / pl['revenue'] * 100, 2)

net_debt = bl['long-term debt'] - bl['cash on hand']
nd_op_in = net_debt / pl['operating income']

cfs['fcf'] = cfs['ocf'] - cfs['capex']
cfs['payout_ratio'] = (cfs['dividends'] + cfs['nqr']) / cfs['fcf'] * 100
cfs[cfs['date'] >= 2013]['payout_ratio'].mean() #For the past 10 years, Apple has payed 100% of its FCF

#---------------------------------------------------------------------------------------#
#                                  Visualisation                                        #
#---------------------------------------------------------------------------------------#

revenue_graph, axs = plt.subplots(1,2, figsize = (12,4.5), sharex=True)
axs[0].bar(pl['date'], pl['revenue']/1000, color ='#0088cc')
axs[0].set_title('Revenue bln $', fontsize=18)
axs[1].plot(pl['date'], pl['revenue_growth'], color ='#0088cc', marker='o')
axs[1].set_title('Revenue Growth %', fontsize=18)
axs[1].grid(True)

margins, axm = plt.subplots(figsize = (9,6))
axm.plot(pl['date'], pl['gross_margin'], color ='#FF6969', label='Gross', marker='o')
axm.plot(pl['date'], pl['operating_margin'], color ='#FFD3B0', label='Operating', marker='d')
axm.plot(pl['date'], pl['net_margin'], color ='#A6D0DD', label='Net', marker='v')
axm.legend(loc = 'lower center', bbox_to_anchor=(0.5, -0.15), ncol=3)
axm.grid(True)
axm.set_title("Apple's Margins %", fontsize=18)

pl['r&d%'] = pl['r&d'] / (pl['r&d'] + pl['sg&a']) * 100
pl['sg&a%'] = pl['sg&a'] / (pl['r&d'] + pl['sg&a']) * 100


costs, axd = plt.subplot_mosaic([['upleft', 'right'], ['lowleft', 'right']], figsize=(10,6))
axd['upleft'].bar(pl['date'], pl['r&d']/1000, color ='#0088cc')
axd['upleft'].set_title('R&D', fontsize=16)
axd['lowleft'].bar(pl['date'], pl['sg&a']/1000, color ='#FF6969')
axd['lowleft'].set_title('SG&A', fontsize=16)
plt.subplots_adjust(wspace=0.2, hspace=0.3)
axd['right'].plot(pl['date'], pl['r&d%'], label='R&D', color ='#0088cc')
axd['right'].plot(pl['date'], pl['sg&a%'], label='SG&A', color ='#FF6969')
axd['right'].grid(True)
axd['right'].legend()
axd['right'].set_title('Cost structure in 2022, %', fontsize=16)

debt, axf = plt.subplots(2, 1, figsize=(10,6))
axf[0].bar(bl['date'], net_debt/1000, width=0.35, label='Net Debt')
axf[0].axhline(y=0, color='k', linestyle='-')
axf[0].bar(pl['date'] + 0.35, pl['operating income']/1000, width=0.35, label='Operatin Income')
axf[0].set_title('Debt vs Operating Income, bln$', fontsize=16)
axf[0].set_ylabel('bln $', labelpad=-5)
axf[0].legend()
axf[1].plot(pl['date'], nd_op_in, color = '#A6D0DD', marker='o')
axf[1].grid(True)
axf[1].set_title('Net Debt to Operating Income Ratio', fontsize=16)
axf[1].axhline(y=0, color='r', linestyle='--')
plt.subplots_adjust(hspace=0.35)

cfs['div + rep'] = cfs['dividends'] + cfs['nqr']

cash_fl, afs = plt.subplots(figsize=(11,6))
afs.bar(cfs['date'], cfs['fcf']/1000, width=0.35, label='FCF', color = '#1B9C85')
afs.bar(cfs['date'] + 0.4, cfs['dividends']/1000, width = 0.35, label = 'Dividends', color = '#FFE194')
afs.bar(cfs['date'] + 0.4, cfs['nqr']/1000, width = 0.35, bottom = cfs['dividends']/1000 ,label = 'Repurchased', color = '#4C4C6D')
