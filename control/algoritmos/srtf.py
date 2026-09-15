from model.prioridade import Prioridade


def srtf(processos, ctx_time=0):
    tempo_atual = 0
    ultimo_processo_id = None
    ctx_time = float(ctx_time)

    # 1. Inicialização dos processos
    for p in processos:
        p.tempo_restante = int(p.duracao)
        p.tempo_executado = 0
        p.processamentos = []

    pendentes = [p for p in processos if p.tempo_restante > 0]

    while pendentes:
        # Filtra os processos que já chegaram
        chegados = [p for p in pendentes if p.chegada <= tempo_atual]

        # Se a CPU está ociosa, salta direto para a próxima chegada (C10)
        if not chegados:
            proximas_chegadas = [p.chegada for p in pendentes if p.chegada > tempo_atual]
            if not proximas_chegadas:
                raise RuntimeError("Não foi possível encontrar próximo evento.")
            tempo_atual = min(proximas_chegadas)
            continue

        # 2. Escolha pelo critério SRTF: menor tempo restante,
        # menor chegada, menor id (C3)
        escolhido = min(
            chegados,
            key=lambda p: (p.tempo_restante, p.chegada, p.id)
        )

        # 3. Troca de Contexto na tarefa que está ENTRANDO
        # C4: inclusive no 1º despacho
        if escolhido.id != ultimo_processo_id and ctx_time > 0:
            escolhido.adicionar_troca_contexto(
                tempo_atual,
                tempo_atual + ctx_time
            )
            tempo_atual += ctx_time

        # 4. Executa exatamente 1 unidade discreta de tempo
        # C1 - Preemptivo
        duracao_executada = escolhido.adicionar_processamento(
            tempo_atual,
            tempo_atual + 1
        )
        tempo_atual += duracao_executada

        ultimo_processo_id = escolhido.id

        # 5. Remove da lista de pendentes se a tarefa finalizou
        if escolhido.tempo_restante <= 0:
            pendentes.remove(escolhido)

    # 6. Cálculo das métricas oficiais (C8: tw = tt - tp)
    if not processos:
        return 0, 0, "SRTF"

    media_execucao = sum(p.get_turnaround() for p in processos) / len(processos)
    media_espera = sum(p.get_espera() for p in processos) / len(processos)
    media_primeria_execucao = sum(p.get_tempo_primeira_execucao() for p in processos) / len(processos)

    return media_execucao, media_espera, media_primeria_execucao, "SRTF"