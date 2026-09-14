import tkinter as tk
from tkinter import messagebox


def configurar_tela_lotes(janela):

    titulo = tk.Label(
        janela,
        text="Simulação em Lotes",
        font=("Arial", 16, "bold")
    )
    titulo.pack(pady=15)

    frame_parametros = tk.Frame(janela)
    frame_parametros.pack(pady=10)

    # Quantidade de cenários
    tk.Label(
        frame_parametros,
        text="Quantidade de cenários:"
    ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

    entrada_cenarios = tk.Entry(frame_parametros, width=10)
    entrada_cenarios.insert(0, "50")
    entrada_cenarios.grid(row=0, column=1, padx=10, pady=8)

    # Quantidade de tarefas
    tk.Label(
        frame_parametros,
        text="Tarefas por cenário:"
    ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

    entrada_tarefas = tk.Entry(frame_parametros, width=10)
    entrada_tarefas.insert(0, "5")
    entrada_tarefas.grid(row=1, column=1, padx=10, pady=8)

    # Quantum
    tk.Label(
        frame_parametros,
        text="Quantum:"
    ).grid(row=2, column=0, padx=10, pady=8, sticky="w")

    entrada_quantum = tk.Entry(frame_parametros, width=10)
    entrada_quantum.insert(0, "2")
    entrada_quantum.grid(row=2, column=1, padx=10, pady=8)

    # Chegada máxima
    tk.Label(
        frame_parametros,
        text="Chegada máxima:"
    ).grid(row=3, column=0, padx=10, pady=8, sticky="w")

    entrada_chegada_max = tk.Entry(frame_parametros, width=10)
    entrada_chegada_max.insert(0, "8")
    entrada_chegada_max.grid(row=3, column=1, padx=10, pady=8)

    # Duração máxima
    tk.Label(
        frame_parametros,
        text="Duração máxima:"
    ).grid(row=4, column=0, padx=10, pady=8, sticky="w")

    entrada_duracao_max = tk.Entry(frame_parametros, width=10)
    entrada_duracao_max.insert(0, "6")
    entrada_duracao_max.grid(row=4, column=1, padx=10, pady=8)

    # Prioridade máxima
    tk.Label(
        frame_parametros,
        text="Prioridade máxima:"
    ).grid(row=5, column=0, padx=10, pady=8, sticky="w")

    entrada_prioridade_max = tk.Entry(frame_parametros, width=10)
    entrada_prioridade_max.insert(0, "5")
    entrada_prioridade_max.grid(row=5, column=1, padx=10, pady=8)

    def executar():
        try:
            quantidade_cenarios = int(entrada_cenarios.get())
            quantidade_tarefas = int(entrada_tarefas.get())
            quantum = int(entrada_quantum.get())
            chegada_max = int(entrada_chegada_max.get())
            duracao_max = int(entrada_duracao_max.get())
            prioridade_max = int(entrada_prioridade_max.get())

            if quantidade_cenarios <= 0:
                raise ValueError("A quantidade de cenários deve ser maior que zero.")

            if quantidade_tarefas <= 0:
                raise ValueError("A quantidade de tarefas deve ser maior que zero.")

            if quantum <= 0:
                raise ValueError("O quantum deve ser maior que zero.")

            if chegada_max < 0:
                raise ValueError("A chegada máxima não pode ser negativa.")

            if duracao_max <= 0:
                raise ValueError("A duração máxima deve ser maior que zero.")

            if prioridade_max <= 0:
                raise ValueError("A prioridade máxima deve ser maior que zero.")

            messagebox.showinfo(
                "Configuração",
                "Parâmetros válidos!\n\n"
                f"Cenários: {quantidade_cenarios}\n"
                f"Tarefas por cenário: {quantidade_tarefas}\n"
                f"Quantum: {quantum}\n"
                f"Chegada máxima: {chegada_max}\n"
                f"Duração máxima: {duracao_max}\n"
                f"Prioridade máxima: {prioridade_max}"
            )

        except ValueError as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    botao_executar = tk.Button(
        janela,
        text="Executar lote",
        command=executar,
        width=20
    )
    botao_executar.pack(pady=20)