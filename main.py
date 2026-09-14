from view import criar_janela
#from control.gerador_cenarios.gerador_lotes import executar_lote
#from control.simular_escalonamento import simular_escalonamento
#import copy

if __name__ == "__main__":
    criar_janela()

    if False:
        cenario = executar_lote(5)

        print("\nCENÁRIO:")
        for p in cenario:
            print(
                f"ID={p.id} | chegada={p.chegada} | "
                f"duração={p.duracao} | prioridade={p.prioridade}"
            )

        resultado = simular_escalonamento(
            copy.deepcopy(cenario),
            1,
            2,
            0,
            0
        )

        print("\nRESULTADO:")
        print(resultado)

    if False:
        resultados = executar_lote(
            quantidade_cenarios=50,
            quantidade_tarefas=5
        )

        for algoritmo, resultado in resultados.items():
            print(f"\n{resultado['nome']}")
            print(f"Turnaround médio: {resultado['turnaround_medio']:.2f}")
            print(f"Espera média: {resultado['espera_media']:.2f}")
