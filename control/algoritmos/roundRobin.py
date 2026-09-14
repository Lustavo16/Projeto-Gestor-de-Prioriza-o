def round_robin(processos, quantum=2, ctx_time=0):
    tempo_atual = 0
    ultimo_processo_id = None
    quantum = int(quantum)
    ctx_time = float(ctx_time)

    # 1. Inicialização limpa dos processos
    for p in processos:
        p.tempo_restante = int(p.duracao)
        p.tempo_executado = 0
        p.processamentos = []

    # C3: Desempate inicial por ordem de chegada e depois por ID
    nao_chegados = sorted(processos, key=lambda p: (p.chegada, p.id))
    fila_prontos = []

    while nao_chegados or fila_prontos:
        # Se a CPU está ociosa, salta direto para a próxima chegada (C10)
        if not fila_prontos:
            tempo_atual = max(tempo_atual, nao_chegados[0].chegada)

        # Adiciona à fila de prontos todos que chegaram até o instante atual
        while nao_chegados and nao_chegados[0].chegada <= tempo_atual:
            fila_prontos.append(nao_chegados.pop(0))

        # 2. Despacha o primeiro processo da fila
        p_atual = fila_prontos.pop(0)

        # 3. Troca de Contexto na tarefa que está ENTRANDO (C4: inclusive no 1º despacho)
        if p_atual.id != ultimo_processo_id and ctx_time > 0:
            p_atual.adicionar_troca_contexto(tempo_atual, tempo_atual + ctx_time)
            tempo_atual += ctx_time

        # 4. Executa até o limite do quantum
        tempo_rodar = min(p_atual.tempo_restante, quantum)
        p_atual.adicionar_processamento(tempo_atual, tempo_atual + tempo_rodar)
        tempo_atual += tempo_rodar

        # 5. Processos que chegaram durante a execução entram na fila antes da reinserção
        while nao_chegados and nao_chegados[0].chegada <= tempo_atual:
            fila_prontos.append(nao_chegados.pop(0))

        # 6. Se ainda resta tempo de execução, volta para o fim da fila de prontos
        if p_atual.tempo_restante > 0:
            fila_prontos.append(p_atual)

        ultimo_processo_id = p_atual.id

    # 7. Cálculo das métricas oficiais (C8: tw = tt - tp)
    if not processos:
        return 0, 0, "Round Robin"

    media_execucao = sum(p.get_turnaround() for p in processos) / len(processos)
    media_espera = sum(p.get_espera() for p in processos) / len(processos)

    return media_execucao, media_espera, "Round Robin"