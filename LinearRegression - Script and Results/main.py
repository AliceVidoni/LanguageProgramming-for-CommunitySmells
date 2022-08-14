import numpy as np
from sklearn.linear_model import LinearRegression
import csv
import statsmodels.api as sm

#PER LA REGRESSIONE MULTIPLA - L'ARRAY X ORA AVRA' DUE O PIU' COLONNE

#eseguirlo per ogni community smell (uno per volta)
community_smells=["OSE", "BCE", "PDE", "SV", "OS", "SD", "RS", "TFS", "UI", "TC"]
for cs in community_smells:
    #importare il CSV
    with open("Dataset_Input/"+cs) as file_name:
        file_read=csv.reader(file_name, delimiter=",")
        array=list(file_read)

    #input - Variabili indipendenti- reshape perchè la matrice deve essere bidimensionale ->tutto il resto
    x=[]
    for el in array:
        temp=[]
        for val in el:
            temp.append(float(val))
        temp.pop(0)
        x.append(temp)

    #output - Variabili dipendenti -> communitySmell
    y=[]
    for el in array:
        y.append(int(el[0]))

    x,y=np.array(x), np.array(y)

    #modello di regressione
    #.fit() calcola i valori ottimali dei pesi b0 e b1
    model=LinearRegression().fit(x,y)

    #determino su quale file scrivere
    file_Result=open("Result/"+cs+"_Result.txt", "a")

    #coefficiente di determinazione R^2
    r_sq=model.score(x,y)
    file_Result.write(f"coefficient of determination (R^2): {r_sq}\n\n")

    #_ alla fine della variabile indica che l'attributo è stimato (valori stimati)
    #coefficiente b0 (scalare)
    file_Result.write(f"intercept (b0): {model.intercept_}\n\n")

    #coefficiente b1 (array)
    file_Result.write(f"slope (b1): {model.coef_}\n\n")

    #previsioni con dati esistenti o nuovi
    y_pred=model.intercept_ + np.sum(model.coef_ * x, axis=1)
    file_Result.write(f"predicted response:\n{y_pred}\n\n")

    #REGRESSIONE LINEARE AVANZATA

    #è necessario agiungere la colonna di uno degli input se si desidera che statsmodels calcoli b0
    x=sm.add_constant(x)

    #modello di regressione basato sui minimi quadrati
    model=sm.OLS(y, x)
    result=model.fit()
    file_Result.write(f"\n{result.summary()}\n\n")
