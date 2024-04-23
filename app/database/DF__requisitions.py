import pandas as pd
from .impo import requisitions, requisitionItems, contactID, approvalPath, uom



requisitions = requisitions.merge(contactID[['Contact ID','Requisitioned By']], how='left', left_on='Requisitioned By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitions = requisitions.merge(contactID[['Contact ID','Created By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))
requisitions = requisitions.merge(approvalPath, how='left', on='Approval Path ID')

requisitionItems = requisitionItems.merge(uom, how='left', on='UOMID')
requisitionItems = requisitionItems.merge(contactID[['Contact ID','Requisition line By']], how='left', left_on='Created By Contact ID', right_on='Contact ID', suffixes=('to_delete','to_delete'))

requisitions = requisitionItems.merge(requisitions, how='outer', on='Requisition ID')
requisitions['Total Expected Price'] = requisitions['Requisitioned Quantity'] * requisitions['Expected Purchase Price']




requisitions = requisitions.loc [ requisitions['Cancelled Date Time'].isna() ]
requisitions.fillna({'Approval Path Name':'undefined'}, inplace=True)





requisitions['Raised Date Time'] = pd.to_datetime(requisitions['Raised Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['raisedYear']  = requisitions['Raised Date Time'].dt.year
requisitions['raisedMonth'] = requisitions['Raised Date Time'].dt.month

requisitions['Required By Date Time'] = pd.to_datetime(requisitions['Required By Date Time'], format="%d/%m/%Y %H:%M:%S %p")
requisitions['requiredYear']  = requisitions['Required By Date Time'].dt.year
requisitions['requiredMonth'] = requisitions['Required By Date Time'].dt.month


### Фильтр по годам
#requisitions = requisitions.loc [ requisitions['raisedYear']==2023]
#requisitions = requisitions.loc [ requisitions['requiredYear']==2023]
#######################################################################




maintenance_ApprovalPath = ['SLU Default','PWU Default','Maintenance','Other Departments','CofE department','Routine Maintenance Department',
    'CofE','Civil Department','Material Control Department','Turnaround','Contract Services Deparment','Civil','CofE (Insul/Scaff)']
maintenance_Users = ['Abbos Meyliyev Ziyatovich','Abusoleh Asrorxonov Qutbiddinovich',"Alisher Xaydarov Keldiyor o'g'li","Asomiddin Soibov Abdilaziz o'g'li",
    "Atobek Karimov Axmad o'g'li",'Avazbek Boyqobilov Nazaraliyevich','Azizbek Berdiev','Azizjon Soibov','Bobur Aralov','Davron Khidirov',
    'Dilmurat Kulnazarov Jumayevich','Doston Normuminov','Farkhod Kholmatov','Ganisher Umrzaqov ','Ilyos Sadullayev','Islom Abdizoirov Abduraxmonovich',
    "Jahongir Xudoyorov Zokir o'g'li","Jasur Erkinov To'lqinjon o'g'li",'Javlon Yarashev','Jurabek Berdialiev ','Kamoljon Ismoilov','Khurshid Bobomurodov',
    "Komil Aliqulov Ahmad o'g'li","Mansur Xasanov Tulqin o'g'li","Maruf Toshpulatov O'rin og'li",'Mirjakhon Toirov','Mirjalol Kudirov',
    'Mirjalol Kudirov Urozovich',"Nurbek Xoliqulov Bahodir o'g'li","O'ktam Ilhomov Omon o'g'li","O'ktam Omonov",'Orif Bekmirzayev',
    "Sarvar Rahmonov Ruslan o'g'li","Shaxriyor Nuriddinov Navruz ug'li",'Sheroz Yusupov','Shohboz Xushnazarov',"Shohzod Yuldoshev Shuhrat o'g'li",
    'Ulugbek  Xamroyev Maksudovich',"Umar Dusnazarov Doniyor o'g'li",'Xasan Eshmatov',"Zufar Chorshanbiyev Muzafar o'g'li",]
requisitions = requisitions.loc [ (requisitions['Approval Path Name'].isin(maintenance_ApprovalPath)) | (requisitions['Created By'].isin(maintenance_Users))]



requisitions['mergeNumber'] = ''
for RequisitionNumber, group in requisitions.groupby('Requisition Number'):
    counter = 0
    for i, row in group.iterrows():
        requisitions.loc[ i, 'mergeNumber'] = str(RequisitionNumber) + "-" + str(counter)
        counter += 1


requisitions = requisitions[['Requisition Line Description','Requisition Description','Approval Path Name','Created By',
 'Requisitioned Quantity', 'UOMDescription', 'Expected Purchase Price','Total Expected Price',
 'Requisition Number','mergeNumber', 'requiredYear', 'requiredMonth', 'raisedYear', 'raisedMonth', 'Completed Date Time',]]