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
        fakty = [['Peter', 'rodic', 'Jano'],['manzelia', 'Peter', 'Eva']]

        # while True :
        #     text = input("zadat fakt (alebo 'x' pre vyhodnotenie): ")
        #     if text == 'x':
        #         break
        #     else:
        #         fakty.append(text.split())
        self.fakty = fakty

    def najdi_naviazania(self):
        nove_pravidla = []
        for meno, opis in self.pravidla.items():
            premenne = self.vyhodnot_podmienky(opis[0],{})
            if premenne:
                nove_pravidla.append(self.naviaz(premenne,opis[1]))
        # print(nove_fakty)
        nove_pravidla = self.filtruj(nove_pravidla)

        if nove_pravidla:
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
                    print(pravidlo[1:])

    def vyhodnot_podmienky(self, podmienky, premenne):
        if not podmienky:
            return premenne

        podmienka = podmienky[0]

        for fakt in self.fakty:
            if len(fakt) == len(podmienka):
                lokal = premenne.copy()
                podm = [lokal[x] if x[0] == '?' and x in lokal else x for x in podmienka]
                for x in range(len(fakt)):
                    if podm[x][0] != '?' and podm[x] != fakt[x]:
                        if podmienka[x][0] == '?' and fakt[x][0].isupper():
                            return False
                        else:
                            lokal = {}
                            break
                    elif podm[x][0] == '?' and fakt[x][0].isupper():
                        # if podm[x] in premenne and premenne[podm[x]] != fakt[x]:
                        #     break
                        # else:
                        lokal[podm[x]] = fakt[x]
                        # print(podm[x],fakt[x])
                premenne = {**premenne, **lokal}
                        # print(podmienka[x],fakt[x])
                    # elif podm[x] != fakt[x]:
                    #     break
        podmienky.remove(podmienka)
        return self.vyhodnot_podmienky(podmienky,premenne)

    def naviaz(self, premenne, akcie):
        nove_akcie = []
        for akcia in akcie:
            for i, slovo in enumerate(akcia):
                if slovo[0] == '?':
                    akcia[i] = premenne[slovo]
            nove_akcie.append(akcia)
        return nove_akcie

    def filtruj(self, pravidla):
        iba_vypis = 0
        for akcia in pravidla:
            for i, pravidlo in enumerate(akcia):
                iba_vypis = 0
                # print(pravidlo)
                # print(pravidlo[1:])
                # print(self.fakty)
                if pravidlo[0] == 'pridaj' and pravidlo[1:] in self.fakty:
                    akcia.remove(pravidlo)
                elif pravidlo[0] == 'vymaz' and pravidlo[1:] not in self.fakty:
                    akcia.remove(pravidlo)
                elif pravidlo[0] == 'sprava':
                    iba_vypis = 1
                else:
                    iba_vypis = 0
            if not akcia or iba_vypis == 1:
                pravidla.remove(akcia)
        return pravidla

        # for podmienka in podmienky:
        #     print(1)


m = machine()
m.najdi_naviazania()
# m.akt_fakty()
# m.naviaz([["?X rodic ?Y","manzelia ?X ?Z"],["pridaj ?Z rodic ?Y"]])


