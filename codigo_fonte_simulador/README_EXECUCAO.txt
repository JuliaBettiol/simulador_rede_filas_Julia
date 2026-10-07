SIMULADOR PARA REDE DE FILAS - INSTRUCOES

Arquivos:
- simulador_rede_filas.py : codigo-fonte
- modelo.yml              : dados de entrada do modelo

Requisitos:
- Python 3.10 ou superior
- PyYAML

Instalacao da dependencia:
  pip install pyyaml

Execucao:
  python simulador_rede_filas.py

Configuracao usada na validacao:
- semente: 1
- 100.000 numeros pseudoaleatorios
- primeira chegada no tempo 2,0 min
- Fila 1: G/G/1; chegada U(2,4); servico U(1,2)
- Fila 2: G/G/2/5; servico U(4,6)
- Fila 3: G/G/2/10; servico U(5,15)
- roteamento: F1->F2 0,2; F1->F3 0,8; F2->F1 0,3; F2->fora 0,2; F2->F3 0,5; F3->F1 0,7; F3->fora 0,3.

Observacao: a simulacao termina imediatamente quando o 100.000o numero pseudoaleatorio e solicitado/utilizado, conforme o enunciado.
