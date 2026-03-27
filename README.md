# Contador de Palavras

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Licenca: MIT](https://img.shields.io/badge/Licenca-MIT-green)](https://opensource.org/licenses/MIT)

Projeto em Python para analisar um arquivo de texto e mostrar:

- o numero total de palavras;
- as 10 palavras mais frequentes com suas contagens.

O script ignora diferencas entre maiusculas e minusculas e desconsidera pontuacao na separacao das palavras.

## Funcionalidades

- Leitura de arquivos de texto (`.txt` e similares) com codificacao UTF-8
- Suporte a arquivos `.docx` (quando `python-docx` estiver instalado)
- Normalizacao do texto para minusculas
- Extracao de palavras com expressao regular
- Remocao de stopwords comuns (palavras muito frequentes sem valor semantico)
- Exibicao do ranking com tamanho configuravel via argumento `--top`
- Exportacao opcional do resultado em CSV ou JSON
- Tratamento de erros comuns (arquivo nao encontrado, codificacao invalida e dependencia ausente)

## Estrutura

- `contador.py`: script principal com as funcoes de leitura, processamento e exibicao.

## Autor

- Moacir

## Repositorio

- URL: `https://github.com/moacirrochadev/contador_de_palavras`

## Requisitos

- Python 3.10+ (recomendado 3.12)
- Opcional para `.docx`: `python-docx`

## Instalacao

Clone o repositorio e entre na pasta do projeto:

```bash
git clone <https://github.com/moacirrochadev/contador_de_palavras>
cd curso-python/contador_de_palavras
```

Opcional: crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale a dependencia para ler arquivos `.docx`:

```bash
pip install python-docx
```

## Como executar

```bash
python3 contador.py
```

Exibindo, por exemplo, o top 20:

```bash
python3 contador.py --top 20
```

Depois, informe o caminho completo do arquivo quando solicitado.

Ao final, voce pode exportar o resultado digitando:

- `csv` para gerar `resultado_contagem.csv`
- `json` para gerar `resultado_contagem.json`
- `nao` para apenas exibir no terminal

Exemplo:

```text
Digite o caminho para o arquivo de texto: /home/usuario/Documentos/texto.txt
Numero total de palavras: 245

Top 10 palavras mais frequentes:
python: 14
dados: 10
...
```

## Tratamento de erros

O programa informa de forma amigavel quando:

- o arquivo nao existe;
- o arquivo de texto nao pode ser lido como UTF-8;
- o arquivo eh `.docx`, mas `python-docx` nao esta instalado.

## Licenca

Este projeto esta sob a licenca MIT.
