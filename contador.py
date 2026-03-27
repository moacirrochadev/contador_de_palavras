import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "a", "as", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo",
    "com", "como", "da", "das", "de", "dela", "delas", "dele", "deles", "depois",
    "do", "dos", "e", "ela", "elas", "ele", "eles", "em", "entre", "era", "eram",
    "essa", "essas", "esse", "esses", "esta", "estas", "este", "estes", "eu", "foi",
    "foram", "ha", "isso", "isto", "ja", "la", "mais", "mas", "me", "mesmo", "meu",
    "meus", "minha", "minhas", "muito", "na", "nas", "nao", "nem", "no", "nos",
    "nossa", "nossas", "nosso", "nossos", "num", "numa", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "qual", "quando", "que", "quem", "se",
    "sem", "ser", "seu", "seus", "sua", "suas", "tambem", "te", "tem", "tendo",
    "ter", "teve", "tipo", "tu", "um", "uma", "voces", "vos",
}


def ler_conteudo(caminho_arquivo: Path) -> str:
    """Lê conteúdo de arquivo .txt (ou texto) e .docx."""
    if caminho_arquivo.suffix.lower() == ".docx":
        try:
            from docx import Document  # pyright: ignore[reportMissingImports]
        except ImportError:
            raise RuntimeError(
                "Para ler arquivos .docx, instale: pip install python-docx"
            ) from None

        documento = Document(str(caminho_arquivo))
        return "\n".join(paragrafo.text for paragrafo in documento.paragraphs)

    with caminho_arquivo.open("r", encoding="utf-8") as arquivo_texto:
        return arquivo_texto.read()


def extrair_palavras(texto: str) -> list[str]:
    """Extrai palavras sem números e remove stopwords comuns."""
    tokens = re.findall(r"\w+", texto.lower())
    return [token for token in tokens if token.isalpha() and token not in STOPWORDS]


def exibir_top_palavras(palavras: list[str], limite: int = 10) -> None:
    frequencias = Counter(palavras)
    mais_frequentes = frequencias.most_common(limite)

    print(f"Número total de palavras: {len(palavras)}")
    print(f"\nTop {limite} palavras mais frequentes:")
    for palavra, contagem in mais_frequentes:
        print(f"{palavra}: {contagem}")


def exportar_csv(caminho_saida: Path, frequencias: Counter[str]) -> None:
    with caminho_saida.open("w", newline="", encoding="utf-8") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["palavra", "contagem"])
        for palavra, contagem in frequencias.most_common():
            writer.writerow([palavra, contagem])


def exportar_json(caminho_saida: Path, frequencias: Counter[str]) -> None:
    dados = [{"palavra": palavra, "contagem": contagem} for palavra, contagem in frequencias.most_common()]
    with caminho_saida.open("w", encoding="utf-8") as arquivo_json:
        json.dump(dados, arquivo_json, ensure_ascii=False, indent=2)


def perguntar_exportacao(frequencias: Counter[str]) -> None:
    resposta = input("\nDeseja exportar o resultado? (csv/json/nao): ").strip().lower()

    if resposta == "csv":
        caminho_saida = Path("resultado_contagem.csv")
        exportar_csv(caminho_saida, frequencias)
        print(f"Resultado exportado em: {caminho_saida.resolve()}")
        return

    if resposta == "json":
        caminho_saida = Path("resultado_contagem.json")
        exportar_json(caminho_saida, frequencias)
        print(f"Resultado exportado em: {caminho_saida.resolve()}")
        return

    if resposta in {"nao", "não", "n"}:
        print("Exportação não realizada.")
        return

    print("Opção inválida. Use: csv, json ou nao.")


def obter_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Conta palavras e exibe as mais frequentes em um arquivo."
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Quantidade de palavras mais frequentes para exibir (padrao: 10).",
    )
    return parser.parse_args()


def main() -> None:
    args = obter_argumentos()
    if args.top <= 0:
        print("O valor de --top deve ser maior que zero.")
        sys.exit(1)

    caminho_informado = input("Digite o caminho para o arquivo de texto: ").strip()
    caminho_arquivo = Path(caminho_informado).expanduser()

    if not caminho_arquivo.exists():
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        sys.exit(1)

    try:
        conteudo = ler_conteudo(caminho_arquivo)
    except RuntimeError as erro:
        print(erro)
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            "Não foi possível decodificar o arquivo como UTF-8. "
            "Use um arquivo de texto UTF-8 ou um .docx."
        )
        sys.exit(1)

    palavras = extrair_palavras(conteudo)
    exibir_top_palavras(palavras, limite=args.top)
    frequencias = Counter(palavras)
    perguntar_exportacao(frequencias)


if __name__ == "__main__":
    main()