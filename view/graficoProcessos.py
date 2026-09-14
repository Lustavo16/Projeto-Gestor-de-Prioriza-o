import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk

def centralizar_grafico(fig):
    janela_temporaria = tk.Tk()
    janela_temporaria.withdraw()

    largura_tela = janela_temporaria.winfo_screenwidth()
    altura_tela = janela_temporaria.winfo_screenheight()

    largura_janela = fig.canvas.manager.window.winfo_width()
    altura_janela = fig.canvas.manager.window.winfo_height()

    pos_x = (largura_tela // 2) - int(1.5 * largura_janela)
    pos_y = (altura_tela // 2) - int(1.5 * altura_janela)

    fig.canvas.manager.window.wm_geometry(f"+{pos_x}+{pos_y}")
    janela_temporaria.destroy()

def grafico_processos(processos, media_execucao, media_espera, nome_processo):
    fig, ax = plt.subplots(figsize=(14, 6))
    plt.subplots_adjust(left=0.1, right=0.82, bottom=0.15, top=0.9)
    
    fig.canvas.manager.set_window_title('Gráfico de Escalonamento')
    
    todos_fins = [p.fim for proc in processos for p in proc.processamentos]
    tempo_maximo = max(todos_fins) if todos_fins else 1
    ax.set_xlim(0, tempo_maximo)
    
    # Eixo X com marcas inteiras conforme convenção C1
    ax.set_xticks(range(0, int(tempo_maximo) + 1))
    ax.set_yticks(range(1, len(processos) + 1))
    ax.set_yticklabels([f"t{p.id}" for p in processos])

    for processo in processos:
        tempo_util_acumulado = 0

        for periodo in processo.processamentos:
            duracao = periodo.fim - periodo.inicio
            
            if periodo.tipo == "Execução":
                # Bloco de execução normal (Azul)
                ax.barh(processo.id, duracao, left=periodo.inicio, height=0.6, color='#1E90FF', edgecolor='#1E90FF')

                # Marca a seção crítica com barra superior vermelha se estiver na posse do recurso (C7)
                if getattr(processo, 'sc_inicio', None) is not None:
                    fim_util = tempo_util_acumulado + duracao
                    inter_inicio = max(tempo_util_acumulado, processo.sc_inicio)
                    inter_fim = min(fim_util, processo.sc_fim)
                    
                    if inter_inicio < inter_fim:
                        desloc_inicio = inter_inicio - tempo_util_acumulado
                        largura_sc = inter_fim - inter_inicio
                        # Traço vermelho no topo da barra (página 6 do PDF)
                        ax.barh(processo.id + 0.32, largura_sc, left=periodo.inicio + desloc_inicio, 
                                height=0.06, color='#B22222', edgecolor='#B22222')

                tempo_util_acumulado += duracao

            elif periodo.tipo == "CTX":
                ax.barh(processo.id, duracao, left=periodo.inicio, height=0.6, color='#FFD700', edgecolor='#DAA520')
                ax.text(periodo.inicio + duracao/2, processo.id, 'CTX', ha='center', va='center', fontsize=7)

        # Preenchimento dos intervalos de espera (vermelho suave)
        if processo.processamentos:
            tempo_ponteiro = processo.chegada
            for periodo in processo.processamentos:
                if periodo.inicio > tempo_ponteiro:
                    duracao_espera = periodo.inicio - tempo_ponteiro
                    ax.barh(processo.id, duracao_espera, left=tempo_ponteiro, height=0.6, 
                            color='#FF6347', alpha=0.35, edgecolor='#FF6347')
                tempo_ponteiro = periodo.fim

        # Textos informativos à direita
        espera = processo.get_espera()
        turnaround = processo.get_turnaround()
        ax.text(tempo_maximo + 0.3, processo.id, f"Tt: {turnaround:.1f} | Tw: {espera:.1f}", va='center', fontsize=9)

    ax.set_xlabel('Tempo (unidades discretas)')
    ax.set_title(nome_processo, fontsize=14, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    # Legendas
    p_exec = mpatches.Patch(color='#1E90FF', label=f'Execução (Tt médio = {media_execucao:.2f})')
    p_esp = mpatches.Patch(color='#FF6347', alpha=0.5, label=f'Espera (Tw médio = {media_espera:.2f})')
    p_ctx = mpatches.Patch(color='#FFD700', label='Troca de Contexto')
    p_sc = mpatches.Patch(color='#B22222', label='Posse de Recurso (Seção Crítica)')
    
    ax.legend(handles=[p_exec, p_esp, p_ctx, p_sc], loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=4)

    centralizar_grafico(fig)
    plt.show()