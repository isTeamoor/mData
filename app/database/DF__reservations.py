import pandas as pd
from .impo import reservations, contactID


reservations = reservations.loc[  reservations['Cancelled By Contact ID'].isna()  ].copy()


reservations['Completed Date Time'] = pd.to_datetime(reservations['Completed Date Time'], format="%d/%m/%Y %H:%M:%S %p")
reservations['reservYear']  = reservations['Completed Date Time'].dt.year
reservations['reservMonth'] = reservations['Completed Date Time'].dt.month



reservations = reservations.merge(contactID[['Contact ID', 'Reserved By']], how = 'left', left_on = 'Created By Contact ID', right_on = 'Contact ID')

rmpd_planners = ['Ulugbek  Xamroyev Maksudovich',
                 "Ulug'bek Xamroyev",
                 'Ulugbek Khamroev',
                 "Mansur Xasanov Tulqin o'g'li",
                 "Sarvar Rahmonov Ruslan o'g'li",
                 'Abusoleh Asrorxonov Qutbiddinovich',
                 "Mirsaid Xaydorov Baxtiyor o'g'li",
                 'Shokhijaxon Tilavov',
                 'Avazbek Boyqobilov Nazaraliyevich',
                 'Mansur Buriyev Jurayevich',
                 'Farruxjon Mamurov',
                 "To'lqin Berdiyev Omonovich",
                 'Mirjakhon Toirov',
                 'Mirjahon Toirov Ilxom o`g`li', 
                 'G`anisher G`afforov Maxmadustovich',
                 'Shohijahon Tilavov Abduxalil o`g`li',
                 'Shomirzo Juraqulov Shahobiddin o`g`li'
                 ]
reservations['isRMPD_planner'] = reservations['Reserved By'].copy().map(lambda x: 'yes' if x in rmpd_planners else 'no')



reservations = reservations[['Work Order Spare ID', 'Reservation Number', 'reservYear','reservMonth', 'Reserved By','isRMPD_planner']]