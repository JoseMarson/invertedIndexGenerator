# README

## Projeto: Modelo Booleano para Recuperção de Informação

Este projeto implementa um gerador de índice invertido e um modelo booleano de recuperação de informação em Python, usando a biblioteca SpaCy para processamento de linguagem natural, como lematização e remoção de stopwords.

Este projeto foi desenvolvido por **José Vitor Oliveira Marson** para cumprimento de um trabalho da disciplina de Organização e Recuperação de Informações, ministrado pelo professor Wendel Alexandre Xavier de Melo. 

### Requisitos de instalação

Antes de executar o código, certifique-se de instalar as seguintes bibliotecas Python:

1. **SpaCy**: biblioteca para processamento de linguagem natural
   ```bash
   py -m pip install -U spacy

2. **spacy-lookups-data**: necessário para suportar a lematização em múltiplos idiomas
    ```bash
    pip install -U spacy-lookups-data

3. **pt_core_news_lg**: modelo de linguagem do português utilizado pelo SpaCy

    ```bash
    python -m spacy download pt_core_news_lg

### Como Executar

Execute o programa da seguinte forma:

1. **Abra um terminal**: abra um terminal na pasta do repositorio que você clonou.
2. **Seleção da base**: Selecione um arquivo que contenha os caminhos para os arquivos que compõem a base de documentos.
3. **Seleção de consultas**: Selecione um arquivo que possua a consulta a ser respondida pelo sistema de RI, escrita em uma
única linha
4. **Entrada no terminal**: A linha de entrada no terminal deve ser no seguinte modelo: 
    ```bash
    python modelo_booleano.py baseSelecionada.txt consultaSelecionada.txt
5. **O que esperar**: Após a execussão, o índice invertido será gerado no arquivo index.txt, e o resultado da consulta será gravado no arquivo resposta.txt.