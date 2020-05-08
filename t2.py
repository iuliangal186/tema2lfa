import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
from graphviz import Digraph

gfc = Digraph('finite_state_machine', filename='fsm.gv')
gfc.attr(rankdir = 'LR')

class NFA:
    def __init__(self):
        self.nr_stari = 0
        self.stari = []
        self.alf = []
        self.nr_stari_finale = 0
        self.stari_finale = []
        self.stare_start = 0
        self.functii_tran = []


    def print_nfa(self):
        print(self.nr_stari)
        print(self.stari)
        print(self.alf)
        print(self.nr_stari_finale)
        print(self.stari_finale)
        print(self.stare_start)
        print(self.functii_tran)

    def construct_nfa(self, lines):
        self.nr_stari = int(lines[0])
        init_stari = lines[1].split(" ")

        for i in range(0,len(init_stari)):
            if i == len(init_stari) - 1:
                c = init_stari[i]
                c = c.split()
                self.stari.append(c[0])
            else:
                self.stari.append(init_stari[i])

        self.alf = list(lines[2].strip())

        linie_stari_finale = lines[3].split(" ")
        for i in range(len(linie_stari_finale)):
            if i == 0:
                self.nr_stari_finale = int(linie_stari_finale[i])
            elif i == len(linie_stari_finale) - 1:
                k = linie_stari_finale[i]
                k = k.split()
                self.stari_finale.append(k[0])
            else:
                self.stari_finale.append(linie_stari_finale[i])

        st_st = lines[4]
        st_st = st_st.split()
        self.stare_start = st_st[0]

        for i in range(5, len(lines)):
            linie_tranzitie = lines[i].split(" ")

            k1 = linie_tranzitie[0]
            k2 = linie_tranzitie[1]
            k3_cpy = linie_tranzitie[2]
            k3_cpy = k3_cpy.split()
            k3 = k3_cpy[0]

            li = (k1, k2, k3)
            self.functii_tran.append(li)


class DFA:
    def __init__(self):
        self.nr_stari = 0
        self.stari = nfa.stari
        self.alf = []
        self.nr_stari_finale = 0
        self.stari_finale = []
        self.stare_start = 0
        self.functii_tran = []
        self.q = []

    def nfa_to_dfa(self, nfa):
        self.alf = nfa.alf
        self.stare_start = nfa.stare_start

        nfa_tran = {}
        dfa_tran = {}

        # combin tranzitiile nfa
        for t in nfa.functii_tran:
            start = t[0]
            mid = t[1]
            end = t[2]

            if(start, mid) in nfa_tran:
                nfa_tran[(start, mid)].append(end)
            else:
                nfa_tran[(start, mid)] = [end]

        self.q.append((self.stare_start,))

        # tranzitiile din nfa in dfa
        for i in self.q:
            for j in nfa.alf:
                if len(i) == 1 and (i[0], j) in nfa_tran:
                    dfa_tran[(i, j)] = nfa_tran[(i[0], j)]

                    if tuple(dfa_tran[(i, j)]) not in self.q:
                        self.q.append(tuple(dfa_tran[(i, j)]))

                else:
                    d = []
                    fd = []

                    for k in i:
                        if (k, j) in nfa_tran and nfa_tran[(k, j)] not in d:
                            d.append(nfa_tran[(k, j)])

                    if not d:
                        fd.append(None)
                    else:
                        for d1 in d:
                            for d2 in d1:
                                if d2 not in fd:
                                    fd.append(d2)

                    dfa_tran[(i, j)] = fd

                    if tuple(fd) not in self.q:
                        self.q.append(tuple(fd))

        # stari nfa la stari dfa

        for key in dfa_tran:
            self.functii_tran.append((self.stari[self.q.index(tuple(key[0]))], key[1], self.stari[self.q.index(tuple(dfa_tran[key]))]))


        for i in self.q:
            for j in nfa.stari_finale:
                if j in i:
                    self.stari_finale.append(j)
                    self.nr_stari_finale += 1


    def print_dfa(self):
        gfc.attr('node', style = 'invisible', shape = 'circle')
        fake = ' '
        gfc.node(fake)

        if self.stare_start in self.stari_finale:
            gfc.attr('node', style = '', shape = 'doublecircle', color = 'red')
        else:
            gfc.attr('node', style = '', shape = 'circle', color = 'red')

        gfc.edge(fake, self.stare_start, label = ' ', style = 'bold', color = 'red')

        gfc.attr('node', shape = 'doublecircle', color = 'green')

        for i in range(self.nr_stari_finale):
            gfc.node(self.stari_finale[i])

        gfc.attr('node', shape = 'circle', color = 'black')

        x = self.functii_tran[0]
        i = 1
        while i < len(self.functii_tran):
            gfc.edge(str(x[0]),str(x[2]), label = x[1], color = 'blue')
            x = self.functii_tran[i]
            i += 1

        gfc.view()
        print(self.functii_tran)
file = open("read", 'r')
lines = file.readlines()
file.close()


nfa = NFA()
dfa = DFA()

nfa.construct_nfa(lines)
dfa.nfa_to_dfa(nfa)

dfa.print_dfa()

