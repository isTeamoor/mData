import pandas as pd
from .impo import reservations, contactID




reservations = reservations.loc[  reservations['Cancelled By Contact ID'].isna()  ].copy()



reservations['Completed Date Time'] = pd.to_datetime(reservations['Completed Date Time'], format="%d/%m/%Y %H:%M:%S %p")
reservations['reservYear']  = reservations['Completed Date Time'].dt.year
reservations['reservMonth'] = reservations['Completed Date Time'].dt.month



reservations = reservations.merge(contactID[['Contact ID', 'Reserved By']], how = 'left', left_on = 'Created By Contact ID', right_on = 'Contact ID')


reservations = reservations[['Work Order Spare ID', 'Reservation Number', 'reservYear','reservMonth', 'Reserved By',]]