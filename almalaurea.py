#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:18:20 2023

@author: riccardo
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':15})
import requests
import re
import pandas as pd
from tqdm import tqdm

def almalaurea(ID,A,G):
    url = "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=tutti&corstipo=tutti&ateneo="+ID+"&facolta=tutti&gruppo="+G+"&livello=tutti&area4="+A+"&pa="+ID+"&classe=tutti&postcorso=tutti&isstella=0&presiui=tutti&disaggregazione=&LANG=it&CONFIG=profilo"
    text = requests.get(url).text
    
    string = r"Ateneo: (.*)"
    ateneo = re.findall(string,text)
    
    string = r"Facoltà/Dipartimento/Scuola: (.*)"
    facolta = re.findall(string,text)
    
    string = r"area disciplinare: (.*)"
    area = re.findall(string,text)
    
    string = r"gruppo disciplinare: (.*)"
    gruppo = re.findall(string,text)

    string = r"<b>anno di laurea......(.*?)'"
    anni = re.findall(string,text)
    anni = list(dict.fromkeys(anni))
    
    if len(ateneo)==0:
        d0 = np.empty(19)
        d0[:] = np.nan
        d1 = d0
        d2 = d0
        d3 = d0
    
    else:
        ateneo = ateneo[0][:-1]
        facolta = facolta[0][:-1]
        area = area[0][:-1]
        gruppo = gruppo[0][:-1]
        # print(f"--Retrieved--\nAteneo: {ateneo}\nFacoltà: {facolta}\nArea: {area}\nGruppo: {gruppo}")
        
        #########################################
        ### Array col numero di laureati/anno ###
        #########################################
        string = r"Numero di laureati([\s\S]*)Hanno compilato il questionario"
        
        t = re.findall(string,text)
        
        string = r"<td class='datobold'>(.*)</td>"
        
        d0 = re.findall(string,t[0])
        
        for i in range(len(d0)):
            if d0[i]=='&nbsp;':
                d0[i] = np.nan
            else:
                d0[i] = d0[i].replace('.','')
        
        d0 = np.array(d0,float)
        
        ###############################################
        ### Array con la percentuale di maschi/anno ###
        ###############################################
        string = r"Uomini([\s\S]*?)Donne"
        
        t = re.findall(string,text)
        
        string = r"<td class='dato'>(.*)</td>"
        
        d1 = re.findall(string,t[0])
        
        for i in range(len(d1)):
            if d1[i]=='&nbsp;':
                d1[i] = np.nan
            else:
                d1[i] = d1[i].replace(',','.')
        
        d1 = np.array(d1,float)
        
        ################################################
        ### Array con la percentuale di femmine/anno ###
        ################################################
        string = r"Donne([\s\S]*?)Età alla laurea"
        
        t = re.findall(string,text)
        
        string = r"<td class='dato'>(.*)</td>"
        
        d2 = re.findall(string,t[0])
        
        for i in range(len(d2)):
            if d2[i]=='&nbsp;':
                d2[i] = np.nan
            else:
                d2[i] = d2[i].replace(',','.')
        
        d2 = np.array(d2,float)
        
        ###################################
        ### Array con il voto di laurea ###
        ###################################
        string = r"Voto di laurea([\s\S]*?)Regolarità negli studi"
        
        t = re.findall(string,text)
        
        string = r"<td class='datobold'>(.*)</td>"
        
        d3 = re.findall(string,t[0])
        
        for i in range(len(d3)):
            if d3[i]=='&nbsp;':
                d3[i] = np.nan
            else:
                d3[i] = d3[i].replace(',','.')
        
        d3 = np.array(d3,float)
    
    my_return = [d0,d1,d2,d3,anni,ateneo,facolta,area,gruppo]
    
    return my_return

area = {'tutti':'tutti','ALE':'1','EGS':'2','SAV':'3','STEM':'4'}

gruppo = {'tutti':'tutti',
          'Educazione e formazione':'1','Arte e design':'2','Letterario umanistico':'3',
          'Linguistico':'4','Politico-sociale e comunicazione':'5','Psicologico':'6',
          'Economico':'7','Giuridico':'8','Scientifico':'9',
          'Informatica e tecnologie ICT':'10','Architettura e Ing civile':'11',
          "Ing industriale e dell'informazione":'12',
          'Agrario-forestale e veterinario':'13','Medico-sanitario e farmaceutico':'14',
          'Scienze motorie e sportive':'15'}

gruppo_id = {v:k for k,v in gruppo.items()}

# x = 'tutti'
# y = 'tutti'

# fig, ax = plt.subplots(4,4,sharex=True,sharey=True,figsize=(24,20))

# fig.suptitle('Percentuale di laureati maschi e femmine per i vari gruppi disciplinari (e aree disciplinari al 2024 in ordinata, classificazione MUR 2020)',
#              y=0.92)
# fig.supxlabel('Anno',y=0.08)
# fig.supylabel('Percentuale sul totale [%]',x=0.07)

# area_ID = ['1','2','4','3']
# area_nome = ['ALE','EGS','STEM','SAV']

# for z in tqdm(range(1,16)):
#     z = str(z)
#     data = almalaurea(x,y,z)
    
#     M,F,anni = data[1],data[2],data[4]
#     # Convert anni to integers to avoid unwanted vertical lines in the plot
#     anni = [int(a) for a in anni]

#     z = int(z)-1
    
#     data[-1] = 'Gruppo '+data[-1]
    
#     if len(data[-1])>=35:
#         data[-1] = data[-1].replace(' e ',' e\n')
    
#     ax[z//4][z%4].set_title(f'{data[-1]}')
#     ax[z//4][z%4].plot(anni,M,color='royalblue',marker='o',lw=1.5,label='Maschi')
#     ax[z//4][z%4].plot(anni,F,color='deeppink',marker='o',lw=1.5,label='Femmine')
#     ax[z//4][z%4].plot([anni[0],anni[-1]],[50,50],c='black',ls='dashed',lw=1.5)
    
#     ax[z//4][z%4].grid()
    
#     if z%4==0:
#         data = almalaurea(x,y,'tutti')
#         M,F,anni = data[1],data[2],data[4]
#         anni = [int(a) for a in anni]
#         ax[z//4][z%4].set_ylabel(f"{area_nome[z//4]} - M: {round(M[-1],1)}% - F: {round(F[-1],1)}%")
    
# z+=1
# data = almalaurea(x,y,'tutti')
# M,F = data[1],data[2]

# ax[z//4][z%4].set_title(f'Totale - M: {round(M[-1],1)}% - F: {round(F[-1],1)}%')
# ax[z//4][z%4].plot(anni,M,color='royalblue',marker='o',lw=2,label='Maschi')
# ax[z//4][z%4].plot(anni,F,color='deeppink',marker='o',lw=2,label='Femmine')
# ax[z//4][z%4].plot([anni[0],anni[-1]],[50,50],c='black',ls='dashed',lw=1.5)

# ax[z//4][z%4].annotate('Source: AlmaLaurea''\n\n''Elaboration by''\n''Biasissi Riccardo', 
#                         xy=(0.03,0.03), xytext=(0.03,0.03), xycoords='axes fraction',
#                         va='bottom', fontsize=15)

# ax[z//4][z%4].legend()
# ax[z//4][z%4].grid()

# plt.subplots_adjust(wspace=0.08, hspace=0.24)

# plt.savefig('M_VS_F.png', dpi=200, bbox_inches='tight')

# plt.close()




































def almalaurea_occupazione(ID,Y,A,G,C,YRL):
    if C=="tutti":
        url = "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno="+Y+"&corstipo=tutti&ateneo="+ID+"&facolta=tutti&gruppo="+G+"&livello=tutti&area4="+A+"&pa="+ID+"&classe="+C+"&postcorso=tutti&isstella=0&annolau="+YRL+"&condocc=tutti&iscrls=tutti&disaggregazione=&LANG=it&CONFIG=occupazione"
    else:
        url = "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno="+Y+"&corstipo=LS&ateneo="+ID+"&facolta=tutti&gruppo="+G+"&livello=tutti&area4="+A+"&pa="+ID+"&classe="+C+"&postcorso=tutti&isstella=0&annolau="+YRL+"&condocc=tutti&iscrls=tutti&disaggregazione=&LANG=it&CONFIG=occupazione"
    text = requests.get(url).text
    
    f = open('test.txt','w')
    f.write(text)
    f.close()
    
    string = r"Ateneo: (.*)"
    ateneo = re.findall(string,text)
    
    string = r"Facoltà/Dipartimento/Scuola: (.*)"
    facolta = re.findall(string,text)
    
    string = r"area disciplinare: (.*)"
    area = re.findall(string,text)
    
    string = r"gruppo disciplinare: (.*)"
    gruppo = re.findall(string,text)
    
    d0,d1,d2,d3,d4,d5,d6,d7 = [],[],[],[],[],[],[],[]
    
    if len(ateneo)==0:
        d0.append(np.nan)
        d1.append(np.nan)
        d2.append(np.nan)
        d3.append(np.nan)
        d4.append(np.nan)
        d5.append(np.nan)
        d6.append(np.nan)
        d7.append(np.nan)
    
    else:
        ateneo = ateneo[0][:-1]
        facolta = facolta[0][:-1]
        area = area[0][:-1]
        gruppo = gruppo[0][:-1]
        # print(f"--Retrieved--\nAteneo: {ateneo}\nFacoltà: {facolta}\nArea: {area}\nGruppo: {gruppo}")
        
        ###############################
        ### Numero di laureati/anno ###
        ###############################
        string = r"Numero di laureati([\s\S]*?)Numero di intervistati"
        # print(string)
        
        t = re.findall(string,text)
        
        string = r"<td class='datobold'>(.*)</td>"
        # print(string)
        
        d0_temp = re.findall(string,t[0])
        
        for i in range(len(d0_temp)):
            if d0_temp[i]=='&nbsp;':
                d0_temp[i] = np.nan
            else:
                d0_temp[i] = d0_temp[i].replace('.','')
        
        d0_temp = np.array(d0_temp,float)
        d0.append(d0_temp[0])
        
        ##################################
        ### Percentuale di maschi/anno ###
        ##################################
        string = r"Genere([\s\S]*?)Età alla laurea"
        
        t = re.findall(string,text)
        
        string = r"Uomini([\s\S]*?)Donne"
        
        t = re.findall(string,t[0])
        
        string = r"<td class='dato'>(.*)</td>"
        
        d1_temp = re.findall(string,t[0])
        
        for i in range(len(d1_temp)):
            if d1_temp[i]=='&nbsp;':
                d1_temp[i] = np.nan
            else:
                d1_temp[i] = d1_temp[i].replace(',','.')
        
        d1_temp = float(d1_temp[0])
        d1.append(d1_temp)
        
        ###################################
        ### Percentuale di femmine/anno ###
        ###################################
        string = r"Genere([\s\S]*?)Età alla laurea"
        
        t = re.findall(string,text)
        
        string = r"Donne([\s\S]*?)Età alla laurea"
        
        t = re.findall(string,text)
        
        string = r"<td class='dato'>(.*)</td>"
        
        d2_temp = re.findall(string,t[0])
        
        for i in range(len(d2_temp)):
            if d2_temp[i]=='&nbsp;':
                d2_temp[i] = np.nan
            else:
                d2_temp[i] = d2_temp[i].replace(',','.')
        
        d2_temp = float(d2_temp[0])
        d2.append(d2_temp)
        
        if int(Y)<2020:
            ###################################
            ### Tasso di occupazione totale ###
            ###################################
            string = r"Tasso di occupazione([\s\S]*?)Tasso di disoccupazione"
            
            t = re.findall(string,text)
            
            string = r"<td class='datobold'>(.*)</td>"
            
            d3_temp = re.findall(string,t[0])
            
            for i in range(len(d3_temp)):
                if d3_temp[i]=='&nbsp;':
                    d3_temp[i] = np.nan
                else:
                    d3_temp[i] = d3_temp[i].replace(',','.')
            
            d3_temp = float(d3_temp[0])
            d3.append(d3_temp)
            
            ######################################
            ### Tasso di disoccupazione totale ###
            ######################################
            string = r"Tasso di disoccupazione([\s\S]*?)Ingresso nel mercato"
            
            t = re.findall(string,text)
            
            string = r"<td class='datobold'>(.*)</td>"
            
            d4_temp = re.findall(string,t[0])
            
            for i in range(len(d4_temp)):
                if d4_temp[i]=='&nbsp;':
                    d4_temp[i] = np.nan
                if d4_temp[i]=='-':
                    d4_temp[i] = 0
                else:
                    d4_temp[i] = d4_temp[i].replace(',','.')
            
            d4_temp = float(d4_temp[0])
            d4.append(d4_temp)
        
        else:
            ###################################
            ### Tasso di occupazione totale ###
            ###################################
            string = r"Totale([\s\S]*?)Tasso di disoccupazione"
            
            t = re.findall(string,text)
            
            string = r"<td class='datobold'>(.*)</td>"
            
            d3_temp = re.findall(string,t[0])
            
            for i in range(len(d3_temp)):
                if d3_temp[i]=='&nbsp;':
                    d3_temp[i] = np.nan
                else:
                    d3_temp[i] = d3_temp[i].replace(',','.')
            
            d3_temp = float(d3_temp[0])
            d3.append(d3_temp)
            
            ######################################
            ### Tasso di disoccupazione totale ###
            ######################################
            string = r"Tasso di disoccupazione([\s\S]*?)Ingresso nel mercato"
            
            t = re.findall(string,text)
            
            string = r"<td class='datobold'>(.*)</td>"
            
            d4_temp = re.findall(string,t[0])
            
            for i in range(len(d4_temp)):
                if d4_temp[i]=='&nbsp;':
                    d4_temp[i] = np.nan
                if d4_temp[i]=='-':
                    d4_temp[i] = 0
                else:
                    d4_temp[i] = d4_temp[i].replace(',','.')
            
            d4_temp = float(d4_temp[0])
            d4.append(d4_temp)
        
        ##############################
        ### Retribuzione mensile   ###
        ### d5 maschi e d6 femmine ###
        ##############################
        string = r"Retribuzione mensile([\s\S]*?)Utilizzo"
        
        t = re.findall(string,text)
        if len(t)!=1:
            t[0] = t[-1]
        string = r"<td class='dato'>(.*)</td>"
        
        d5_temp = re.findall(string,t[0])

        for i in range(len(d5_temp)):
            if d5_temp[i]=='&nbsp;':
                d5_temp[i] = np.nan
            else:
                d5_temp[i] = d5_temp[i].replace('.','')
        
        d5.append(float(d5_temp[0]))

        d6.append(float(d5_temp[1]))
        
        string = r"<td class='datobold'>(.*)</td>"
        
        d7_temp = re.findall(string,t[0])
        
        for i in range(len(d7_temp)):
            if d7_temp[i]=='&nbsp;':
                d7_temp[i] = np.nan
            else:
                d7_temp[i] = d7_temp[i].replace('.','')

        d7_temp = [float(x) for x in d7_temp if x is not np.nan and x != 'nan']

        d7.append(float(d7_temp[0]))


    my_return = [d0,d1,d2,d3,d4,d5,d6,d7,ateneo,facolta,area,gruppo]
    
    return my_return

###################################
### Estrattore dati da almlaurea.it
###################################

# ID = id ateneo
# A = area
# G = gruppo
# C = classe
# YRL = anni di distanza da conseguimento
# ID,A,G,C,YRL = 'tutti','tutti',["tutti"]+list(np.arange(0,15)+1),'tutti',[1,3,5]
# Y = np.arange(2008,2025)
# a = 1

# data = []

# total_iterations = len(G) * len(YRL) * len(Y)
# with tqdm(total=total_iterations) as pbar:
#     for g in G:
#         g = str(g)
#         for yrl in YRL:
#             yrl = str(yrl)
#             for y in Y:
#                 y = str(y)
#                 temp = almalaurea_occupazione(ID, y, A, g, C, yrl)
#                 data.append([y, yrl, a, g, ID, temp[0][0], temp[1][0], temp[2][0], temp[3][0], temp[4][0], temp[5][0], temp[6][0], temp[7][0]])
#                 pbar.update(1)

# columns = [
#     "anno",
#     "anni_da_conseguimento_titolo",
#     "area",
#     "gruppo",
#     "ateneo",
#     "numero_laureati",
#     "percentuale_maschi",
#     "percentuale_femmine",
#     "tasso_occupazione_totale",
#     "tasso_disoccupazione_totale",
#     "retribuzione_mensile_maschi",
#     "retribuzione_mensile_femmine",
#     "retribuzione_mensile"
# ]

# df = pd.DataFrame(data, columns=columns)
# print(df)

# df.to_csv('almalaurea.csv', index=False)



















######################################
### Grafico retribuzione mensile netta
######################################

df = pd.read_csv('almalaurea.csv')

# G = df['gruppo']
# YRL = ['1','3','5']

# for yrl in YRL:
#     fig, ax = plt.subplots(4,4,sharex=True,sharey=True,figsize=(24,20))

#     fig.suptitle(f'Retribuzione mensile netta (a {yrl} anni dal titolo) suddivisa per genere e gruppo disciplinare (classificazione MUR 2020)',
#                   y=0.93)
#     fig.supxlabel('Anno',y=0.08)
#     fig.supylabel('Retribuzione mensile netta [€]',x=0.08)

#     for g in G:
#         if g!='tutti':
#             title = f'Gruppo {gruppo_id[g]}'
#             ax[(int(g)-1)//4][(int(g)-1)%4].set_title(title.replace(' e ',' e\n'))

#             df_temp = df[(df['gruppo']==g) & (df['anni_da_conseguimento_titolo']==int(yrl))]
#             M,F,T = df_temp['retribuzione_mensile_maschi'],df_temp['retribuzione_mensile_femmine'],df_temp['retribuzione_mensile']

#             ax[(int(g)-1)//4][(int(g)-1)%4].plot(df_temp['anno'],M,color='royalblue',marker='o',lw=1.5,label='Maschi')
#             ax[(int(g)-1)//4][(int(g)-1)%4].plot(df_temp['anno'],F,color='deeppink',marker='o',lw=1.5,label='Femmine')
#             ax[(int(g)-1)//4][(int(g)-1)%4].plot(df_temp['anno'],T,color='black',marker='o',lw=1.5,label='Totale')

#             ax[(int(g)-1)//4][(int(g)-1)%4].grid()

#     g = 'tutti'
#     ax[-1][-1].set_title('Totale')

#     df_temp = df[(df['gruppo']==g) & (df['anni_da_conseguimento_titolo']==int(yrl))]
#     M,F,T = df_temp['retribuzione_mensile_maschi'],df_temp['retribuzione_mensile_femmine'],df_temp['retribuzione_mensile']

#     g = 16

#     ax[(g-1)//4][(g-1)%4].plot(df_temp['anno'],M,color='royalblue',marker='o',lw=2,label='Maschi')
#     ax[(g-1)//4][(g-1)%4].plot(df_temp['anno'],F,color='deeppink',marker='o',lw=2,label='Femmine')
#     ax[(g-1)//4][(g-1)%4].plot(df_temp['anno'],T,color='black',marker='o',lw=2,label='Totale')

#     ax[(int(g)-1)//4][(int(g)-1)%4].grid()
#     ax[(int(g)-1)//4][(int(g)-1)%4].legend()

#     ax[(int(g)-1)//4][(int(g)-1)%4].annotate('Source: AlmaLaurea''\n\n''Elaboration by''\n''Biasissi Riccardo', 
#                         xy=(0.97,0.03), xytext=(0.97,0.03), xycoords='axes fraction',
#                         va='bottom', ha='right',fontsize=15)

#     plt.subplots_adjust(wspace=0.08, hspace=0.24)

#     plt.savefig(f'retribuzione_gruppi_{yrl}.png', dpi=200, bbox_inches='tight')

#     plt.close()


# ###########################################################
# ### Grafico divario maschile-femminile retribuzione mensile
# ###########################################################

# fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(24, 20))

# fig.suptitle('Divario retributivo maschile-femminile (a 1, 3, 5 anni dal titolo) per gruppo disciplinare (classificazione MUR 2020)',
#              y=0.93)
# fig.supxlabel('Anno', y=0.08)
# fig.supylabel('Divario retributivo [%]', x=0.08)

# for idx, g in enumerate([str(i) for i in range(1, 16)] + ['tutti']):
#     row, col = idx // 4, idx % 4
#     if g != 'tutti':
#         title = f'Gruppo {gruppo_id[g]}'
#         ax[row][col].set_title(title.replace(' e ', ' e\n'))
#     else:
#         ax[row][col].set_title('Totale')

#     for yrl, color, label in zip(['1', '3', '5'], ['royalblue', 'deeppink', 'darkgreen'], ['1 anno', '3 anni', '5 anni']):
#         df_temp = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == int(yrl))]
#         if not df_temp.empty:
#             M = df_temp['retribuzione_mensile_maschi']
#             F = df_temp['retribuzione_mensile_femmine']
#             anni = df_temp['anno']
#             divario = 100 * (M - F) / M
#             ax[row][col].plot(anni, divario, marker='o', lw=2, color=color, label=label)

#     ax[row][col].grid()
#     if idx == 15:
#         ax[row][col].legend()
#         ax[row][col].annotate('Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
#                               xy=(0.03, 0.03), xytext=(0.03, 0.03), xycoords='axes fraction',
#                               va='bottom', fontsize=15)

# plt.subplots_adjust(wspace=0.08, hspace=0.24)

# plt.savefig('divario_retributivo.png', dpi=200, bbox_inches='tight')

# plt.close()

# ################################
# ### Grafico tasso disoccupazione
# ################################

# fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(24, 20))

# fig.suptitle('Tasso di disoccupazione totale (a 1, 3, 5 anni dal titolo) per gruppo disciplinare (classificazione MUR 2020)',
#              y=0.93)
# fig.supxlabel('Anno', y=0.09)
# fig.supylabel('Tasso di disoccupazione [%]', x=0.08)

# for idx, g in enumerate([str(i) for i in range(1, 16)] + ['tutti']):
#     row, col = idx // 4, idx % 4
#     if g != 'tutti':
#         title = f'Gruppo {gruppo_id[g]}'
#         ax[row][col].set_title(title.replace(' e ', ' e\n'))
#     else:
#         ax[row][col].set_title('Totale')

#     for yrl, color, label in zip(['1', '3', '5'], ['royalblue', 'deeppink', 'darkgreen'], ['1 anno', '3 anni', '5 anni']):
#         df_temp = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == int(yrl))]
#         if not df_temp.empty:
#             anni = df_temp['anno']
#             tasso = df_temp['tasso_disoccupazione_totale']
#             ax[row][col].plot(anni, tasso, marker='o', lw=2, color=color, label=label)

#     ax[row][col].set_ylim(0, 35)
#     ax[row][col].grid()
    
#     if idx == 11:
#         ax[row][col].annotate('Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
#                               xy=(0.03, 0.95), xytext=(0.03, 0.95), xycoords='axes fraction',
#                               va='top', ha='left', fontsize=15)
    
#     if idx == 15:
#         ax[row][col].legend()

# plt.subplots_adjust(wspace=0.06, hspace=0.24)
# plt.savefig('disoccupazione_gruppi.png', dpi=200, bbox_inches='tight')
# plt.close()

# ######################################
# ### Grafico numero laureati sul totale [%]
# ######################################

# Define area names for ylabel usage
area_nome = ['ALE','EGS','STEM','SAV']

fig, ax = plt.subplots(4, 4, sharex=True, figsize=(24, 20))

fig.suptitle('Frazione di laureati sul totale per gruppo disciplinare (e aree disciplinari al 2024 in ordinata, classificazione MUR 2020)',
             y=0.93)
fig.supxlabel('Anno', y=0.08)
fig.supylabel('Frazione di laureati [%]', x=0.07)

for idx, g in enumerate([str(i) for i in range(1, 16)] + ['tutti']):
    row, col = idx // 4, idx % 4
    if g != 'tutti':
        title = f'Gruppo {gruppo_id[g]}'
        ax[row][col].set_title(title.replace(' e ', ' e\n'))

        df_temp = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == 1)]
        anni = df_temp['anno']
        n_laureati = df_temp['numero_laureati']
        # Calcolo percentuale sul totale per quell'anno
        tot_anno = df[(df['anni_da_conseguimento_titolo'] == 1) & (df['gruppo'] == 'tutti')]['numero_laureati']
        print(df[(df['anni_da_conseguimento_titolo'] == 1) & (df['gruppo'] == 'tutti')]['numero_laureati'])
        percentuale = 100 * np.array(n_laureati) / np.array(tot_anno)
        ax[row][col].plot(anni, percentuale, marker='o', lw=2, color='black')

        ax[row][col].set_ylim(0, 16)
        if col != 0:
            ax[row][col].set_yticklabels([])
        ax[row][col].grid()

        if col%4==0:
            # Calcola la percentuale per area (somma dei gruppi associati)
            area_gruppi = {
                0: ['1', '2', '3', '4'],
                1: ['5', '6', '7', '8'],
                2: ['9', '10', '11', '12'],
                3: ['13', '14', '15']
            }
            gruppi_area = area_gruppi.get(row, [])
            tot_anno = df[(df['anno'] == 2024) & (df['anni_da_conseguimento_titolo'] == 1) & (df['gruppo'] == 'tutti')]['numero_laureati'].sum()
            n_laureati_area = df[(df['anno'] == 2024) & (df['gruppo'].isin(gruppi_area)) & (df['anni_da_conseguimento_titolo'] == 1)]['numero_laureati'].sum()
            percentuale_area = 100 * n_laureati_area / tot_anno
            ax[row][col].set_ylabel(f"{area_nome[row]} - {percentuale_area:.1f}%")
    else:
        ax[row][col].set_title('Totale assoluto annuale (in milioni)')

        df_temp = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == 1)]
        anni = df_temp['anno']
        n_laureati = df_temp['numero_laureati']/1e6
        ax[row][col].plot(anni, n_laureati, marker='o', lw=2, color='black')
        ax[row][col].grid()
        ax[row][col].yaxis.tick_right()

plt.subplots_adjust(wspace=0.06, hspace=0.24)
plt.savefig('numero_laureati_percentuale.png', dpi=200, bbox_inches='tight')
plt.close()