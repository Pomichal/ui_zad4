import json


class machine:

    def __init__(self):

        with open('rules.json') as data_file:
            data = json.load(data_file)
            pravidla = data["pravidla"]

        for k,v in pravidla.items():
            v = [list(map(lambda x: x.split(), x)) for x in v]
            pravidla[k] = v

        self.pravidla = pravidla
        # fakty = []
        fakty = [['Peter', 'rodic', 'Jano'],['manzelia', 'Peter', 'Eva'],['muz','Peter'],['zena','Eva'],['Peter','rodic','Sano']]

        # while True :
        #     text = input("zadat fakt (alebo 'x' pre vyhodnotenie): ")
        #     if text == 'x':
        #         break
        #     else:
        #         fakty.append(text.split())
        self.fakty = fakty

    def najdi_naviazania(self):
        nove = 1
        while nove == 1:
            nove = 0
            for meno, opis in self.pravidla.items():
                nove_pravidla = []
                premenne = self.vyhodnot_podmienky(opis[0],{})
                if premenne:
                    nove_pravidla.append(self.naviaz(premenne,opis[1]))
                nove_pravidla = self.filtruj(nove_pravidla)
                if nove_pravidla:
                    nove = 1
                    self.vykonaj(nove_pravidla)
        print(self.fakty)

    def vykonaj(self,pravidla):
        for akcia in pravidla:
            for i, pravidlo in enumerate(akcia):
                if pravidlo[0] == 'pridaj':
                    self.fakty.append(pravidlo[1:])
                elif pravidlo[0] == 'vymaz':
                    self.fakty.remove(pravidlo)
                elif pravidlo[0] == 'sprava':
                    print(' '.join(pravidlo[1:]))

    def vyhodnot_podmienky(self, podmien, premenne):
        podmienky = podmien.copy()
        if not podmienky:
            return premenne

        podmienka = podmienky[0]
        for fakt in self.fakty:
            tmp = 0
            if len(fakt) == len(podmienka):
                podm = [premenne[x] if x[0] == '?' and x in premenne else x for x in podmienka]
                for x in range(len(fakt)):
                    if podm[0] == '<>' and podm[1] == podm[2]:
                        tmp = 1
                        break
                    if podm[x][0] != '?' and podm[x] != fakt[x]:
                        if podmienka[x][0] == '?' and fakt[x][0].isupper():
                            return False
                        else:
                            tmp = 1
                            break
                    elif podm[x][0] == '?' and fakt[x][0].isupper():
                        premenne[podm[x]] = fakt[x]
                if tmp == 0:
                    if podmienka in podmienky:
                        podmienky.remove(podmienka)
                    premenne = self.vyhodnot_podmienky(podmienky, premenne)
                    if premenne:
                        return premenne
                    else:
                        premenne = {}
        return False

    def naviaz(self, premenne, akcie):
        nove_akcie = []
        for akcia in akcie:
            akc = akcia.copy()
            for i, slovo in enumerate(akcia):
                if slovo[0] == '?':
                    akc[i] = premenne[slovo]
            nove_akcie.append(akc)
        return nove_akcie

    def filtruj(self, pravidla):
        iba_vypis = 0
        for akcia in pravidla:
            for i, pravidlo in enumerate(akcia):
                iba_vypis = 0
                if pravidlo[0] == 'pridaj' and pravidlo[1:] in self.fakty:
                    akcia.remove(pravidlo)
                elif pravidlo[0] == 'vymaz' and pravidlo[1:] not in self.fakty:
                    akcia.remove(pravidlo)
                elif pravidlo[0] == 'sprava':
                    iba_vypis -= 1
                else:
                    iba_vypis += 1
            if not akcia or iba_vypis == 0:
                pravidla.remove(akcia)
        return pravidla


m = machine()
m.najdi_naviazania()
# m.akt_fakty()
# m.naviaz([["?X rodic ?Y","manzelia ?X ?Z"],["pridaj ?Z rodic ?Y"]])


