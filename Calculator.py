from bs4 import BeautifulSoup
import re

def getRatings():
    with open("page.htm", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    ratings_pattern = 'track_ratings.ratings\[(\d+)\].rating = (\d+);'

    ratingsArray = []
    
    for script_tag in soup.find_all('script'):
        script_content = script_tag.string
        if script_content and 'track_ratings' in script_content:
            matches = re.findall(ratings_pattern, script_content)
            for match in matches:
                index, rating = map(int, match)
                ratingsArray.append(rating)
    
    return ratingsArray

def extract_track_durations():
    with open("page.htm", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    durations = []
    for span in soup.find_all('span', {'class': 'tracklist_title'}):  # Encontra elementos com a classe "tracklist_title"
        if span.find('span', itemprop='name'):  # Verifica se existe um filho com o itemprop "name"
            duration_span = span.find('span', {'data-inseconds': True})  
            if duration_span:
                durations.append(int(duration_span['data-inseconds']))  # Extrai o valor se existir

    return durations

def calculate_and_print_results(lista1, lista2):
    """Calcula os resultados da multiplicação de elementos de duas listas e salva em arquivo.

    Args:
        lista1: A primeira lista de números.
        lista2: A segunda lista de números.
    """

    if len(lista1) != len(lista2):
        print("Erro: As listas devem ter o mesmo tamanho.")
        return

    soma_ponderada = 0
    soma_lista2 = 0
    expressao = ""
    for num1, num2 in zip(lista1, lista2):
        soma_ponderada += num1 * num2
        soma_lista2 += num2
        expressao += f"({num1}*{num2})+"

    expressao = expressao[:-1]  # Remove o último '+'

    with open("resultado.txt", "w") as f:  # Abre o arquivo em modo de escrita
        print(expressao, file=f)          # Escreve a expressão no arquivo
        print(soma_lista2, file=f)         # Escreve a soma de lista2 no arquivo
        print(soma_ponderada / soma_lista2, file=f)  # Escreve a média ponderada no arquivo

ratings = getRatings()
durations = extract_track_durations()
calculate_and_print_results(ratings, durations)