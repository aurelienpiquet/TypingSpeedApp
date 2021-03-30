import os, random

CUR_dir = os.path.dirname(os.path.abspath(__file__))    
dictionnary_url = os.path.join(CUR_dir, 'resources/en-basic.json')

class Dictionnary():
    def __init__(self, size):
        self.size = size
        self.liste_random = []
        self.string_random = ""

    def open_txt(self):
        with open(dictionnary_url, 'r') as f:
            data = f.readlines()
            data_cleared = [elm[:-1] for elm in data]
            return data_cleared

    def random_list_word(self):
        liste_word = self.open_txt()
        self.liste_random = [random.choice(liste_word) for i in range(0,self.size)]
        return self.liste_random

  


if __name__ == '__main__':

    dictionnaire = Dictionnary(size=10)
    a = dictionnaire.random_list_word()
    print(a)

    # crée un regex de chaque element en format liste
    # crée un cursor pour montrer l'avancement dans la liste_word
    

