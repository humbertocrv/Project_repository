def classes_abc(dataset,categories_set):

    import numpy as np
    import pandas as pd


    data = dataset
    categ = categories_set

    #Extraer categorias de interes y unir
    categ = categ[['Material','NOMBRE CAT','SUBCATEGORIA','NOMBRE SUB']]
    data_merged = pd.merge(data,categ,how='inner',on='Material')

    #Reorder columns
    cols = data_merged.columns.tolist()
    cols.insert(10,cols.pop(cols.index('NOMBRE CAT')))
    cols.insert(10,cols.pop(cols.index('SUBCATEGORIA')))
    cols.insert(10,cols.pop(cols.index('NOMBRE SUB')))
    data_merged = data_merged.reindex(columns=cols) 

    #ABC_class
    pmat=data_merged[['Material']]
    pmat=pmat['Material'].value_counts().rename_axis('Material').reset_index(name='freq').sort_values(by='freq',ascending=False)
    pmat['freq_rel']=(pmat['freq']/(pmat['freq'].sum()))*100

    #Create new columns
    pmat['freq_abs'],pmat['Cat_ABC']=np.nan,np.nan

    #Estimate absolute_frequence
    for i in range(len(pmat)):
        if i == 0:
            pmat.loc[i,'freq_abs']=pmat.loc[i,'freq_rel']
        else:
            pmat.loc[i,'freq_abs']=pmat.loc[i,'freq_rel']+pmat.loc[i-1,'freq_abs']

    #Assign categories
    condi_class=[(pmat['freq_abs'] <= 10),
                  (pmat['freq_abs'] > 10 ) & (pmat['freq_abs'] <= 30),
                  (pmat['freq_abs'] > 30)]
    class_class=['A','B','C']
    pmat['Cat_ABC']=np.select(condi_class,class_class)

    #Join dataframe and assign ABC
    pmat=pmat[['Material','Cat_ABC']]
    data_merged=pd.merge(data_merged,pmat,how='inner',on='Material')
    
    #Create logistic columns
    data_merged['Categoria Logistica'],data_merged['Rent Rotacion']=np.nan,np.nan

    return data_merged