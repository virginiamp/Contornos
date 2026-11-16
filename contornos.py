"""
Autor: Virginia Martins Perozim
Versão: 1.0
"""

import os
import re
import cv2
import numpy as np
import tkinter as tk
import tkinter.filedialog as fdlg
from tkinter import messagebox
from functools import partial
from PIL import Image
from PIL import ImageTk
from ajuda_texto import TEXTO_AJUDA


# definicao de constantes
# --------------------------------------------------------------------------------------------------------------------
JANELA_PADRAO = '1200x560'
FUNDO = 'white'
FRENTE = 'black'

KERNEL_SIZE = 3
PORCENTAGEM_MAX = 1000  # limite do redimensionamento, evita imagens enormes que esgotam a memoria
GMIN = 0                # valores minimo e maximo das barras deslizantes de contornos
GMAX = 900
ATRASO_BARRA_MS = 150   # tempo que a barra deslizante precisa ficar parada para o filtro ser recalculado

ERROS_ABRIR = {
    0: ('ERRO #0! Arquivo não pode ser aberto.',
        'Provavelmente você está tentando abrir um arquivo que está protegido.'),
    1: ('ERRO #1! Formato desconhecido.',
        'Provavelmente você está tentando abrir um arquivo que não é de imagem.'),
    2: ('ERRO #2! Desconhecido.', ''),
}


# funcoes de imagem (nao dependem da interface)
# --------------------------------------------------------------------------------------------------------------------
# cv2.imread/cv2.imwrite nao aceitam caminhos com acentos no Windows (ex.: "Área de Trabalho").
# Por isso o arquivo e lido/gravado pelo numpy e apenas decodificado/codificado pelo OpenCV.
def ler_imagem(caminho):

    dados = np.fromfile(caminho, dtype=np.uint8)
    if dados.size == 0:
        return None
    return cv2.imdecode(dados, cv2.IMREAD_COLOR)  # retorna None se nao for imagem


def salvar_imagem(caminho, imagem):

    # Levanta ValueError se o formato (extensao) nao for suportado e OSError se nao conseguir gravar o arquivo.
    extensao = os.path.splitext(caminho)[1] or '.png'
    try:
        ok, dados = cv2.imencode(extensao, imagem)
    except cv2.error:
        ok = False
    if not ok:
        raise ValueError(f'formato não suportado: {extensao}')
    dados.tofile(caminho)


def cv_to_tk(cv_img):

    # o OpenCV guarda as cores em BGR (ou 1 canal, no filtro preto e branco); o Tk/Pillow espera RGB
    conversao = cv2.COLOR_GRAY2RGB if cv_img.ndim == 2 else cv2.COLOR_BGR2RGB
    return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(cv_img, conversao)))


def contorno_colorido(imagem, minimo, maximo):

    # linhas coloridas (cores da imagem original) sobre fundo preto
    bordas = cv2.Canny(cv2.blur(imagem, (3, 3)), minimo, maximo, KERNEL_SIZE)
    mascara = (bordas != 0)[:, :, None].astype(imagem.dtype)
    return imagem * mascara


def contorno_preto_branco(imagem, minimo, maximo):

    # linhas pretas sobre fundo branco
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    return cv2.bitwise_not(cv2.Canny(cinza, minimo, maximo, KERNEL_SIZE))


def preenche_ajuda(widget, texto):

    # Insere o texto da ajuda (ver ajuda_texto.py) no widget Text, aplicando as marcacoes [x]...[/x] como estilos.
    widget.config(state=tk.NORMAL)
    widget.delete('1.0', tk.END)
    for linha in texto.splitlines():
        tags_linha = ('tabela',) if '\t' in linha else ()
        pos = 0
        for marca in re.finditer(r'\[(\w)\](.*?)\[/\1\]', linha):
            widget.insert(tk.END, linha[pos:marca.start()], tags_linha)
            widget.insert(tk.END, marca.group(2), tags_linha + (marca.group(1),))
            pos = marca.end()
        widget.insert(tk.END, linha[pos:] + '\n', tags_linha)
    widget.config(state=tk.DISABLED)                   # somente leitura


# ====================================================================================================================
# APLICATIVO
# ====================================================================================================================
class Contornos:

    def __init__(self, root):

        self.root = root

        # estado do aplicativo
        self.imagem_original = None   # imagem como foi aberta (usada por Desfazer e Redimensionar)
        self.imagem_base = None       # imagem sobre a qual os filtros sao aplicados (original ou redimensionada)
        self.img_corrente = None      # imagem OpenCV (numpy) exibida no momento; e a que sera salva
        self.img_tela = None          # PhotoImage exibida na tela (precisa manter referencia)
        self.filtro_ativo = None      # contorno_colorido, contorno_preto_branco ou None
        self.atualizacao_pendente = None  # recalculo do filtro agendado pelas barras deslizantes

        root.title('Contornos')
        root.geometry(JANELA_PADRAO)

        self._cria_menus()
        self._cria_janela_principal()
        self._cria_janela_ajuda()

        self.estado_inicial_aplicacao()
        self.habilita_menu('ajuda_fechar', False)

        root.config(menu=self.menubar)

    # ----------------------------------------------------------------------------------------------------------------
    # construcao da interface
    # ----------------------------------------------------------------------------------------------------------------
    def _cria_menus(self):

        self.menubar = tk.Menu(self.root)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        editmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu = tk.Menu(self.menubar, tearoff=0)

        # Menu Arquivo
        self.menubar.add_cascade(label="Arquivo", menu=filemenu)
        filemenu.add_command(label="Abrir...", command=self.carrega_imagem)
        filemenu.add_command(label="Salvar como...", command=self.salva_imagem)
        filemenu.add_command(label="Fechar", command=self.estado_inicial_aplicacao)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=self.root.destroy)

        # Menu Ferramentas
        self.menubar.add_cascade(label="Ferramentas", menu=editmenu)
        editmenu.add_command(label="Desfazer", command=self.desfaz)
        editmenu.add_separator()
        editmenu.add_command(label="Redimensionar...", command=self.resize_win)
        editmenu.add_command(label="Filtro Colorido", command=partial(self.aplica_filtro, contorno_colorido))
        editmenu.add_command(label="Filtro Preto e Branco",
                             command=partial(self.aplica_filtro, contorno_preto_branco))

        # Menu Ajuda
        self.menubar.add_cascade(label="Ajuda", menu=helpmenu)
        helpmenu.add_command(label="Sobre", command=self.mostra_ajuda)
        helpmenu.add_separator()
        helpmenu.add_command(label="Fechar", command=self.fecha_ajuda)

        # Itens de menu que sao habilitados/desabilitados durante o uso: nome -> (menu, rotulo)
        self.itens_menu = {
            'salvar': (filemenu, 'Salvar como...'),
            'fechar': (filemenu, 'Fechar'),
            'desfazer': (editmenu, 'Desfazer'),
            'redimensionar': (editmenu, 'Redimensionar...'),
            'filtro_cor': (editmenu, 'Filtro Colorido'),
            'filtro_pb': (editmenu, 'Filtro Preto e Branco'),
            'ajuda_fechar': (helpmenu, 'Fechar'),
        }

    def _cria_janela_principal(self):

        frame_root = tk.Frame(self.root, height=560, bg=FUNDO)
        frame_root.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        tk.Label(frame_root, text='C o n t o r n o s', font=('Ar Delaney', '30', 'bold'), bg=FUNDO, fg=FRENTE).pack()
        tk.Label(frame_root, bg=FUNDO, width=80).pack()

        # barras deslizantes para filtro de contornos
        self.var_sc = tk.IntVar()
        self.sc = self._cria_barra(frame_root, 'Gera contornos - gradiente mínimo', self.var_sc)
        self.var_sc_max = tk.IntVar()
        self.sc_max = self._cria_barra(frame_root, 'Gera contornos - gradiente máximo', self.var_sc_max)

        tk.Label(frame_root, bg=FUNDO, width=80).pack()

        # canvas onde sera carregada a imagem
        self.canvas = tk.Canvas(frame_root, bd=3, relief=tk.GROOVE, scrollregion=(0, 0, 100, 100))
        self.canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        vbar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    def _cria_barra(self, pai, rotulo, variavel):

        barra = tk.Scale(pai, label=rotulo, from_=GMIN, to=GMAX, length=500, variable=variavel,
                         orient=tk.HORIZONTAL, bg=FUNDO, fg=FRENTE, font='7', command=self.barra_movida)
        barra.pack()
        return barra

    def _cria_janela_ajuda(self):

        # o conteudo da ajuda fica em ajuda_texto.py
        self.frame_help = tk.Frame(self.root, height=560)
        tk.Button(self.frame_help, text='X', font='bold', command=self.fecha_ajuda).pack(side=tk.TOP, anchor='e')
        vbar = tk.Scrollbar(self.frame_help, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_help = tk.Text(self.frame_help, width=60, wrap=tk.WORD, bd=3, relief=tk.GROOVE, bg='white',
                                  padx=12, pady=8, font=('Calibri', 11), tabs=('130p',), cursor='arrow',
                                  yscrollcommand=vbar.set)
        self.texto_help.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        vbar.config(command=self.texto_help.yview)

        azul = '#0070C0'
        negrito = ('Calibri', 11, 'bold')
        italico = ('Calibri', 11, 'italic')
        self.texto_help.tag_configure('t', font=('Cambria', 14, 'bold italic'), spacing1=10, spacing3=4)
        self.texto_help.tag_configure('m', font=negrito, foreground=azul)
        self.texto_help.tag_configure('b', font=negrito)
        self.texto_help.tag_configure('i', font=italico)
        self.texto_help.tag_configure('u', underline=True)
        self.texto_help.tag_configure('e', foreground='red')
        self.texto_help.tag_configure('s', font=italico, foreground='red')
        self.texto_help.tag_configure('tabela', lmargin2='130p')  # linhas quebradas ficam alinhadas na 2a coluna
        preenche_ajuda(self.texto_help, TEXTO_AJUDA.replace('{PORCENTAGEM_MAX}', str(PORCENTAGEM_MAX)))

    # ----------------------------------------------------------------------------------------------------------------
    # estado da interface
    # ----------------------------------------------------------------------------------------------------------------
    def habilita_menu(self, nome, habilitado):

        menu_tk, rotulo = self.itens_menu[nome]
        menu_tk.entryconfigure(rotulo, state=tk.NORMAL if habilitado else tk.DISABLED)

    def habilita_barras(self, habilitado):

        estado = tk.NORMAL if habilitado else tk.DISABLED
        self.sc['state'] = estado
        self.sc_max['state'] = estado

    def zera_barras(self):

        self.var_sc.set(GMIN)
        self.var_sc_max.set(GMIN)

    def estado_inicial_aplicacao(self):

        # tambem usado pelo menu Arquivo/Fechar
        self.cancela_atualizacao_pendente()
        self.canvas.delete("all")
        self.canvas['bg'] = self.root.cget('bg')  # cor padrao do sistema ('SystemButtonFace' so existe no Windows)
        self.habilita_barras(False)
        for nome in ('salvar', 'fechar', 'desfazer', 'redimensionar', 'filtro_cor', 'filtro_pb'):
            self.habilita_menu(nome, False)

    # ----------------------------------------------------------------------------------------------------------------
    # Menu Arquivo
    # ----------------------------------------------------------------------------------------------------------------
    def carrega_imagem(self):

        filename = fdlg.askopenfilename()  # Isto te permite selecionar um arquivo
        if not filename:  # usuario cancelou a selecao de arquivo
            return

        try:
            imagem_lida = ler_imagem(filename)
        except OSError:
            self.trata_erro(0)  # 'Provavelmente voce estah tentando abrir um arquivo que estah protegido.'
            return
        except Exception:
            self.trata_erro(2)  # 'ERRO desconhecido'
            return

        if imagem_lida is None:
            self.trata_erro(1)  # 'Provavelmente voce estah tentando abrir um arquivo que nao eh de imagem.'
            return

        self.imagem_original = imagem_lida
        self.mostra_imagem(self.imagem_original)

        # habilita:
        for nome in ('salvar', 'fechar', 'redimensionar', 'filtro_cor', 'filtro_pb'):
            self.habilita_menu(nome, True)

        # desabilita:
        self.habilita_menu('desfazer', False)
        self.zera_barras()
        self.habilita_barras(False)

    def salva_imagem(self):

        ftypes = [('PNG', '.png'), ('BMP', '.bmp')]
        filename = fdlg.asksaveasfilename(defaultextension='.png', filetypes=ftypes, confirmoverwrite=True)
        if not filename:  # usuario cancelou
            return

        try:
            salvar_imagem(filename, self.img_corrente)
        except ValueError:
            messagebox.showerror('Contornos', 'ERRO! Formato de arquivo não suportado.',
                                 detail='Salve a imagem com a extensão .png ou .bmp.', parent=self.root)
        except OSError:
            messagebox.showerror('Contornos', 'ERRO! Não foi possível salvar o arquivo.',
                                 detail='Verifique se você tem permissão para gravar nessa pasta e se o arquivo '
                                        'não está aberto em outro programa.', parent=self.root)

    def trata_erro(self, n):

        er, adv = ERROS_ABRIR[n]
        messagebox.showerror('Contornos', er, detail=adv, parent=self.root)

    # ----------------------------------------------------------------------------------------------------------------
    # exibicao da imagem
    # ----------------------------------------------------------------------------------------------------------------
    def mostra_imagem(self, im):

        # mostra uma nova imagem base (aberta, redimensionada ou desfeita), sem filtro
        self.cancela_atualizacao_pendente()  # evita que um recalculo agendado aplique o filtro sobre esta imagem
        self.imagem_base = im.copy()
        self.img_corrente = im.copy()

        self.canvas.delete("all")
        self.canvas['bg'] = 'white'
        self.img_tela = cv_to_tk(im)
        self.canvas.create_image(0, 0, anchor='nw', image=self.img_tela)
        h = self.img_tela.height() + 10
        w = self.img_tela.width() + 10
        self.canvas.config(scrollregion=(0, 0, w, h))   # formata scrollbar para tamanho da imagem carregada

    # ----------------------------------------------------------------------------------------------------------------
    # Menu Ferramentas
    # ----------------------------------------------------------------------------------------------------------------
    def desfaz(self):

        self.mostra_imagem(self.imagem_original)

        # habilita
        self.habilita_menu('redimensionar', True)

        # desabilita
        self.zera_barras()
        self.habilita_barras(False)
        self.habilita_menu('desfazer', False)

    def aplica_filtro(self, filtro):

        # habilita
        self.habilita_barras(True)
        self.habilita_menu('desfazer', True)
        self.filtro_ativo = filtro
        self.zera_barras()

        # desabilita
        self.habilita_menu('redimensionar', False)

        self.cancela_atualizacao_pendente()
        self.atualiza_contornos()  # ao escolher o filtro, aplica na hora (sem esperar)

    def barra_movida(self, _valor=None):

        # Chamada pelas barras deslizantes a cada movimento (o Tk passa o valor da barra, que nao e usado).
        # Em fotos grandes o filtro demora, entao so recalcula quando a barra fica parada por ATRASO_BARRA_MS.
        self.cancela_atualizacao_pendente()
        self.atualizacao_pendente = self.root.after(ATRASO_BARRA_MS, self.atualiza_contornos)

    def cancela_atualizacao_pendente(self):

        if self.atualizacao_pendente is not None:
            self.root.after_cancel(self.atualizacao_pendente)
            self.atualizacao_pendente = None

    def atualiza_contornos(self):

        self.atualizacao_pendente = None
        if self.filtro_ativo is None:
            return

        self.img_corrente = self.filtro_ativo(self.imagem_base, self.var_sc.get(), self.var_sc_max.get())
        self.img_tela = cv_to_tk(self.img_corrente)
        self.canvas.create_image(0, 0, anchor='nw', image=self.img_tela)

    def resize_win(self):

        xl1, yl1 = 20, 20
        xtb1, ytb1 = 6 * xl1, yl1
        xbt1, ybt1 = 30, 4 * yl1
        xbt2, ybt2 = xbt1 + 70, ybt1
        xbt3, ybt3 = xbt2 + 70, ybt1

        resizewin = tk.Toplevel(self.root)
        resizewin.title('Redimensiona imagem')
        resizewin.geometry("280x120")
        resizewin.resizable(width=0, height=0)

        frame_rs = tk.Frame(resizewin)
        frame_rs.pack(expand=True, fill=tk.BOTH)

        lerro = tk.Label(frame_rs, text='', fg='red')
        tk.Label(frame_rs, text='Porcentagem: ').place(x=xl1, y=yl1)
        textbox1 = tk.Entry(resizewin)
        textbox1.insert(tk.END, '100')
        bt1 = tk.Button(frame_rs, text='OK', width=8, command=partial(self.image_resize, textbox1, lerro, xtb1, ytb1))
        bt2 = tk.Button(frame_rs, text='Cancelar', width=8, command=partial(self.cancelar, lerro))
        bt3 = tk.Button(frame_rs, text='Fechar', width=8, command=resizewin.destroy)

        textbox1.place(x=xtb1, y=ytb1)
        bt1.place(x=xbt1, y=ybt1)
        bt2.place(x=xbt2, y=ybt2)
        bt3.place(x=xbt3, y=ybt3)

        # Janela modal: enquanto estiver aberta, a janela principal nao responde. Assim nao e possivel fechar a
        # imagem, aplicar um filtro ou abrir outra janela de redimensionamento com esta aberta.
        resizewin.transient(self.root)
        resizewin.grab_set()
        textbox1.focus_set()

    def image_resize(self, tb, ler, xtb, ytb):

        def mostra_erro(mensagem):
            ler.place(x=xtb, y=ytb + 20)  # mensagem aparece logo abaixo da caixa de texto
            ler['text'] = mensagem

        altura, largura = self.imagem_original.shape[:2]

        try:
            aux = int(tb.get())  # porcentagem de incremento/decremento
        except ValueError:
            if len(tb.get()) == 0:
                mostra_erro('Campo não deve estar vazio!')
            else:
                mostra_erro('Valor deve ser nº inteiro!')
            return

        if aux < 1 or aux > PORCENTAGEM_MAX:
            mostra_erro(f'Valor deve estar entre 1 e {PORCENTAGEM_MAX}!')
            return

        fat = aux / 100
        nova_largura = round(largura * fat)
        nova_altura = round(altura * fat)
        if nova_largura < 1 or nova_altura < 1:
            mostra_erro('Porcentagem pequena demais para esta imagem!')
            return

        self.mostra_imagem(cv2.resize(self.imagem_original, (nova_largura, nova_altura)))
        ler['text'] = ''

        # habilita
        self.habilita_menu('desfazer', True)

    def cancelar(self, ler):

        ler['text'] = ''
        self.desfaz()  # desfaz() ja desabilita o menu Ferramentas/Desfazer

    # ----------------------------------------------------------------------------------------------------------------
    # Menu Ajuda
    # ----------------------------------------------------------------------------------------------------------------
    def mostra_ajuda(self):

        self.frame_help.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.habilita_menu('ajuda_fechar', True)
        self.texto_help.yview_moveto(0)                 # sempre abre no inicio do texto

    def fecha_ajuda(self):

        self.frame_help.forget()
        self.habilita_menu('ajuda_fechar', False)


# ====================================================================================================================
# PROGRAMA PRINCIPAL
# ====================================================================================================================
def main():

    root = tk.Tk()
    Contornos(root)
    root.mainloop()


if __name__ == '__main__':
    main()
