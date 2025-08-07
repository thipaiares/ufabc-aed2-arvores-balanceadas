from typing import List, Tuple, Optional

VERMELHO = True
PRETO = False

class NoRubroNegra:
    def __init__(self, tempo: int, nRec: int, intervalos: List[Tuple[int, int]]):
        self.tempo = tempo
        self.nRec = nRec
        self.intervalos = intervalos

        self.cor = VERMELHO
        self.esquerda = None
        self.direita = None
        self.pai = None

class PerfilDisponibilidadeRN:
    def __init__(self):
        self.nulo = NoRubroNegra(-1, 0, [])
        self.nulo.cor = PRETO
        self.raiz = self.nulo

    def criar_no(self, tempo: int, nRec: int, intervalos: List[Tuple[int, int]]) -> NoRubroNegra:
        novo = NoRubroNegra(tempo, nRec, intervalos)
        novo.esquerda = self.nulo
        novo.direita = self.nulo
        novo.cor = VERMELHO
        self._inserir_rubronegra(novo)

        return novo

    def _inserir_rubronegra(self, no: NoRubroNegra):
        pai = self.nulo
        filho = self.raiz
        while filho != self.nulo:
            pai = filho
            if no.tempo < filho.tempo:
                filho = filho.esquerda
            else:
                filho = filho.direita
        no.pai = pai
        if pai == self.nulo:
            self.raiz = no
        elif no.tempo < pai.tempo:
            pai.esquerda = no
        else:
            pai.direita = no
        no.esquerda = self.nulo
        no.direita = self.nulo
        no.cor = VERMELHO
        self._corrige_arvore(no)

    def _corrige_arvore(self, no):
        while no.pai.cor == VERMELHO:
            if no.pai == no.pai.pai.esquerda:
                aux = no.pai.pai.direita
                if aux.cor == VERMELHO:
                    no.pai.cor = PRETO
                    aux.cor = PRETO
                    no.pai.pai.cor = VERMELHO
                    no = no.pai.pai
                else:
                    if no == no.pai.direita:
                        no = no.pai
                        self._rotacionar_esquerda(no)
                    no.pai.cor = PRETO
                    no.pai.pai.cor = VERMELHO
                    self._rotacionar_direita(no.pai.pai)
            else:
                aux = no.pai.pai.esquerda
                if aux.cor == VERMELHO:
                    no.pai.cor = PRETO
                    aux.cor = PRETO
                    no.pai.pai.cor = VERMELHO
                    no = no.pai.pai
                else:
                    if no == no.pai.esquerda:
                        no = no.pai
                        self._rotacionar_direita(no)
                    no.pai.cor = PRETO
                    no.pai.pai.cor = VERMELHO
                    self._rotacionar_esquerda(no.pai.pai)
        self.raiz.cor = PRETO

    def _rotacionar_esquerda(self, no):
        f_dir = no.direita
        no.direita = f_dir.esquerda
        if f_dir.esquerda != self.nulo:
            f_dir.esquerda.pai = no
        f_dir.pai = no.pai
        if no.pai == self.nulo:
            self.raiz = f_dir
        elif no == no.pai.esquerda:
            no.pai.esquerda = f_dir
        else:
            no.pai.direita = f_dir
        f_dir.esquerda = no
        no.pai = f_dir

    def _rotacionar_direita(self, no):
        f_esq = no.esquerda
        no.esquerda = f_esq.direita
        if f_esq.direita != self.nulo:
            f_esq.direita.pai = no
        f_esq.pai = no.pai
        if no.pai == self.nulo:
            self.raiz = f_esq
        elif no == no.pai.direita:
            no.pai.direita = f_esq
        else:
            no.pai.esquerda = f_esq
        f_esq.direita = no
        no.pai = f_esq

    def encontrar_ancora(self, tempo_inicio: int) -> Optional[NoRubroNegra]:
        no = self.raiz
        resultado = None
        while no != self.nulo:
            if no.tempo <= tempo_inicio:
                resultado = no
                no = no.direita
            else:
                no = no.esquerda
        return resultado

    def confirmar_disponibilidade(self, tempo_inicio: int, tempo_fim: int, reqRec: int) -> Tuple[Optional[Tuple[int, List[Tuple[int, int]]]], int, int]:
        ancora = self.encontrar_ancora(tempo_inicio)
        if ancora is None or ancora.nRec < reqRec:
            return None, 0, 0

        intersec = ancora.intervalos.copy()
        visitados = 0
        total_possivel = 0

        no = ancora
        while no is not None and no.tempo < tempo_fim:
            total_possivel += 1

            if no.nRec < reqRec:
                return None, visitados, total_possivel

            intersec = self._intersecao_intervalos(intersec, no.intervalos)
            if self._contar_recursos(intersec) < reqRec:
                return None, visitados, total_possivel

            visitados += 1
            no = self.sucessor(no)

        if visitados == 0:
            return None, visitados, total_possivel

        return (ancora.tempo, intersec), visitados, total_possivel

    def sucessor(self, no: NoRubroNegra) -> Optional[NoRubroNegra]:
        if no.direita != self.nulo:
            return self._minimo(no.direita)

        pai = no.pai
        while pai != self.nulo and no == pai.direita:
            no = pai
            pai = pai.pai
        return pai if pai != self.nulo else None

    def _minimo(self, no: NoRubroNegra) -> NoRubroNegra:
        while no.esquerda != self.nulo:
            no = no.esquerda
        return no

    def _intersecao_intervalos(self, a: List[Tuple[int, int]], b: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        resultado = []
        i = j = 0
        while i < len(a) and j < len(b):
            comeco = max(a[i][0], b[j][0])
            fim = min(a[i][1], b[j][1])
            if comeco <= fim:
                resultado.append((comeco, fim))
            if a[i][1] < b[j][1]:
                i += 1
            else:
                j += 1
        return resultado

    def _contar_recursos(self, intervalos: List[Tuple[int, int]]) -> int:
        return sum(fim - comeco + 1 for comeco, fim in intervalos)