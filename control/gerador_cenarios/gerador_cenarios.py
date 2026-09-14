import random

from model.processo import Processo
from model.prioridade import Prioridade


def gerar_cenario(quantidade):
    processos = []

    for i in range(1, quantidade + 1):
        chegada = random.randint(0, 8)
        duracao = random.randint(1, 6)
        prioridade = random.randint(1, 5)

        processo = Processo(
            i,
            chegada,
            duracao,
            Prioridade(prioridade)
        )

        processos.append(processo)

    processos.sort(
        key=lambda p: (
            p.id
        )
    )

    return processos