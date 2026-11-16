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
from functools import partial
from PIL import Image
from PIL import ImageTk
from ajuda_texto import TEXTO_AJUDA


# definicao de funcoes
# --------------------------------------------------------------------------------------------------------------------
def close_window():

    estado_inicial_aplicacao()


# --------------------------------------------------------------------------------------------------------------------
def fecha_help_window():

    global frame_ja
    global op_aju_fechar

    habilita_desabilita_frame(frame_ja, 0)   # Habilita janela Ajuda
    habilita_desabilita_menu(op_aju_fechar, 0)  # desabilita Menu Ajuda/Fechar


# --------------------------------------------------------------------------------------------------------------------
def save_img():

    global filename
    global img_corrente

    ftypes = [('PNG', '.png'), ('BMP', '.bmp')]
    filename = fdlg.asksaveasfilename(defaultextension='.png', filetypes=ftypes, confirmoverwrite=True)
    if len(filename) > 0:
        salvar_imagem(filename, img_corrente)


# --------------------------------------------------------------------------------------------------------------------
# cv2.imread/cv2.imwrite nao aceitam caminhos com acentos no Windows (ex.: "Área de Trabalho").
# Por isso o arquivo e lido/gravado pelo numpy e apenas decodificado/codificado pelo OpenCV.
def ler_imagem(caminho):

    dados = np.fromfile(caminho, dtype=np.uint8)
    if dados.size == 0:
        return None
    return cv2.imdecode(dados, cv2.IMREAD_COLOR)  # retorna None se nao for imagem


def salvar_imagem(caminho, imagem):

    extensao = os.path.splitext(caminho)[1] or '.png'
    ok, dados = cv2.imencode(extensao, imagem)
    if ok:
        dados.tofile(caminho)


# --------------------------------------------------------------------------------------------------------------------
def cv_to_tk(cv_img):

    image = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGB)
    image = Image.fromarray(image)
    tk_img = ImageTk.PhotoImage(image)

    return tk_img


# --------------------------------------------------------------------------------------------------------------------
def cancelar(ler):

    ler['text'] = ''
    desfaz()  # desfaz() ja desabilita o menu Ferramentas/Desfazer


# --------------------------------------------------------------------------------------------------------------------
def desfaz():

    global imagem_original

    global op_fer_redimensionar
    global frame_sb
    global op_fer_desfazer

    carrega_img_resize_scrollbar(canvas_root, imagem_original)
    vbar_root.pack(side=tk.RIGHT, fill=tk.Y)
    hbar_root.pack(side=tk.BOTTOM, fill=tk.X)

    # habilita
    habilita_desabilita_menu(op_fer_redimensionar, 1)  # habilita menu Ferramentas/Redimensionar

    # desabilita
    zera_barras()
    habilita_desabilita_frame(frame_sb, 0)  # desbilita barra deslizante de contornos
    habilita_desabilita_menu(op_fer_desfazer, 0)  # desbilita menu Ferramentas/Desfazer


# --------------------------------------------------------------------------------------------------------------------
def zera_barras():

    var_sc.set(gmin)
    var_sc_max.set(gmin)


# --------------------------------------------------------------------------------------------------------------------
def image_resize(tb, ler, xtb, ytb):

    global imagem_original
    global op_fer_desfazer

    def mostra_erro(mensagem):
        ler.place(x=xtb, y=ytb + 20)  # mensagem aparece logo abaixo da caixa de texto
        ler['text'] = mensagem

    img_copy = imagem_original.copy()
    altura, largura = img_copy.shape[:2]

    try:
        aux = int(tb.get())  # poncentagem de incremento/decremento
    except ValueError:
        if len(tb.get()) == 0:
            mostra_erro('Campo não deve estar vazio!')
        else:
            mostra_erro('Valor deve ser nº inteiro!')
        return

    if aux < 1 or aux > porcentagem_max:
        mostra_erro(f'Valor deve estar entre 1 e {porcentagem_max}!')
        return

    fat = aux / 100
    nova_largura = round(largura * fat)
    nova_altura = round(altura * fat)
    if nova_largura < 1 or nova_altura < 1:
        mostra_erro('Porcentagem pequena demais para esta imagem!')
        return

    img_resized = cv2.resize(img_copy, (nova_largura, nova_altura))
    carrega_img_resize_scrollbar(canvas_root, img_resized)
    ler['text'] = ''

    # habilita
    habilita_desabilita_menu(op_fer_desfazer, 1)


# --------------------------------------------------------------------------------------------------------------------
def resize_win():

    xl1, yl1 = 20, 20
    xtb1, ytb1 = 6 * xl1, yl1
    xbt1, ybt1 = 30, 4 * yl1
    xbt2, ybt2 = xbt1 + 70, ybt1
    xbt3, ybt3 = xbt2 + 70, ybt1

    resizewin = tk.Toplevel(root)
    resizewin.title('Redimensiona imagem')
    resizewin.geometry("280x120")
    resizewin.resizable(width=0, height=0)

    frame_rs = tk.Frame(resizewin)
    frame_rs.pack(expand=True, fill=tk.BOTH)

    lerro = tk.Label(frame_rs, text='', fg='red')
    tk.Label(frame_rs, text='Porcentagem: ').place(x=xl1, y=yl1)
    textbox1 = tk.Entry(resizewin)
    textbox1.insert(tk.END, '100')
    action_with_arg1 = partial(image_resize, textbox1, lerro, xtb1, ytb1)
    bt1 = tk.Button(frame_rs, text='OK', width=8, command=action_with_arg1)
    action_with_arg2 = partial(cancelar, lerro)
    bt2 = tk.Button(frame_rs, text='Cancelar', width=8, command=action_with_arg2)
    bt3 = tk.Button(frame_rs, text='Fechar', width=8, command=resizewin.destroy)

    textbox1.place(x=xtb1, y=ytb1)
    bt1.place(x=xbt1, y=ybt1)
    bt2.place(x=xbt2, y=ybt2)
    bt3.place(x=xbt3, y=ybt3)

    resizewin.mainloop()


# --------------------------------------------------------------------------------------------------------------------
def trata_erro(n):

    errorwin = tk.Toplevel(root)
    errorwin.geometry("500x90")

    er, adv = '', ''

    if n == 0:
        er = 'ERRO #0! Arquivo não pode ser aberto.'
        adv = 'Provavelmente você está tentando abrir um arquivo que está protegido.'
    elif n == 1:
        er = 'ERRO #1! Formato desconhecido.'
        adv = 'Provavelmente você está tentando abrir um arquivo que não é de imagem.'
    elif n == 2:
        er = 'ERRO #2! Desconhecido.'
        adv = ''

    tk.Label(errorwin, text=er).pack()
    tk.Label(errorwin, text=adv).pack()
    tk.Button(errorwin, width=10, text='OK', command=errorwin.destroy).place(x=220, y=50)

    errorwin.mainloop()


# --------------------------------------------------------------------------------------------------------------------
def help_window():

    global frame_ja
    global op_aju_fechar

    habilita_desabilita_frame(frame_ja, 1)          # habilita janela Ajuda
    habilita_desabilita_menu(op_aju_fechar, 1)      # habilita Menu Ajuda/Fechar
    texto_help.yview_moveto(0)                      # sempre abre no inicio do texto


# --------------------------------------------------------------------------------------------------------------------
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


# --------------------------------------------------------------------------------------------------------------------
def carrega_img_resize_scrollbar(canvas, im):

    global img_corrente
    global img_contorno
    global cv2image

    cv2image = im.copy()
    img_corrente = im.copy()                          # imagem OpenCV (numpy) usada ao salvar

    limpa_janela_principal()
    img_contorno = cv_to_tk(im)                       # PhotoImage exibida na tela (precisa manter referencia)
    canvas.create_image(0, 0, anchor='nw', image=img_contorno)  # carrega imagem na janela principal
    h = img_contorno.height() + 10
    w = img_contorno.width() + 10
    canvas.config(scrollregion=(0, 0, w, h))          # formata scrollbar para tamanho da imagem carregada


# --------------------------------------------------------------------------------------------------------------------
def contorno_colorido(imagem, minimo, maximo):

    # linhas coloridas (cores da imagem original) sobre fundo preto
    bordas = cv2.Canny(cv2.blur(imagem, (3, 3)), minimo, maximo, kernel_size)
    mascara = (bordas != 0)[:, :, None].astype(imagem.dtype)
    return imagem * mascara


def contorno_preto_branco(imagem, minimo, maximo):

    # linhas pretas sobre fundo branco
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    return cv2.bitwise_not(cv2.Canny(cinza, minimo, maximo, kernel_size))


# --------------------------------------------------------------------------------------------------------------------
def atualiza_contornos(_valor=None):

    # Chamada pelas duas barras deslizantes (o Tk passa o valor da barra, que nao e usado) e ao escolher um filtro.
    global img_contorno
    global img_corrente

    if filtro_ativo is None:
        return

    img_corrente = filtro_ativo(cv2image, var_sc.get(), var_sc_max.get())
    img_contorno = cv_to_tk(img_corrente)
    canvas_root.create_image(0, 0, anchor='nw', image=img_contorno)


# --------------------------------------------------------------------------------------------------------------------
def aplica_filtro(filtro):

    global filtro_ativo

    # habilita
    habilita_desabilita_frame(frame_sb, 1)  # habilita barra deslizante de contornos
    habilita_desabilita_menu(op_fer_desfazer, 1)
    filtro_ativo = filtro
    zera_barras()

    # desabilita
    habilita_desabilita_menu(op_fer_redimensionar, 0)  # desabilita menu Ferramentas/Redimensionar

    atualiza_contornos()


# --------------------------------------------------------------------------------------------------------------------
def limpa_janela_principal():

    canvas_root.delete("all")
    canvas_root['bg'] = 'white'


# --------------------------------------------------------------------------------------------------------------------
def estado_inicial_aplicacao():

    global frame_jp  # 'Janela Principal'
    global frame_sb  # 'Scale Bar'

    global op_arq_salvar
    global op_arquivo_fechar
    global op_fer_desfazer
    global op_fer_redimensionar
    global op_fer_fcor
    global op_fer_fpb

    habilita_desabilita_frame(frame_jp, 0)
    habilita_desabilita_frame(frame_sb, 0)

    habilita_desabilita_menu(op_arq_salvar, 0)
    habilita_desabilita_menu(op_arquivo_fechar, 0)
    habilita_desabilita_menu(op_fer_desfazer, 0)
    habilita_desabilita_menu(op_fer_redimensionar, 0)
    habilita_desabilita_menu(op_fer_fcor, 0)
    habilita_desabilita_menu(op_fer_fpb, 0)


# --------------------------------------------------------------------------------------------------------------------
def habilita_desabilita_menu(menu, flag_menu):

    menu_tk, rotulo = itens_menu[menu]
    menu_tk.entryconfigure(rotulo, state=tk.NORMAL if flag_menu else tk.DISABLED)


# --------------------------------------------------------------------------------------------------------------------
def habilita_desabilita_frame(frame, hab_desab):

    global frame_jp  # 'Janela Principal'
    global frame_ja  # 'Janela Ajuda'
    global frame_sb  # 'Scale Bar'

    if frame == frame_jp:    # frame_root
        if hab_desab == 0:
            canvas_root.delete("all")
            canvas_root['bg'] = 'SystemButtonFace'

    elif frame == frame_ja:                  # frame_help ---------------------------
        if hab_desab == 0:
            frame_help.forget()
        else:
            frame_help.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    elif frame == frame_sb:                 # frame_scalebar ------------------------
        estado = tk.NORMAL if hab_desab else tk.DISABLED
        sc['state'] = estado
        sc_max['state'] = estado


# --------------------------------------------------------------------------------------------------------------------
def carrega_imagem():

    global imagem_original
    global filename

    global op_arq_salvar
    global op_arquivo_fechar
    global op_fer_desfazer
    global op_fer_redimensionar
    global op_fer_fcor
    global op_fer_fpb
    global frame_sb

    filename = fdlg.askopenfilename()  # Isto te permite selecionar um arquivo
    if not filename:  # usuario cancelou a selecao de arquivo
        return

    try:
        imagem_lida = ler_imagem(filename)
    except OSError:
        trata_erro(0)  # 'Provavelmente voce estah tentando abrir um arquivo que estah protegido.'
        return
    except Exception:
        trata_erro(2)  # 'ERRO desconhecido'
        return

    if imagem_lida is None:
        trata_erro(1)  # 'Provavelmente voce estah tentando abrir um arquivo que nao eh de imagem.'
        return

    imagem_original = imagem_lida
    carrega_img_resize_scrollbar(canvas_root, imagem_original)

    # habilita:
    habilita_desabilita_menu(op_arq_salvar, 1)
    habilita_desabilita_menu(op_arquivo_fechar, 1)
    habilita_desabilita_menu(op_fer_redimensionar, 1)
    habilita_desabilita_menu(op_fer_fcor, 1)
    habilita_desabilita_menu(op_fer_fpb, 1)

    # desabilita:
    habilita_desabilita_menu(op_fer_desfazer, 0)
    zera_barras()
    habilita_desabilita_frame(frame_sb, 0)  # desabilita barra deslizante de contornos


# ====================================================================================================================
# PROGRAMA PRINCIPAL
# ====================================================================================================================

# definicao de constantes
# --------------------------------------------------------------------------------------------------------------------
janela_padrao = '1200x560'
background = 'white'
foreground = 'black'

imagem_original = None
cv2image = None
img_contorno = None
img_corrente = None
filename = None

frame_jp = 'Janela Principal'
frame_ja = 'Janela Ajuda'
frame_sb = 'Scale Bar'

op_arq_salvar = 11
op_arquivo_fechar = 12
op_fer_desfazer = 20
op_fer_redimensionar = 21
op_fer_fcor = 22
op_fer_fpb = 23
op_aju_fechar = 31

kernel_size = 3
porcentagem_max = 1000  # limite do redimensionamento, evita imagens enormes que esgotam a memoria

filtro_ativo = None  # contorno_colorido, contorno_preto_branco ou None

# Janela Principal
# --------------------------------------------------------------------------------------------------------------------
root = tk.Tk()  # janela principal
root.title('Contornos')
root.geometry(janela_padrao)

# Menu Principal
# ----------------------------------------------------
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
editmenu = tk.Menu(menubar, tearoff=0)
helpmenu = tk.Menu(menubar, tearoff=0)

# Menu File
# ----------------------------------------------------
menubar.add_cascade(label="Arquivo", menu=filemenu)
filemenu.add_command(label="Abrir...", command=carrega_imagem)
filemenu.add_command(label="Salvar como...", command=save_img)
filemenu.add_command(label="Fechar", command=close_window)
filemenu.add_separator()
filemenu.add_command(label="Sair", command=root.destroy)

# Menu Edit
# ----------------------------------------------------
menubar.add_cascade(label="Ferramentas", menu=editmenu)
editmenu.add_command(label="Desfazer", command=desfaz)
editmenu.add_separator()
editmenu.add_command(label="Redimensionar...", command=resize_win)
editmenu.add_command(label="Filtro Colorido", command=partial(aplica_filtro, contorno_colorido))
editmenu.add_command(label="Filtro Preto e Branco", command=partial(aplica_filtro, contorno_preto_branco))

# Menu Help
# ----------------------------------------------------
menubar.add_cascade(label="Ajuda", menu=helpmenu)
helpmenu.add_command(label="Sobre", command=help_window)
helpmenu.add_separator()
helpmenu.add_command(label="Fechar", command=fecha_help_window)

# Itens de menu que sao habilitados/desabilitados durante o uso: codigo -> (menu, rotulo)
itens_menu = {
    op_arq_salvar: (filemenu, 'Salvar como...'),
    op_arquivo_fechar: (filemenu, 'Fechar'),
    op_fer_desfazer: (editmenu, 'Desfazer'),
    op_fer_redimensionar: (editmenu, 'Redimensionar...'),
    op_fer_fcor: (editmenu, 'Filtro Colorido'),
    op_fer_fpb: (editmenu, 'Filtro Preto e Branco'),
    op_aju_fechar: (helpmenu, 'Fechar'),
}

# cria area (Frame) com scrollbar para incluir figura
# --------------------------------------------------------------------------------------------------------------------
frame_root = tk.Frame(root, height=560)
frame_root.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
frame_root['bg'] = background
frame_help = tk.Frame(root, height=560)

# Barra deslizante para filtro de contornos (frame_scalebar)
# -----------------------------------------------------
gmin = 0
gmax = 900

tk.Label(frame_root, text='C o n t o r n o s', font=('Ar Delaney', '30', 'bold'), bg=background, fg=foreground).pack()
tk.Label(frame_root, bg=background, width=80).pack()


def cria_barra(rotulo, variavel):

    barra = tk.Scale(frame_root, label=rotulo, from_=gmin, to=gmax, length=500, variable=variavel,
                     orient=tk.HORIZONTAL, bg=background, fg=foreground, font='7', command=atualiza_contornos)
    barra.pack()
    return barra


var_sc = tk.IntVar()
sc = cria_barra('Gera contornos - gradiente mínimo', var_sc)
var_sc_max = tk.IntVar()
sc_max = cria_barra('Gera contornos - gradiente máximo', var_sc_max)

tk.Label(frame_root, bg=background, width=80).pack()

# Canvas onde sera carregada a imagem (frame_root)
# -----------------------------------------------------
canvas_root = tk.Canvas(frame_root, bd=3, relief=tk.GROOVE, scrollregion=(0, 0, 100, 100))  # SUNKEN, RAISED, GROOVE, RIDGE
canvas_root.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
vbar_root = tk.Scrollbar(canvas_root, orient=tk.VERTICAL)
vbar_root.pack(side=tk.RIGHT, fill=tk.Y)
vbar_root.config(command=canvas_root.yview)
hbar_root = tk.Scrollbar(canvas_root, orient=tk.HORIZONTAL)
hbar_root.pack(side=tk.BOTTOM, fill=tk.X)
hbar_root.config(command=canvas_root.xview)
canvas_root.config(xscrollcommand=hbar_root.set, yscrollcommand=vbar_root.set)

# Texto da Ajuda (frame_help) - o conteudo fica em ajuda_texto.py
# -----------------------------------------------------
bt_help = tk.Button(frame_help, text='X', font='bold', command=fecha_help_window)
bt_help.pack(side=tk.TOP, anchor='e')
vbar_help = tk.Scrollbar(frame_help, orient=tk.VERTICAL)
vbar_help.pack(side=tk.RIGHT, fill=tk.Y)
texto_help = tk.Text(frame_help, width=60, wrap=tk.WORD, bd=3, relief=tk.GROOVE, bg='white', padx=12, pady=8,
                  font=('Calibri', 11), tabs=('130p',), cursor='arrow', yscrollcommand=vbar_help.set)
texto_help.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
vbar_help.config(command=texto_help.yview)

azul = '#0070C0'
negrito = ('Calibri', 11, 'bold')
italico = ('Calibri', 11, 'italic')
texto_help.tag_configure('t', font=('Cambria', 14, 'bold italic'), spacing1=10, spacing3=4)
texto_help.tag_configure('m', font=negrito, foreground=azul)
texto_help.tag_configure('b', font=negrito)
texto_help.tag_configure('i', font=italico)
texto_help.tag_configure('u', underline=True)
texto_help.tag_configure('e', foreground='red')
texto_help.tag_configure('s', font=italico, foreground='red')
texto_help.tag_configure('tabela', lmargin2='130p')   # linhas quebradas ficam alinhadas na segunda coluna
preenche_ajuda(texto_help, TEXTO_AJUDA)

estado_inicial_aplicacao()
habilita_desabilita_menu(op_aju_fechar, 0)

root.config(menu=menubar)
root.mainloop()
