from typing import List, Tuple, Optional

class NoAVL:
    def __init__(self, tempo: int, nRec: int, intervalos: List[Tuple[int, int]]):
        self.tempo = tempo
        self.nRec = nRec
        self.intervalos = intervalos

        self.altura = 1
        self.esquerda = None
        self.direita = None
        self.pai = None

class PerfilDisponibilidadeAVL:
    def __init__(self):
        self.raiz = None

    def criar_no(self, tempo: int, nRec: int, intervalos: List[Tuple[int, int]]) -> NoAVL:
        novo = NoAVL(tempo, nRec, intervalos)
        self.raiz = self._inserir_avl(self.raiz, novo)
        return novo

    def _inserir_avl(self, raiz: NoAVL, no: NoAVL) -> NoAVL:
        if raiz == None:
            return no

        if no.tempo < raiz.tempo:
            raiz.esquerda = self._inserir_avl(raiz.esquerda, no)
            raiz.esquerda.pai = raiz
        else:
            raiz.direita = self._inserir_avl(raiz.direita, no)
            raiz.direita.pai = raiz

        raiz.altura = 1 + max(self._calcular_altura(raiz.esquerda), self._calcular_altura(raiz.direita))

        fator_balanceamento = self._fator_balanceamento(raiz)

        if fator_balanceamento > 1 and no.tempo < raiz.esquerda.tempo:
            return self._rotacionar_direita(raiz)

        if fator_balanceamento < -1 and no.tempo > raiz.direita.tempo:
            return self._rotacionar_esquerda(raiz)

        if fator_balanceamento > 1 and no.tempo > raiz.esquerda.tempo:
            raiz.esquerda = self._rotacionar_esquerda(raiz.esquerda)
            return self._rotacionar_direita(raiz)

        if fator_balanceamento < -1 and no.tempo < raiz.direita.tempo:
            raiz.direita = self._rotacionar_direita(raiz.direita)
            return self._rotacionar_esquerda(raiz)

        return raiz

    def _calcular_altura(self, no: Optional[NoAVL]) -> int:
        if no is None:
            return 0
        return no.altura

    def _fator_balanceamento(self, no: Optional[NoAVL]) -> int:
        if no is None:
            return 0
        return self._calcular_altura(no.esquerda) - self._calcular_altura(no.direita)

    def _rotacionar_esquerda(self, no: NoAVL) -> NoAVL:
        f_dir = no.direita
        neto_dir_esq = f_dir.esquerda

        f_dir.esquerda = no
        no.direita = neto_dir_esq

        if neto_dir_esq:
            neto_dir_esq.pai = no

        f_dir.pai = no.pai
        no.pai = f_dir

        if f_dir.pai:
            if f_dir.pai.esquerda == no:
                f_dir.pai.esquerda = f_dir
            else:
                f_dir.pai.direita = f_dir
        else:
            self.raiz = f_dir

        no.altura = 1 + max(self._calcular_altura(no.esquerda), self._calcular_altura(no.direita))
        f_dir.altura = 1 + max(self._calcular_altura(f_dir.esquerda), self._calcular_altura(f_dir.direita))

        return f_dir

    def _rotacionar_direita(self, no: NoAVL) -> NoAVL:
        f_esq = no.esquerda
        neto_esq_dir = f_esq.direita

        f_esq.direita = no
        no.esquerda = neto_esq_dir

        if neto_esq_dir:
            neto_esq_dir.pai = no

        f_esq.pai = no.pai
        no.pai = f_esq

        if f_esq.pai:
            if f_esq.pai.esquerda == no:
                f_esq.pai.esquerda = f_esq
            else:
                f_esq.pai.direita = f_esq
        else:
            self.raiz = f_esq

        no.altura = 1 + max(self._calcular_altura(no.esquerda), self._calcular_altura(no.direita))
        f_esq.altura = 1 + max(self._calcular_altura(f_esq.esquerda), self._calcular_altura(f_esq.direita))

        return f_esq

    def encontrar_ancora(self, tempo_inicio: int) -> Optional[NoAVL]:
        no = self.raiz
        resultado = None
        while no:
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
        while no and no.tempo < tempo_fim:
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

    def sucessor(self, no: NoAVL) -> Optional[NoAVL]:
        if no.direita:
            return self._minimo(no.direita)

        pai = no.pai
        while pai and no == pai.direita:
            no = pai
            pai = pai.pai
        return pai

    def _minimo(self, no: NoAVL) -> NoAVL:
        while no.esquerda:
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