import heapq, math, random, yaml
from collections import defaultdict

class LimiteAleatorios(Exception): pass
class Gerador:
    def __init__(self, semente, limite): self.rng=random.Random(semente); self.limite=limite; self.usados=0
    def uniforme(self,a,b):
        if self.usados >= self.limite: raise LimiteAleatorios
        self.usados += 1
        return a + (b-a)*self.rng.random()

class Fila:
    def __init__(self, cfg):
        self.nome=cfg['nome']; self.servidores=cfg['servidores']; self.capacidade=cfg.get('capacidade')
        self.servico=tuple(cfg['servico']); self.rotas=cfg['rotas']
        self.n=0; self.ocupados=0; self.perdas=0; self.tempos=defaultdict(float)
    def cheia(self): return self.capacidade is not None and self.n >= self.capacidade

class Simulador:
    def __init__(self,cfg):
        self.g=Gerador(cfg.get('semente',1),cfg['aleatorios'])
        self.filas=[Fila(x) for x in cfg['filas']]; self.eventos=[]; self.seq=0; self.tempo=0.0
        self.primeira_chegada=cfg['primeira_chegada']; self.chegadas=tuple(cfg['chegadas'])
    def agenda(self,tipo,fila,tempo): heapq.heappush(self.eventos,(tempo,self.seq,tipo,fila)); self.seq+=1
    def inicia_servico(self,i):
        f=self.filas[i]; f.ocupados+=1; self.agenda('saida',i,self.tempo+self.g.uniforme(*f.servico))
    def entra(self,i):
        f=self.filas[i]
        if f.cheia(): f.perdas+=1; return
        f.n+=1
        if f.ocupados < f.servidores: self.inicia_servico(i)
    def roteia(self,i):
        r=self.g.uniforme(0.0,1.0); soma=0.0
        for rota in self.filas[i].rotas:
            soma += rota['p']
            if r < soma:
                if rota['destino'] != -1: self.entra(rota['destino'])
                return
        raise ValueError('Probabilidades de roteamento devem somar 1.')
    def executa(self):
        self.agenda('chegada',0,self.primeira_chegada)
        try:
            while self.eventos:
                t,_,tipo,i=heapq.heappop(self.eventos)
                dt=t-self.tempo
                for f in self.filas: f.tempos[f.n]+=dt
                self.tempo=t
                if tipo=='chegada':
                    self.agenda('chegada',0,self.tempo+self.g.uniforme(*self.chegadas)); self.entra(0)
                else:
                    f=self.filas[i]; f.n-=1; f.ocupados-=1
                    if f.n > f.ocupados: self.inicia_servico(i)
                    self.roteia(i)
        except LimiteAleatorios:
            pass
        return self
    def relatorio(self):
        print(f'Aleatorios utilizados: {self.g.usados}')
        for i,f in enumerate(self.filas,1):
            print(f'\nFILA {i} - {f.nome}')
            print('Estado\tTempo acumulado\tProbabilidade')
            for estado in sorted(f.tempos):
                tempo=f.tempos[estado]; print(f'{estado}\t{tempo:.4f}\t{100*tempo/self.tempo:.4f}%')
            print('Perdas:',f.perdas)
        print(f'\nTempo global da simulacao: {self.tempo:.4f} minutos')

def main():
    with open('modelo.yml',encoding='utf-8') as arq: cfg=yaml.safe_load(arq)
    Simulador(cfg).executa().relatorio()
if __name__=='__main__': main()
