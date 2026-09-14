import copy

from .gerador_cenarios import gerar_cenario
from control import simular_escalonamento


def executar_lote(
    quantidade_cenarios,
    quantidade_tarefas,
    quantum,
    chegada_max,
    duracao_max,
    prioridade_max,
    ctx_time=0,
    alpha=0
):
    resultados = {
        1: {"nome": "FCFS", "turnaround": [], "espera": []},
        2: {"nome": "SJF", "turnaround": [], "espera": []},
        3: {"nome": "Round Robin", "turnaround": [], "espera": []},
        4: {"nome": "SRTF", "turnaround": [], "espera": []},
        5: {"nome": "Prioridade Cooperativa", "turnaround": [], "espera": []},
        6: {"nome": "Prioridade Preemptiva", "turnaround": [], "espera": []}
    }

    for numero_cenario in range(quantidade_cenarios):

        cenario = gerar_cenario(
            quantidade_tarefas,
            chegada_max,
            duracao_max,
            prioridade_max
        )

        for algoritmo in range(1, 7):

            processos = copy.deepcopy(cenario)

            resultado = simular_escalonamento(
                processos,
                algoritmo,
                quantum,
                ctx_time,
                alpha
            )

            media_execucao, media_espera, nome_processo = resultado

            resultados[algoritmo]["turnaround"].append(media_execucao)
            resultados[algoritmo]["espera"].append(media_espera)

    for algoritmo in resultados:

        resultados[algoritmo]["turnaround_medio"] = (
            sum(resultados[algoritmo]["turnaround"])
            / len(resultados[algoritmo]["turnaround"])
        )

        resultados[algoritmo]["espera_media"] = (
            sum(resultados[algoritmo]["espera"])
            / len(resultados[algoritmo]["espera"])
        )

    return resultados