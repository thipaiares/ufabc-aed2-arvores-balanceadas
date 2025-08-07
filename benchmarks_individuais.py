from pympler import asizeof
from avl import PerfilDisponibilidadeAVL
from rubronegra import PerfilDisponibilidadeRN
import random
import time

def gerar_intervalos(n, total_recursos):
    return [(i, i + n - 1) for i in range(0, total_recursos - n + 1, n)]

def benchmark_ins_mem(quantidade_nos, nRec, intervalos, repeticoes, imprimir_repeticoes):
    tempos_insercao_RN = []
    memorias_RN = []

    tempos_insercao_AVL = []
    memorias_AVL = []

    for i in range(repeticoes):
        tempos = sorted(random.sample(range(0, 10000000000, 50), quantidade_nos))

        perfilRN = PerfilDisponibilidadeRN()

        start_insercao_RN = time.perf_counter()
        for t in tempos:
            perfilRN.criar_no(t, nRec, intervalos)
        tempos_insercao_RN.append(time.perf_counter() - start_insercao_RN)

        memoria_RN = asizeof.asizeof(perfilRN)
        memorias_RN.append(memoria_RN)

        perfilAVL = PerfilDisponibilidadeAVL()

        start_insercao_AVL = time.perf_counter()
        for t in tempos:
            perfilAVL.criar_no(t, nRec, intervalos)
        tempos_insercao_AVL.append(time.perf_counter() - start_insercao_AVL)

        memoria_AVL = asizeof.asizeof(perfilAVL)
        memorias_AVL.append(memoria_AVL)

        if imprimir_repeticoes:
          print(f"Repetição {i+1}:")
          print(f"[RN]  Inserção={tempos_insercao_RN[-1]:.4f}s, Memória={memoria_RN / (1024**2):.4f} MB")
          print(f"[AVL] Inserção={tempos_insercao_AVL[-1]:.4f}s, Memória={memoria_AVL / (1024**2):.4f} MB\n")

    print("\n===== Árvore Rubro-Negra =====")
    print(f"\nMédia de inserção: {sum(tempos_insercao_RN)/repeticoes:.4f} s")
    print(f"Média de memória: {sum(memorias_RN)/repeticoes / (1024**2):.4f} MB\n")

    print("===== Árvore AVL =====")
    print(f"\nMédia de inserção: {sum(tempos_insercao_AVL)/repeticoes:.4f} s")
    print(f"Média de memória: {sum(memorias_AVL)/repeticoes / (1024**2):.4f} MB\n")

def benchmark_buscas(quantidade_nos, nRec, intervalos, repeticoes, buscas_por_repeticao, imprimir_repeticoes):
    tempos = sorted(random.sample(range(0, 10000000000, 50), quantidade_nos))
    tempos_busca_RN = []
    tempos_busca_AVL = []

    perfilRN = PerfilDisponibilidadeRN()
    perfilAVL = PerfilDisponibilidadeAVL()

    for t in tempos:
            perfilRN.criar_no(t, nRec, intervalos)
            perfilAVL.criar_no(t, nRec, intervalos)

    for i in range(repeticoes):
        tempos_para_busca = random.sample(tempos, buscas_por_repeticao)

        start_busca_RN = time.perf_counter()
        for t_busca in tempos_para_busca:
            _ = perfilRN.encontrar_ancora(t_busca)
        tempos_busca_RN.append(time.perf_counter() - start_busca_RN)

        start_busca_AVL = time.perf_counter()
        for t_busca in tempos_para_busca:
            _ = perfilAVL.encontrar_ancora(t_busca)
        tempos_busca_AVL.append(time.perf_counter() - start_busca_AVL)

        if imprimir_repeticoes:
          print(f"Repetição {i+1}:")
          print(f"[RN]  Buscas={tempos_busca_RN[-1]:.4f}s")
          print(f"[AVL] Buscas={tempos_busca_AVL[-1]:.4f}s\n")

    print("\n===== Árvore Rubro-Negra =====")
    print(f"Média de buscas: {sum(tempos_busca_RN)/repeticoes:.4f} s")

    print("===== Árvore AVL =====")
    print(f"Média de buscas: {sum(tempos_busca_AVL)/repeticoes:.4f} s")

def benchmark_req(quantidade_nos, nRec, intervalos, qtd_chamadas, repeticoes, imprimir_repeticoes):
    tempos = sorted(random.sample(range(0, 10000000000, 50), quantidade_nos))
    tempos_req_RN = []
    tempos_req_AVL = []

    perfilRN = PerfilDisponibilidadeRN()
    perfilAVL = PerfilDisponibilidadeAVL()

    for t in tempos:
        perfilRN.criar_no(t, nRec, intervalos)
        perfilAVL.criar_no(t, nRec, intervalos)


    for i in range(repeticoes):
        chamadas = []

        for _ in range(qtd_chamadas):
            t0 = random.choice(tempos[:-100])
            duracao = random.randint(200, 1000) 
            t1 = t0 + duracao
            req = random.randint(1, 3)
            chamadas.append((t0, t1, req))

        total_visitado_RN = 0
        total_possivel_RN = 0
        sucessos_RN = 0

        start_req_RN = time.perf_counter()
        for t0, t1, req in chamadas:
            _, visitado, possivel = perfilRN.confirmar_disponibilidade(t0, t1, req)
            total_visitado_RN += visitado
            total_possivel_RN += possivel
            if visitado > 0:
                sucessos_RN += 1
        tempos_req_RN.append(time.perf_counter() - start_req_RN)

        total_visitado_AVL = 0
        total_possivel_AVL = 0
        sucessos_AVL = 0

        start_req_AVL = time.perf_counter()
        for t0, t1, req in chamadas:
            _, visitado, possivel = perfilAVL.confirmar_disponibilidade(t0, t1, req)
            total_visitado_AVL += visitado
            total_possivel_AVL += possivel
            if visitado > 0:
                sucessos_AVL += 1
        tempos_req_AVL.append(time.perf_counter() - start_req_AVL)

        if imprimir_repeticoes:
            print(f"=========Repetição {i+1}:=========")
            print(f"[RN]  Tempo de processamento={tempos_req_RN[-1]:.4f}s")
            print(f"[RN] Chamadas bem-sucedidas: {sucessos_RN}/{qtd_chamadas}")

            print(f"\n\n[AVL] Tempo de processamento={tempos_req_AVL[-1]:.4f}s")
            print(f"[AVL] Chamadas bem-sucedidas: {sucessos_AVL}/{qtd_chamadas}\n")


    print("\n===== Árvore Rubro-Negra =====")
    print(f"Média de processamento de {qtd_chamadas} chamadas: {sum(tempos_req_RN)/repeticoes:.4f} s")

    print("===== Árvore AVL =====")
    print(f"Média de processamento de {qtd_chamadas} chamadas: {sum(tempos_req_AVL)/repeticoes:.4f} s")

if __name__ == '__main__':
    quantidade_nos = 15000
    nRec = 10
    intervalos = gerar_intervalos(nRec, 20)
    buscas_por_repeticao = 1000
    repeticoes = 5
    imprimir_repeticoes = True
    qtd_chamadas = 15000

    print("INSERÇÃO E MEMÓRIA:")
    benchmark_ins_mem(quantidade_nos, nRec, intervalos, repeticoes, imprimir_repeticoes)
    print(f"\n{buscas_por_repeticao} BUSCAS")
    benchmark_buscas(quantidade_nos, nRec, intervalos, repeticoes, buscas_por_repeticao, imprimir_repeticoes)
    print("\n REQUISIÇÕES")
    benchmark_req(quantidade_nos, nRec, intervalos, qtd_chamadas, repeticoes, imprimir_repeticoes)