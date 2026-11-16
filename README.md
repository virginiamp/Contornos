# Contornos

Aplicativo com interface gráfica que transforma uma imagem na sua versão apenas com linhas de contorno, usando o detector de bordas Canny do OpenCV.

Autora: Virginia Martins Perozim

## Requisitos

- Python 3 (testado com Python 3.12) com Tkinter. O instalador oficial do Python para Windows já inclui o Tkinter.
- Bibliotecas `opencv-python`, `numpy` e `pillow`, listadas em `requirements.txt`.

## Instalação

Na pasta do projeto, crie um ambiente virtual e instale as dependências.

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

No Linux ou macOS:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Como rodar

No Windows (PowerShell):

```powershell
.\.venv\Scripts\python.exe contornos.py
```

No Linux ou macOS:

```bash
.venv/bin/python contornos.py
```

O programa pode ser iniciado a partir de qualquer pasta, desde que o caminho para `contornos.py` esteja correto.

## Como usar

1. **Arquivo > Abrir...** e escolha uma imagem.
2. Opcional: **Ferramentas > Redimensionar...** para mudar o tamanho da imagem (de 1% a 1000%). Isso precisa ser feito antes de aplicar o filtro.
3. **Ferramentas > Filtro Colorido** (linhas coloridas sobre fundo preto) ou **Ferramentas > Filtro Preto e Branco** (linhas pretas sobre fundo branco).
4. Ajuste as barras **gradiente mínimo** e **gradiente máximo**. Quanto mais para a direita, menos linhas aparecem.
5. **Arquivo > Salvar como...** para gravar o resultado em PNG ou BMP.

**Ferramentas > Desfazer** volta para a imagem original. A ajuda completa está em **Ajuda > Sobre**.

## Arquivos

- `contornos.py`: o programa.
- `ajuda_texto.py`: o texto da janela de Ajuda. Para alterar a ajuda, edite esse arquivo. As marcações de formatação estão explicadas no início dele.
- `requirements.txt`: as bibliotecas necessárias.
