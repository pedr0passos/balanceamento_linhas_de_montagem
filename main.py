import time
import numpy as np
import random
import re

# Funções Auxiliares

def read_file(path='HAHN.IN2'):
    """
    Lê o arquivo de instâncias e retorna a matriz de adjacência, a lista de custos e o número de tarefas.
    
    Parâmetros:
    - path: Caminho para o arquivo de instâncias.
    
    Retorna:
    - matriz: Matriz de adjacência representando a precedência das tarefas.
    - custos: Lista com os tempos de execução de cada tarefa.
    - numeroTarefas: Número total de tarefas.
    """
    
    # Abre o arquivo de instâncias para leitura
    with open(path, "r") as file:
        # Lê o número total de tarefas, que é o primeiro valor no arquivo
        total_tarefas = int(file.readline().strip())
        
        # Cria uma matriz de zeros (total_tarefas x total_tarefas) para representar a precedência entre tarefas
        matriz = np.zeros((total_tarefas, total_tarefas), dtype=int)
        
        # Inicializa a lista de custos, que armazenará o tempo de execução de cada tarefa
        custos = []

        # Lê os custos das tarefas, que são os próximos 'total_tarefas' valores no arquivo
        for _ in range(total_tarefas):
            custo = int(file.readline().strip())  # Converte o valor lido para inteiro
            custos.append(custo)  # Adiciona o custo na lista de custos

        # Lê as precedências e preenche a matriz de adjacência
        for linha in file:
            linha = linha.strip()  # Remove espaços em branco e quebras de linha

            # Verifica se a linha está vazia ou se contém a sequência '-1,-1', que indica o fim da lista de precedências
            if not linha or linha == '-1,-1':
                break

            # Usa regex para separar os números por vírgula seguida de qualquer número de espaços
            par = re.split(r',\s*', linha)

            # Verifica se a linha contém exatamente dois números
            if len(par) != 2:
                continue  # Se não, pula para a próxima linha

            # Converte os números da linha para inteiros
            n1, n2 = map(int, par)

            # Verifica se algum dos números é -1, indicando o fim das precedências
            if n1 == -1 or n2 == -1:
                break

            # Ajusta os índices para serem baseados em zero (subtrai 1) e marca a precedência na matriz
            matriz[n1 - 1][n2 - 1] = 1
    
    # Retorna a matriz de adjacência, a lista de custos e o número total de tarefas
    return matriz, custos, total_tarefas

def calcular_fo(solucao, custos):
    """
    Calcula a função objetivo (FO) para uma solução dada.
    
    Parâmetros:
    - solucao: Uma lista de listas, onde cada sublista representa as tarefas atribuídas a uma máquina.
    - custos: Uma lista contendo o tempo de execução de cada tarefa.

    Retorna:
    - maior_ciclo: O maior tempo total (ciclo) entre todas as máquinas, que representa a função objetivo.
    """
    
    # Inicializa a variável maior_ciclo com 0, que armazenará o maior ciclo encontrado
    maior_ciclo = 0
    
    # Itera sobre cada máquina na solução
    for maquina in solucao:
        # Calcula o ciclo total (soma dos tempos de execução) para a máquina atual
        ciclo = sum(custos[tarefa] for tarefa in maquina)
        
        # Atualiza maior_ciclo se o ciclo atual for maior do que o maior ciclo encontrado até agora
        maior_ciclo = max(maior_ciclo, ciclo)
    
    # Retorna o maior ciclo encontrado, que é o valor da função objetivo para a solução
    return maior_ciclo

def distribuir_tarefas_aleatoriamente(numero_de_maquinas, numero_de_tarefas):
    """
    Distribui as tarefas aleatoriamente entre as máquinas, garantindo que cada máquina receba pelo menos uma tarefa.
    
    Parâmetros:
    - numero_de_maquinas: O número total de máquinas disponíveis.
    - numero_de_tarefas: O número total de tarefas a serem distribuídas.

    Retorna:
    - tarefas_por_maquina: Um array onde cada elemento indica o número de tarefas atribuídas a cada máquina.
    """
    
    # Cria um array de zeros onde cada elemento representará a quantidade de tarefas atribuídas a uma máquina
    tarefas_por_maquina = np.zeros(numero_de_maquinas, dtype=int)
    
    # Distribui as tarefas sequencialmente entre as máquinas
    for i in range(0, numero_de_tarefas):
        # Usa o operador módulo para distribuir as tarefas de forma cíclica entre as máquinas
        tarefas_por_maquina[i % numero_de_maquinas] += 1   
    
    # Embaralha o array de tarefas por máquina para garantir uma distribuição aleatória
    np.random.shuffle(tarefas_por_maquina)
    
    # Retorna o array que indica quantas tarefas foram atribuídas a cada máquina
    return tarefas_por_maquina

def imprimir_resultados(numero_de_maquinas, solucao_inicial, fo_inicial, solucao_refinada, fo_refinada):
    
    """
    Imprime os resultados de uma solução inicial e refinada, incluindo o número de máquinas,
    a alocação de tarefas em cada máquina e o valor da função objetivo (FO).
    
    Parâmetros:
    - numero_de_maquinas: O número total de máquinas utilizadas na solução.
    - solucao_inicial: Uma lista de listas, onde cada sublista representa as tarefas atribuídas a uma máquina na solução inicial.
    - fo_inicial: O valor da função objetivo calculado para a solução inicial.
    - solucao_refinada: Uma lista de listas representando as tarefas atribuídas a cada máquina na solução refinada.
    - fo_refinada: O valor da função objetivo calculado para a solução refinada.

    Retorna:
    - None. A função apenas imprime os resultados.
    """

    print(f"Numero de maquinas: {numero_de_maquinas}")
    print("Solução Inicial:")

    for i, tarefas in enumerate(solucao_inicial):
        tarefas_formatadas = ",".join(str(tarefa) for tarefa in tarefas)
        print(f"Maquina {i + 1}: {tarefas_formatadas}")
    
    print(f"FO Inicial: {fo_inicial}")
    print('------------------------------------')
    print("Solução Refinada:")

    for i, tarefas in enumerate(solucao_refinada):
        tarefas_formatadas = ",".join(str(tarefa) for tarefa in tarefas)
        print(f"Maquina {i + 1}: {tarefas_formatadas}")
    
    print(f"FO Refinada: {fo_refinada}")
    print('------------------------------------')

def gerar_sequencia(numero_de_tarefas, matriz):
    """
    Gera uma sequência de tarefas com base nas precedências definidas na matriz.
    As tarefas são escolhidas de forma que respeitem a ordem de precedência e são embaralhadas aleatoriamente.

    Parâmetros:
    - numero_de_tarefas: O número total de tarefas.
    - matriz: Matriz de adjacência representando as precedências entre as tarefas.

    Retorna:
    - sequencia: Uma lista com a sequência de tarefas gerada.
    """
    
    # Cria uma lista vazia para armazenar a sequência de tarefas
    sequencia = []
    
    # Faz uma cópia da matriz original para modificar durante o processo
    matriz_auxiliar = np.copy(matriz)
    
    # Itera sobre o número de tarefas para gerar a sequência
    for _ in range(numero_de_tarefas):
        # Encontra tarefas candidatas para serem adicionadas à sequência
        candidatos = [j for j in range(numero_de_tarefas) if np.sum(matriz_auxiliar[:, j]) == 0]
        
        # Embaralha aleatoriamente a lista de candidatos
        random.shuffle(candidatos)
        
        # Seleciona a primeira tarefa da lista de candidatos e a remove da lista
        escolhido = candidatos.pop(0)
        
        # Adiciona a tarefa escolhida à sequência
        sequencia.append(escolhido)
        
        # Atualiza a matriz auxiliar para refletir a adição da tarefa à sequência
        matriz_auxiliar[escolhido, :] = 0  # Remove a tarefa escolhida das linhas
        matriz_auxiliar[:, escolhido] = -1  # Remove a tarefa escolhida das colunas
        
    return sequencia

# Heurísticas

def cria_solucao_inicial(numero_de_maquinas, custos, matriz):
    """
    Cria uma solução inicial para o problema de alocação de tarefas às máquinas.
    A solução é gerada distribuindo tarefas aleatoriamente entre as máquinas e respeitando as precedências.

    Parâmetros:
    - numero_de_maquinas: O número total de máquinas disponíveis.
    - matriz: Matriz de adjacência representando as precedências entre as tarefas.

    Retorna:
    - solucao: Uma lista de listas, onde cada sublista representa as tarefas atribuídas a uma máquina.
    """
    
    # Obtém o número total de tarefas a partir do tamanho da matriz
    numero_de_tarefas = len(matriz)
    
    # Inicializa a lista para armazenar a solução
    solucao = []
    
    # Distribui as tarefas aleatoriamente entre as máquinas
    numero_de_tarefas_por_maquina = distribuir_tarefas_aleatoriamente(numero_de_maquinas, numero_de_tarefas)
    
    # Gera uma sequência de tarefas respeitando as precedências
    sequencia_de_tarefas = gerar_sequencia(numero_de_tarefas, matriz)
    
    # Atribui as tarefas a cada máquina com base na distribuição aleatória
    for maquina in range(numero_de_maquinas):
        tarefas_por_maquina = []
        # Adiciona o número de tarefas especificado para a máquina atual
        for _ in range(int(numero_de_tarefas_por_maquina[maquina])):
            if sequencia_de_tarefas:
                # Remove a primeira tarefa da sequência e a adiciona à lista de tarefas da máquina
                tarefas_por_maquina.append(sequencia_de_tarefas.pop(0))
        # Adiciona a lista de tarefas da máquina à solução
        solucao.append(tarefas_por_maquina)

    fo_inicial = calcular_fo(solucao, custos)    
    return solucao, fo_inicial

def gerar_vizinho(solucao, matriz, tentativas_max=100):
    """
    Gera um vizinho da solução atual trocando duas tarefas entre duas máquinas diferentes.
    Tenta encontrar uma nova solução válida dentro do número máximo de tentativas.

    Parâmetros:
    - solucao: Solução atual, uma lista de listas onde cada sublista representa as tarefas atribuídas a uma máquina.
    - matriz: Matriz de adjacência representando as precedências entre as tarefas.
    - tentativas_max: Número máximo de tentativas para encontrar uma solução válida.

    Retorna:
    - vizinho: Nova solução vizinha, se encontrada; caso contrário, retorna a solução original.
    """
    
    # Cria uma cópia da solução atual para modificar durante o processo
    vizinho = [list(maquina) for maquina in solucao]
    
    # Obtém o número de máquinas
    numero_de_maquinas = len(solucao)
    
    # Inicializa o contador de tentativas
    tentativas = 0

    # Tenta encontrar uma nova solução válida até o número máximo de tentativas
    while tentativas < tentativas_max:
        # Seleciona duas máquinas diferentes aleatoriamente
        maquina1, maquina2 = np.random.choice(numero_de_maquinas, 2, replace=False)
        
        # Verifica se pelo menos uma das máquinas selecionadas tem tarefas
        if not vizinho[maquina1] or not vizinho[maquina2]:
            # Incrementa o contador de tentativas e tenta novamente
            tentativas += 1
            continue
        
        # Seleciona uma tarefa aleatória de cada uma das máquinas selecionadas
        tarefa1 = np.random.choice(vizinho[maquina1])
        tarefa2 = np.random.choice(vizinho[maquina2])
        
        # Remove as tarefas selecionadas das máquinas originais
        vizinho[maquina1].remove(tarefa1)
        vizinho[maquina2].remove(tarefa2)
        
        # Adiciona as tarefas trocadas às máquinas
        vizinho[maquina1].append(tarefa2)
        vizinho[maquina2].append(tarefa1)
        
        # Verifica se a nova solução é válida
        if verifica_precedencia(vizinho, matriz):
            # Se válida, retorna a nova solução vizinha
            return vizinho
        else:
            # Se não válida, reverte a troca
            vizinho[maquina1].remove(tarefa2)
            vizinho[maquina2].remove(tarefa1)
            vizinho[maquina1].append(tarefa1)
            vizinho[maquina2].append(tarefa2)

        # Incrementa o contador de tentativas
        tentativas += 1
    
    # Se não encontrar uma solução válida dentro do número máximo de tentativas, retorna a solução original
    return solucao

def verifica_precedencia(solucao, matriz):
    """
    Verifica se uma solução respeita as restrições de precedência.
    
    Parâmetros:
    - solucao: A solução atual (lista de listas, representando tarefas em máquinas).
    - matriz: Matriz de adjacência representando a precedência das tarefas.
    
    Retorna:
    - True se a solução respeitar todas as precedências, False caso contrário.
    """
    # Itera sobre cada máquina na solução
    for tarefas in solucao:
        # Verifica as precedências entre cada par de tarefas na mesma máquina
        for i in range(len(tarefas)):
            for j in range(i + 1, len(tarefas)):
                tarefa_i = tarefas[i]
                tarefa_j = tarefas[j]
                # Se houver uma restrição de precedência violada, retorna False
                if matriz[tarefa_j][tarefa_i]:  # tarefa_j não pode vir antes de tarefa_i
                    return False
    return True

def heuristica_descida_randomica(solucao_inicial, custos, matriz, iteracoes_sem_melhora=100):
    """
    Aplica o método de Descida Randômica para refinar a solução inicial.
    O método tenta melhorar a solução atual gerando vizinhos aleatórios e selecionando o melhor.

    Parâmetros:
    - solucao_inicial: Solução inicial para começar o refinamento. Representa a distribuição das tarefas entre as máquinas.
    - custos: Lista com os tempos de execução de cada tarefa.
    - matriz: Matriz de adjacência representando a precedência das tarefas.
    - iteracoes_sem_melhora: Número máximo de iterações sem melhora na função objetivo (FO) antes de parar.

    Retorna:
    - solucao_otimizada: Solução refinada após aplicar o método de descida randômica.
    - melhor_fo: O valor da função objetivo (FO) da solução refinada.
    """
    
    # Inicializa a solução atual com a solução inicial fornecida
    solucao_atual = solucao_inicial
    
    # Calcula o valor da função objetivo (FO) para a solução inicial
    melhor_fo = calcular_fo(solucao_atual, custos)
    
    # Inicializa o contador de iterações sem melhora
    iteracoes_sem_melhora_contador = 0
    
    # Executa o loop enquanto o contador de iterações sem melhora for menor que o limite
    while iteracoes_sem_melhora_contador < iteracoes_sem_melhora:
        # Gera um vizinho da solução atual
        vizinho = gerar_vizinho(solucao_atual, matriz)
        
        # Calcula o valor da função objetivo (FO) para o vizinho gerado
        fo_vizinho = calcular_fo(vizinho, custos)
        
        # Se o valor da função objetivo do vizinho for melhor (menor) que o da solução atual
        if fo_vizinho < melhor_fo:
            # Atualiza a solução atual com o vizinho
            solucao_atual = vizinho
            # Atualiza o melhor valor da função objetivo (FO)
            melhor_fo = fo_vizinho
            # Reseta o contador de iterações sem melhora
            iteracoes_sem_melhora_contador = 0
        else:
            # Incrementa o contador de iterações sem melhora
            iteracoes_sem_melhora_contador += 1
    
    # Retorna a solução otimizada e o valor da função objetivo (FO) correspondente
    return solucao_atual, melhor_fo

def main():
    start = time.time()
    print('------------------------------------')
    matriz, custos, _ = read_file()
    for numero_de_maquinas in range(6, 11):
        solucao_inicial, fo_inicial = cria_solucao_inicial(numero_de_maquinas, custos, matriz)
        solucao_refinada, fo_refinada = heuristica_descida_randomica(solucao_inicial, custos, matriz)
        imprimir_resultados(numero_de_maquinas, solucao_inicial, fo_inicial, solucao_refinada, fo_refinada)
    end = time.time()
    print(f"Tempo de execução: {end - start:.4f} segundos")

if __name__ == "__main__":
    main()
