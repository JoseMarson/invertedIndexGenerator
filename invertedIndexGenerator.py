import spacy
import sys
import os
from collections import defaultdict

nlp = spacy.load("pt_core_news_lg")
caminho= r"C:\Users\José Vitor Marson\Desktop\QuintoPeriodo\ORI"

def prepareDocs(text):
    doc = nlp(text.lower())
    terms = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return terms

def openDocs(base):
    filePath = []
    try:
        with open(base, 'r') as arquivo:
            for linha in arquivo:
                caminho = linha.strip() 
                if caminho:
                    filePath.append(caminho)
        return filePath
    except FileNotFoundError as e:
        print("Não foi possível abrir o arquivo. " + str(e))

        sys.exit(1)

def generateInvertedIndex(documentos):
    indice_invertido = defaultdict(lambda: defaultdict(int))

    for i, arquivo in enumerate(documentos, 1):
        with open(arquivo, 'r') as doc:
            termos = prepareDocs(doc.read())
            for termo in termos:
                indice_invertido[termo][i] += 1

    try:
        with open("indice.txt", 'w') as f:
            for termo, docs in sorted(indice_invertido.items()):
                doc_str = " ".join([f"{doc_id},{count}" for doc_id, count in docs.items()])
                f.write(f"{termo}: {doc_str}\n")
    except IOError as e:
        print(f"Error writing to file {e}")

    return indice_invertido

def processInquiry(consulta, indice):
    def apply_not(operando):
        todos_docs = set().union(*[set(docs.keys()) for docs in indice.values()])
        return todos_docs - operando

    def apply_and(operando1, operando2):
        return operando1.intersection(operando2)

    def apply_or(operando1, operando2):
        return operando1.union(operando2)

    def get_docs(termo):
        termo = termo.lower()
        if termo in indice:
            return set(indice[termo].keys())
        return set()

    termos = consulta.split()
    
    i = 0
    while i < len(termos):
        if termos[i] == "!":
            termo = termos.pop(i + 1)
            docs = get_docs(termo)
            termos[i] = apply_not(docs)
        else:
            if termos[i] not in ["&", "|"]:
                termos[i] = get_docs(termos[i])
            i += 1

    i = 0
    while i < len(termos):
        if termos[i] == "&":
            left = termos.pop(i - 1)
            termos.pop(i - 1)
            right = termos.pop(i - 1)
            termos.insert(i - 1, apply_and(left, right))
        else:
            i += 1

    i = 0
    while i < len(termos):
        if termos[i] == "|":
            left = termos.pop(i - 1)
            termos.pop(i - 1)
            right = termos.pop(i - 1)
            termos.insert(i - 1, apply_or(left, right))
        else:
            i += 1

    return termos[0] if termos else set()

def writeReply(resultado, documentos):
    with open("resposta.txt", 'w') as f:
        total_documentos = len(resultado)
        f.write(f"{total_documentos}\n") 

        for doc_id in sorted(resultado):
            nome_arquivo = os.path.basename(documentos[doc_id - 1])  
            f.write(f"{nome_arquivo}\n") 


def main():
    print("\n====================WELCOME TO THE INVERTED INDEX GENERATOR====================")
    print("\n=============================BY: JOSE VITOR MARSON=============================")

    if len(sys.argv) != 3:
        sys.exit(1)

    arquivo_base = sys.argv[1]  
    arquivo_consulta = sys.argv[2]  

    print("\n==============================SEARCHING DOCUMENTS==============================")
    documentos = openDocs(os.path.join(caminho, arquivo_base))
    if not documentos:
        print("\nNo documents were located.")
        sys.exit(1)
    print("\nThe documents were located.")
    print("\nGenerating inverted index...")
    inverted_index = generateInvertedIndex(documentos)
    print("\nInverted index generated.")
    print("\n==============================PROCESSING QUERY==============================")
    try:
        with open(os.path.join(caminho, arquivo_consulta), 'r') as f:
            consulta = f.read().strip()  
        resultado = processInquiry(consulta, inverted_index)
        print("\nQuery processed.")
    except FileNotFoundError:
        print(f"Error: Query File {arquivo_consulta} not found.")
        sys.exit(1)

    writeReply(resultado,documentos)
    print("\nThe answer was written in the file resposta.txt.")


if __name__ == "__main__":
    main()
