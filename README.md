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

## Histórico de versões

### 1.1

Correções:

- Abrir e salvar imagens em pastas com acento ou ç (por exemplo, "Área de Trabalho") agora funciona.
- Cancelar a janela de **Abrir...** não mostra mais a mensagem "ERRO #0".
- **Salvar como...** agora funciona logo depois de abrir ou redimensionar a imagem, sem precisar aplicar um filtro antes.
- **Redimensionar...** recusa valores inválidos (0, negativos, acima de 1000% ou pequenos demais para a imagem) com uma mensagem, em vez de dar erro.
- A janela **Redimensionar...** bloqueia a janela principal enquanto está aberta. Antes era possível fechar a imagem ou aplicar um filtro com ela aberta e deixar o programa num estado inconsistente.
- Erros ao salvar (formato não suportado, pasta sem permissão) agora mostram uma mensagem explicando o problema.
- A ajuda funciona com o programa iniciado a partir de qualquer pasta.
- Removida uma cor que só existe no Windows e impediria o programa de abrir em outros sistemas.

Melhorias:

- A ajuda passou a ser texto formatado dentro do programa (arquivo `ajuda_texto.py`), no lugar de uma imagem, e foi atualizada com as novas mensagens de erro.
- Mensagens de erro de **Abrir...** usam a caixa de erro padrão do sistema.
- As barras de gradiente ficaram mais leves em fotos grandes: o filtro só é recalculado quando a barra para de se mover.
- Código reorganizado em uma classe, sem variáveis globais, com remoção de código morto e de trechos duplicados.
- Adicionados `README.md` e `requirements.txt`.

### 1.0

Versão inicial.
