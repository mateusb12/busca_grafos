# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:51:51 2021

@author: hsume
"""

import graph as gp
import pandas as pd 
    
def graph_generetor(end):
    
    # Instancia o grago
    graph = gp.Graph()
    
    # Cria o grafo com base nas distacias por terra entre as cidades
    graph.connect('BoaVista', 'Manaus', 785)
    graph.connect('Manaus', 'RioBranco', 1445)
    graph.connect('Manaus', 'PortoVelho', 901)
    graph.connect('Manaus', 'Brasilia', 3490)
    graph.connect('Manaus', 'Belem', 5298)
    graph.connect('RioBranco', 'PortoVelho', 544)
    graph.connect('PortoVelho', 'Cuiaba', 1456)
    graph.connect('Belem', 'Macapa', 650) #Distancia tirada do site https://www.geografos.com.br/distancia-entre-cidades/distancia-entre-macapa-e-belem.php
    graph.connect('Brasilia', 'Palmas', 973)
    graph.connect('Brasilia', 'Goiania', 209)
    graph.connect('Brasilia', 'SaoPaulo', 1015)
    graph.connect('Brasilia', 'BeloHorizonte', 716)
    graph.connect('Brasilia', 'Fortaleza', 2200)
    graph.connect('Brasilia', 'Cuiaba', 1133)
    graph.connect('Fortaleza', 'SaoLuis', 1070)
    graph.connect('Fortaleza', 'Teresina', 634)
    graph.connect('Fortaleza', 'Natal', 537)
    graph.connect('Fortaleza', 'Recife', 800)
    graph.connect('Fortaleza', 'Salvador', 1389)
    graph.connect('Cuiaba', 'CampoGrande', 694)
    graph.connect('Cuiaba', 'SaoPaulo', 1614)
    graph.connect('CampoGrande', 'Curitiba', 991)
    graph.connect('Curitiba', 'Florianopolis', 300)
    graph.connect('Curitiba', 'SaoPaulo', 408)
    graph.connect('Florianopolis', 'PortoAlegre', 476)
    graph.connect('SaoPaulo', 'RioDeJaneiro', 429)
    graph.connect('RioDeJaneiro', 'Vitoria', 521)
    graph.connect('RioDeJaneiro', 'Salvador', 1649)
    graph.connect('Salvador', 'Aracaju', 356)
    graph.connect('Salvador', 'Natal', 1126)
    graph.connect('Aracaju', 'Maceio', 294)
    graph.connect('Maceio', 'Recife', 285)
    graph.connect('Recife', 'JoaoPessoa', 120)
    graph.connect('JoaoPessoa', 'Natal', 185)
    graph.connect('BeloHorizonte', 'SaoPaulo', 586)
    graph.connect('BeloHorizonte', 'RioDeJaneiro', 434)
    
    # making dataframe 
    df = pd.read_csv("DistanciaDasCidades.csv") 
    
    # Trasformar as cidades em index
    df.set_index("Cidades",inplace=True)
    
    # Trasforma o grafo unidiricionalmente
    graph.make_undirected()
    
    # Criar as heurística (distância em linha reta, distância de viagem aérea)
    heuristics = {}
    heuristics['BoaVista'] = df.loc[end, 'BoaVista']
    heuristics['Manaus'] = df.loc[end, 'Manaus']
    heuristics['RioBranco'] = df.loc[end, 'RioBranco']
    heuristics['PortoVelho'] = df.loc[end, 'PortoVelho']
    heuristics['Belem'] = df.loc[end, "Belem"]
    heuristics['Macapa'] = df.loc[end, 'Macapa']
    heuristics['Cuiaba'] = df.loc[end, 'Cuiaba']
    heuristics['CampoGrande'] = df.loc[end, 'CampoGrande']
    heuristics['Curitiba'] = df.loc[end, 'Curitiba']
    heuristics['Florianopolis'] = df.loc[end, 'Florianopolis']
    heuristics['PortoAlegre'] = df.loc[end, 'PortoAlegre']
    heuristics['SaoPaulo'] = df.loc[end, 'SaoPaulo']
    heuristics['RioDeJaneiro'] = df.loc[end, 'RioDeJaneiro']
    heuristics['Vitoria'] = df.loc[end, 'Vitoria']
    heuristics['Salvador'] = df.loc[end, 'Salvador']
    heuristics['Aracaju'] = df.loc[end, 'Maceio']
    heuristics['Maceio'] = df.loc[end, "Belem"]
    heuristics['Recife'] = df.loc[end, 'Recife']
    heuristics['Natal'] = df.loc[end, 'Natal']
    heuristics['JoaoPessoa'] = df.loc[end, 'JoaoPessoa']
    heuristics['Fortaleza'] = df.loc[end, 'Fortaleza']
    heuristics['SaoLuis'] = df.loc[end, 'SaoLuis']
    heuristics['Brasilia'] = df.loc[end, 'Brasilia']
    heuristics['BeloHorizonte'] = df.loc[end, 'BeloHorizonte']
    heuristics['Goiania'] = df.loc[end, 'Goiania']
    heuristics['Palmas'] = df.loc[end, 'Palmas']
    heuristics['Teresina'] = df.loc[end, 'Teresina']
    
    return graph, heuristics
