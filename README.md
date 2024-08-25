# Projeto de Distribuição de Tarefas

## Descrição

Este projeto implementa um algoritmo de otimização para o problema de **distribuição de tarefas** entre máquinas, utilizando o método de **Descida Randômica**. O objetivo é minimizar o tempo máximo de execução das máquinas, respeitando as precedências entre as tarefas.

## Funcionalidades

1. **Leitura de Arquivo**
   - Função: `read_file(path='Trabalho/instancia.txt')`
   - Descrição: Lê um arquivo de instâncias para obter a matriz de adjacência (precedência entre tarefas), a lista de custos (tempos de execução das tarefas) e o número de tarefas.

2. **Cálculo da Função Objetivo (FO)**
   - Função: `calcular_fo(solucao, custos)`
   - Descrição: Calcula o tempo máximo de execução (ciclo mais longo) entre as máquinas para uma solução dada.

3. **Impressão dos Resultados**
   - Função: `imprimir_resultados(numero_de_maquinas, solucao_inicial, fo)`
   - Descrição: Imprime o número de máquinas, a distribuição de tarefas entre as máquinas e o valor da função objetivo para a solução fornecida.

4. **Distribuição Aleatória de Tarefas**
   - Função: `distribuir_tarefas_aleatoriamente(numero_de_maquinas, numero_de_tarefas)`
   - Descrição: Distribui aleatoriamente as tarefas entre as máquinas, garantindo que todas as máquinas recebam um número razoável de tarefas.

5. **Geração de Sequência de Tarefas**
   - Função: `gerar_sequencia(numero_de_tarefas, matriz)`
   - Descrição: Gera uma sequência de tarefas respeitando a matriz de precedência.

6. **Criação da Solução Inicial**
   - Função: `cria_solucao_inicial(numero_de_maquinas, matriz)`
   - Descrição: Cria uma solução inicial para a distribuição de tarefas, baseando-se na distribuição aleatória e na sequência gerada.

7. **Verificação da Solução**
   - Função: `verificar_solucao_valida(solucao, matriz)`
   - Descrição: Verifica se uma solução é válida, garantindo que as precedências entre as tarefas sejam respeitadas.

8. **Geração de Vizinho**
   - Função: `gerar_vizinho(solucao, matriz, tentativas_max=100)`
   - Descrição: Gera uma solução vizinha trocando tarefas entre duas máquinas diferentes, tentando encontrar uma solução melhor.

9. **Heurística de Descida Randômica**
   - Função: `heuristica_descida_randomica(solucao_inicial, custos, matriz, iteracoes_sem_melhora=100)`
   - Descrição: Aplica o método de descida randômica para refinar a solução inicial, buscando melhorar a função objetivo dentro do número máximo de iterações sem melhoria.

