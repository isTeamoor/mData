import pandas as pd
from . import impo



reservations = impo.reservations.copy()
contactID    = impo.contactID[['Contact ID', 'Reserved By']]



reservations = reservations.loc[  ~(reservations['Cancelled By Contact ID']>200)  ] 



reservations['Completed Date Time'] = pd.to_datetime(reservations['Completed Date Time'], format="%d/%m/%Y %H:%M:%S %p")
reservations['reservYear']  = reservations['Completed Date Time'].dt.year
reservations['reservMonth'] = reservations['Completed Date Time'].dt.month


reservations = reservations.merge(contactID, how = 'left', left_on = 'Created By Contact ID', right_on = 'Contact ID')


reservations = reservations[['reservYear','reservMonth', 'Reservation Number','Work Order Spare ID', 'Reserved By',]]