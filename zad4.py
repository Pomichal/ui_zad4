import json


class machine:

    def __init__(self,file,fakty,debug=0):
        with open(file) as data_file:
            data = json.load(data_file)
            pravidla = data["pravidla"]

        for k,v in pravidla.items():
            v = [list(map(lambda x: x.split(), x)) for x in v]
            pravidla[k] = v

        self.debug = debug
        self.pravidla = pravidla
        self.fakty = fakty

    def najdi_fakty(self):
        nove = -1
        while len(self.fakty) != nove:
            nove = len(self.fakty)
            for meno, opis in self.pravidla.items():
                self.vyhodnot_podmienky(opis[0],opis[1],{})
        print()
        print("Vsetky fakty:")
        list((print(' '.join(x)) for x in self.fakty))

    def vyhodnot_podmienky(self, podmien, akcie, premen):

        # ak nie su ziadne dalsie podmienky na vyhodnotenie, vykona akcie
        if not podmien:
            nove_pravidla = []
            nove_pravidla.append(self.naviaz(premen, akcie))
            nove_pravidla = self.filtruj(nove_pravidla)
            if nove_pravidla:
                self.vykonaj(nove_pravidla)
            return

        podmienka = podmien[0]  # pokusa sa splnit prvu podmienku, dosada kazdy fakt
        for fakt in self.fakty:
            podmienky = podmien.copy()
            premenne = premen.copy()
            tmp = 0
            if len(fakt) == len(podmienka) or podmienka[0] == '<>':
                podm = [premenne[x] if x[0] == '?' and x in premenne else x for x in podmienka]
                for x in range(len(fakt)):
                    if podm[0] == '<>' and podm[1] == podm[2]:
                        tmp = 1
                        break
                    elif podm[0] == '<>' and podm[1] != podm[2]:
                        tmp = 0
                    elif podm[x][0] != '?' and podm[x] != fakt[x]:
                        tmp = 1
                        break
                    elif podm[x][0] == '?':
                        premenne[podm[x]] = fakt[x]
                if tmp == 0:            #ak nasiel vhodne naviazanie podmienky, vnara sa do dalsej
                    self.vyhodnot_podmienky(podmienky[1:], akcie, premenne)

    #naviaze najdene premenne na premenne v akcii
    def naviaz(self, premenne, akcie):
        nove_akcie = []
        for akcia in akcie:
            akc = akcia.copy()
            for i, slovo in enumerate(akcia):
                if slovo[0] == '?':
                    akc[i] = premenne[slovo]
            nove_akcie.append(akc)
        return nove_akcie

    # odfiltrovanie akcii, ktore nema vyznam vykonat
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

    def vykonaj(self,pravidla):
        for akcia in pravidla:
            for i, pravidlo in enumerate(akcia):
                pravidlo = self.vyhodnot(pravidlo)

                #krokovanie vykonavania v debug rezime
                if self.debug == 1:
                    print("nove pravidlo: " + " ".join(pravidlo))
                    text = input("1- vsetky fakty, 2- dalsi krok, 3- do konca:")
                    print()
                    while text == "1":
                        list("vsetky fakty:")
                        list((print(' '.join(x)) for x in self.fakty))
                        print()
                        print("nove pravidlo: " + " ".join(pravidlo))
                        text = input("1- vsetky fakty, 2- dalsi krok, 3- do konca:")
                    if text == "3":
                        self.debug = 0

                if pravidlo[0] == 'pridaj':
                    self.fakty.append(pravidlo[1:])
                elif pravidlo[0] == 'vymaz':
                    self.fakty.remove(pravidlo[1:])
                elif pravidlo[0] == 'sprava':
                    print(' '.join(pravidlo[1:]))

    def vyhodnot(self,pravidlo):
        # zaciatky = [index for index, value in enumerate(pravidlo) if value == '{']
        # konce = [index for index, value in enumerate(pravidlo) if value == '}']
        nove_pravidlo = pravidlo
        while '{' in nove_pravidlo:
            zaciatok = nove_pravidlo.index('{')
            koniec = nove_pravidlo.index('}')
            # print(nove_pravidlo[:zaciatok])
            # print(nove_pravidlo[zaciatok + 1:koniec])
            # print(" ".join(nove_pravidlo[zaciatok + 1:koniec]))
            # print(nove_pravidlo[koniec + 1:])
            vysledok = eval(" ".join(nove_pravidlo[zaciatok + 1:koniec]))
            # print(vysledok)
            # vysledok = eval(" ".join(pravidlo[zaciatok + 1:koniec]))
            nove_pravidlo = nove_pravidlo[:zaciatok] + [str(vysledok)] + nove_pravidlo[koniec + 1:]
        return nove_pravidlo
        # nove_pravidlo = []
        # while '{' in pravidlo:
        #     zaciatok= pravidlo.index('{')
        #     koniec = pravidlo.index('}')
        #     print(pravidlo[:zaciatok -1])
        #     print(pravidlo[zaciatok + 1:koniec])
        #     print(" ".join(pravidlo[zaciatok + 1:koniec]))
        #     print(pravidlo[koniec + 1:])
        #     vysledok = eval(" ".join(pravidlo[zaciatok + 1:koniec]))
        #     print(vysledok)
        #     nove_pravidlo = pravidlo[:zaciatok -1] + [str(vysledok)] + pravidlo[koniec + 1:]
        # return pravidlo


# fakty = []
# while True :
#     text = input("zadat fakt (alebo 'x' pre vyhodnotenie): ")
#     if text == 'x':
#         break
#     else:
#         fakty.append(text.split())
# fakty = [['Peter','rodic','Jano'],['Peter','rodic','Vlado'],['manzelia','Peter','Eva'],['Vlado','rodic','Maria'],
#                  ['Vlado','rodic','Viera'],['muz','Peter'],['muz','Jano'],['muz','Vlado'],['zena','Maria'],
#                  ['zena','Viera'],['zena','Eva']]
# fakty = [['typ','karoserie','sedan'],['pocet','dveri','4'],['pohanana','naprava','predna'],['predna','maska','mriezka'],
#          ['ma', 'okruhle', 'svetla'],['karoseria','sedan'],['sedan','4'],['naprava', 'predna']]
# m = machine('fiaty.json',fakty,debug=0)
fakty = [['faktorial','2']]
m = machine('faktorial.json',fakty,debug=0)
m.najdi_fakty()


