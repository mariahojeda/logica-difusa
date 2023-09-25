!pip install scikit-fuzzy
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# O primeiro nº é o nº inicial da escala.
# O segundo nº é a quantidade de valores dentro da escala.
# o terceiro nº representa o incremento da escala (de "quanto em quanto" ela aumenta).
PA = ctrl.Antecedent(np.arange(60, 201, 1), 'Pressão Arterial')
TRI = ctrl.Antecedent(np.arange(100, 201, 1), 'Triglicérides')
ESC = ctrl.Consequent(np.arange(0, 11, 1),  'Estado de Saúde Cardiovascular')

PA.automf(names=['baixa', 'normal', 'alta'])
TRI.automf(names=['baixo', 'normal', 'alto'])
ESC.automf(names=['ruim', 'moderado', 'bom'])


# Funções de pertinência
PA['baixa'] = fuzz.trimf(PA.universe, [60, 80, 100])
PA['normal'] = fuzz.trimf(PA.universe, [90, 125, 160])
PA['alta'] = fuzz.trimf(PA.universe, [140, 170, 200])

TRI['baixo'] = fuzz.trimf(TRI.universe, [100, 130, 160])
TRI['normal'] = fuzz.trimf(TRI.universe, [140, 170, 200])
TRI['alto'] = fuzz.trimf(TRI.universe, [190, 220, 250])

ESC['ruim'] = fuzz.trapmf(ESC.universe, [0, 0, 2.5, 3])
ESC['moderado'] = fuzz.trapmf(ESC.universe, [3.5, 5, 6, 6.5])
ESC['bom'] = fuzz.trapmf(ESC.universe, [7, 9, 9.5, 10])

PA.view()
TRI.view()
ESC.view()

# PA ALTA
rule1 = ctrl.Rule(PA['alta'] | TRI['alto'], ESC['ruim'])
rule2 = ctrl.Rule(PA['alta'] | TRI['baixo'], ESC['bom'])
rule3 = ctrl.Rule(PA['alta'] | TRI['normal'], ESC['moderado'])

# PA NORMAL
rule4 = ctrl.Rule(PA['normal'] | TRI['alto'], ESC['moderado'])
rule5 = ctrl.Rule(PA['normal'] | TRI['baixo'], ESC['bom'])
rule6 = ctrl.Rule(PA['normal'] | TRI['normal'], ESC['bom'])

# PA BAIXA
rule7 = ctrl.Rule(PA['baixa'] | TRI['alto'], ESC['moderado'])
rule8 = ctrl.Rule(PA['baixa'] | TRI['baixo'], ESC['bom'])
rule9 = ctrl.Rule(PA['baixa'] | TRI['normal'], ESC['bom'])

#Criando e simulando um controlador nebuloso
ESC_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
ESC_simulador = ctrl.ControlSystemSimulation(ESC_ctrl)

correspondencia = {
    (0, 4): 'ruim',
    (5, 6): 'moderado',
    (7, 10): 'bom'
}

# SIMULAÇÃO
ESC_simulador.input['Pressão Arterial'] = 100
ESC_simulador.input['Triglicérides'] = 40
ESC_simulador.compute() #computar resultado

resultado_numerico = ESC_simulador.output['Estado de Saúde Cardiovascular']

# Encontrar a chave mais próxima no dicionário correspondencia
resultado_chave = min(correspondencia, key=lambda x: abs(x[0] - resultado_numerico))
resultado_palavra = correspondencia[resultado_chave]

print("O seu Estado de Saúde é:", resultado_palavra)

PA.view(sim=ESC_simulador)
TRI.view(sim=ESC_simulador)
ESC.view(sim=ESC_simulador)