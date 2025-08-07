from pympler import asizeof
from benchmarks_individuais import gerar_intervalos
from avl import PerfilDisponibilidadeAVL
from rubronegra import PerfilDisponibilidadeRN
import random
import time
import pandas as pd
import openpyxl

def coletar_dados_benchmark(nRec, intervalos, buscas_por_repeticao):
    print("Iniciando benchmarks para coleta de dados...")

    nos_variacoes = [1000 * i for i in range(1, 21)]
    qtd_chamadas_variacoes = [1000 * i for i in range(1, 21)]
    repeticoes = len(nos_variacoes)

    df_ins_mem_list = []
    df_mem_list = []
    df_busca_list = []
    df_req_list = []

    for i in range(repeticoes):
        quantidade_nos = nos_variacoes[i]

        # --- Benchmark de Inserção e Memória ---
        tempos = sorted(random.sample(range(0, 100000000, 50), quantidade_nos))
        perfilRN = PerfilDisponibilidadeRN()
        start = time.perf_counter()
        for t in tempos:
            perfilRN.criar_no(t, nRec, intervalos)
        tempo_ins_rn = time.perf_counter() - start
        mem_rn = asizeof.asizeof(perfilRN)

        perfilAVL = PerfilDisponibilidadeAVL()
        start = time.perf_counter()
        for t in tempos:
            perfilAVL.criar_no(t, nRec, intervalos)
        tempo_ins_avl = time.perf_counter() - start
        mem_avl = asizeof.asizeof(perfilAVL)

        df_ins_mem_list.extend([
            {'Árvore': 'Rubro-Negra', 'Tipo': 'Inserção', 'Tamanho': quantidade_nos, 'Valor': tempo_ins_rn, 'Unidade': 's'},
            {'Árvore': 'AVL',         'Tipo': 'Inserção', 'Tamanho': quantidade_nos, 'Valor': tempo_ins_avl, 'Unidade': 's'},
        ])

        df_mem_list.extend([
            {'Árvore': 'Rubro-Negra', 'Tipo': 'Memória', 'Tamanho': quantidade_nos, 'Valor': mem_rn / (1024 ** 2), 'Unidade': 'MB'},
            {'Árvore': 'AVL',         'Tipo': 'Memória', 'Tamanho': quantidade_nos, 'Valor': mem_avl / (1024 ** 2), 'Unidade': 'MB'},
        ])

        # --- Benchmark de Buscas ---
        tempos_busca = random.sample(tempos, buscas_por_repeticao)
        start = time.perf_counter()
        for t in tempos_busca:
            perfilRN.encontrar_ancora(t)
        tempo_busca_rn = time.perf_counter() - start

        start = time.perf_counter()
        for t in tempos_busca:
            perfilAVL.encontrar_ancora(t)
        tempo_busca_avl = time.perf_counter() - start

        df_busca_list.extend([
            {'Árvore': 'Rubro-Negra', 'Tipo': 'Busca', 'Tamanho': quantidade_nos, 'Valor': tempo_busca_rn, 'Unidade': 's'},
            {'Árvore': 'AVL',         'Tipo': 'Busca', 'Tamanho': quantidade_nos, 'Valor': tempo_busca_avl, 'Unidade': 's'},
        ])

        # --- Benchmark de Requisições ---
        qtd_chamadas = qtd_chamadas_variacoes[i]
        chamadas = []
        for _ in range(qtd_chamadas):
            t0 = random.choice(tempos[:-100])
            duracao = random.randint(200, 1000)
            t1 = t0 + duracao
            req = random.randint(1, 3)
            chamadas.append((t0, t1, req))

        start = time.perf_counter()
        for t0, t1, req in chamadas:
            perfilRN.confirmar_disponibilidade(t0, t1, req)
        tempo_req_rn = time.perf_counter() - start

        start = time.perf_counter()
        for t0, t1, req in chamadas:
            perfilAVL.confirmar_disponibilidade(t0, t1, req)
        tempo_req_avl = time.perf_counter() - start

        df_req_list.extend([
            {'Árvore': 'Rubro-Negra', 'Tipo': 'Requisição', 'Chamadas': qtd_chamadas, 'Valor': tempo_req_rn, 'Unidade': 's'},
            {'Árvore': 'AVL',         'Tipo': 'Requisição', 'Chamadas': qtd_chamadas, 'Valor': tempo_req_avl, 'Unidade': 's'},
        ])

    return (
        pd.DataFrame(df_ins_mem_list),
        pd.DataFrame(df_mem_list),
        pd.DataFrame(df_busca_list),
        pd.DataFrame(df_req_list)
    )

if __name__ == '__main__':
    nRec = 10
    intervalos = gerar_intervalos(nRec, 20)
    buscas_por_repeticao = 1000

    df_ins_mem, df_mem, df_busca, df_req = coletar_dados_benchmark(
        nRec, intervalos, buscas_por_repeticao
    )

    from IPython.display import display

    print("📊 Tempo de Inserção por Tamanho:")
    display(df_ins_mem)

    print("\n📦 Memória após Inserção:")
    display(df_mem)

    print(f"\n🔍 Tempo de {buscas_por_repeticao} Buscas por Tamanho:")
    display(df_busca)

    print("\n🔁 Tempo de Requisições por Quantidade de Chamadas:")
    display(df_req)