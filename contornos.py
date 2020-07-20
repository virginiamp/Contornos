import cv2
from tkinter import *
import tkinter.filedialog as fdlg
from functools import partial
from PIL import Image
from PIL import ImageTk


# definicao de funcoes
# --------------------------------------------------------------------------------------------------------------------
def donothing():

    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


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
        cv2.imwrite(filename, img_corrente)


# --------------------------------------------------------------------------------------------------------------------
def cv_to_tk(cv_img):

    image = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGB)
    image = Image.fromarray(image)
    tk_img = ImageTk.PhotoImage(image)

    return tk_img


# --------------------------------------------------------------------------------------------------------------------
def cancelar(ler):

    global op_fer_desfazer

    ler['text'] = ''
    desfaz()

    # desabilita
    habilita_desabilita_menu(op_fer_desfazer, 0)


# --------------------------------------------------------------------------------------------------------------------
def desfaz():

    global imagem_original

    global op_fer_redimensionar
    global frame_sb
    global op_fer_desfazer

    carrega_img_reseize_scrollbar(canvas_root, imagem_original, 0)
    vbar_root.pack(side=RIGHT, fill=Y)
    hbar_root.pack(side=BOTTOM, fill=X)

    # habilita
    habilita_desabilita_menu(op_fer_redimensionar, 1)  # habilita menu Ferramentas/Redimensionar

    # desabilita
    var_sc.set(gmin)
    habilita_desabilita_frame(frame_sb, 0)  # desbilita barra deslizante de contornos
    habilita_desabilita_menu(op_fer_desfazer, 0)  # desbilita menu Ferramentas/Desfazer


# --------------------------------------------------------------------------------------------------------------------
def image_reseize(tb, ler, xtb, ytb):

    global imagem_original
    global op_fer_desfazer

    lxer = xtb
    lyer = ytb + 20

    img_copy = imagem_original.copy()
    icx = img_copy.shape[1]

    try:
        aux = int(tb.get())  # poncentagem de incremento/decremento
    except ValueError:
        ler.place(x=lxer, y=lyer)
        if len(tb.get()) == 0:
            ler['text'] = 'Campo não deve estar vazio!'
        else:
            ler['text'] = 'Valor deve ser nº inteiro!'
    else:
        valor = aux/100
        fat = (icx * valor) / icx

        img_reseized = cv2.resize(img_copy, None, fx=fat, fy=fat)
        carrega_img_reseize_scrollbar(canvas_root, img_reseized, 0)
        ler['text'] = ''

        # habilita
        habilita_desabilita_menu(op_fer_desfazer, 1)


# --------------------------------------------------------------------------------------------------------------------
def reseize_win():

    xl1, yl1 = 20, 20
    xtb1, ytb1 = 6 * xl1, yl1
    xbt1, ybt1 = 30, 4 * yl1
    xbt2, ybt2 = xbt1 + 70, ybt1
    xbt3, ybt3 = xbt2 + 70, ybt1

    resizewin = Toplevel(root)
    resizewin.title('Redimensiona imagem')
    resizewin.geometry("280x120")
    resizewin.resizable(width=0, height=0)

    frame_rs = Frame(resizewin)
    frame_rs.pack(expand=True, fill=BOTH)

    lerro = Label(frame_rs, text='', fg='red')
    Label(frame_rs, text='Porcentagem: ').place(x=xl1, y=yl1)
    textbox1 = Entry(resizewin)
    textbox1.insert(END, '100')
    action_with_arg1 = partial(image_reseize, textbox1, lerro, xtb1, ytb1)
    bt1 = Button(frame_rs, text='OK', width=8, command=action_with_arg1)
    action_with_arg2 = partial(cancelar, lerro)
    bt2 = Button(frame_rs, text='Cancelar', width=8, command=action_with_arg2)
    bt3 = Button(frame_rs, text='Fechar', width=8, command=resizewin.destroy)

    textbox1.place(x=xtb1, y=ytb1)
    bt1.place(x=xbt1, y=ybt1)
    bt2.place(x=xbt2, y=ybt2)
    bt3.place(x=xbt3, y=ybt3)

    resizewin.mainloop()


# --------------------------------------------------------------------------------------------------------------------
def trata_erro(n):

    errorwin = Toplevel(root)
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

    Label(errorwin, text=er).pack()
    Label(errorwin, text=adv).pack()
    Button(errorwin, width=10, text='OK', command=errorwin.destroy).place(x=220, y=50)

    errorwin.mainloop()


# --------------------------------------------------------------------------------------------------------------------
def help_window():

    global tajuda
    global frame_ja
    global op_aju_fechar

    habilita_desabilita_frame(frame_ja, 1)          # habilita janela Ajuda
    habilita_desabilita_menu(op_aju_fechar, 1)      # habilita Menu Ajuda/Fechar

    tajuda = PhotoImage(file='janela_ajuda_nova.png')
    h = tajuda.height() + 10
    w = tajuda.width() + 10
    canvas_help.config(scrollregion=(0, 0, w, h))
    canvas_help.create_image(0, 0, anchor='nw', image=tajuda)
    bt_help.place(x=480, y=4)


# --------------------------------------------------------------------------------------------------------------------
def carrega_img_reseize_scrollbar(canvas, im, wg):

    global img_corrente
    global cv2image

    cv2image = im.copy()

    limpa_widget(wg)
    img_corrente = cv_to_tk(im)                       # transforma imagem em PhotoImage
    canvas.create_image(0, 0, anchor='nw', image=img_corrente)  # carrega imagem na janela principal
    h = img_corrente.height() + 10
    w = img_corrente.width() + 10
    canvas.config(scrollregion=(0, 0, w, h))          # formata scrollbar para tamanho da imagem carregada


# --------------------------------------------------------------------------------------------------------------------
def contornos_cor(n):

    global hab_desab_filtro

    if hab_desab_filtro[0] == 1:
        canny_threshold_cor(gmin, var_sc.get())
    elif hab_desab_filtro[1] == 1:
        canny_threshold_pb(gmin, var_sc.get())


# --------------------------------------------------------------------------------------------------------------------
def canny_threshold_cor(val1, val2):

    global img_contorno
    global img_corrente
    global cv2image

    low_threshold = val1
    upper_threshold = val2
    img_blur = cv2.blur(cv2image, (3, 3))
    detected_edges = cv2.Canny(img_blur, low_threshold, upper_threshold, kernel_size)
    mask = detected_edges != 0
    img_corrente = cv2image * (mask[:, :, None].astype(cv2image.dtype))
    img_contorno = cv_to_tk(img_corrente)
    canvas_root.create_image(0, 0, anchor='nw', image=img_contorno)


# --------------------------------------------------------------------------------------------------------------------
def canny_threshold_pb(val1, val2):

    global img_contorno
    global img_corrente
    global cv2image

    low_threshold = val1
    upper_threshold = val2
    src_gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(src_gray, low_threshold, upper_threshold, kernel_size)
    img_corrente = cv2.bitwise_not(edges)
    img_contorno = cv_to_tk(img_corrente)
    canvas_root.create_image(0, 0, anchor='nw', image=img_contorno)


# --------------------------------------------------------------------------------------------------------------------
def filtro_colorido():

    global hab_desab_filtro
    global op_fer_redimensionar
    global frame_sb
    global op_fer_desfazer

    # habilita
    habilita_desabilita_frame(frame_sb, 1)  # habilita barra deslizante de contornos
    habilita_desabilita_menu(op_fer_desfazer, 1)
    hab_desab_filtro = [1, 0]
    var_sc.set(gmin)

    # desabilita
    habilita_desabilita_menu(op_fer_redimensionar, 0)  # desabilita menu Ferramentas/Redimensionar

    canny_threshold_cor(0, 0)


# --------------------------------------------------------------------------------------------------------------------
def filtro_pretobranco():

    global hab_desab_filtro
    global op_fer_redimensionar
    global frame_sb
    global op_fer_desfazer

    # habilita
    habilita_desabilita_frame(frame_sb, 1)  # habilita barra deslizante de contornos
    habilita_desabilita_menu(op_fer_desfazer, 1)
    hab_desab_filtro = [0, 1]
    var_sc.set(gmin)

    # desabilita
    habilita_desabilita_menu(op_fer_redimensionar, 0)   # desabilita menu Ferramentas/Redimensionar

    canny_threshold_pb(0, 0)


# --------------------------------------------------------------------------------------------------------------------
def limpa_widget(w1):

    global hab_desab_filtro

    if w1 == 0:                       # janela principal ----------------------
        canvas_root.delete("all")
        canvas_root['bg'] = 'white'
    elif w1 == 1:                     # barra deslizante de contornos-----------
        hab_desab_filtro = [0, 0]
    elif w1 == 2:
        pass


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

    global menu_arquivo
    global menu_ajuda
    global menu_ferramentas

    global op_arq_salvar
    global op_arquivo_fechar
    global op_fer_desfazer
    global op_fer_redimensionar
    global op_fer_fcor
    global op_fer_fpb
    global op_aju_fechar

    if menu == op_arq_salvar:
        if flag_menu == 0:
            filemenu.entryconfigure('Salvar como...', state=DISABLED)
        else:
            filemenu.entryconfigure('Salvar como...', state=NORMAL)

    elif menu == op_arquivo_fechar:
        if flag_menu == 0:
            filemenu.entryconfigure('Fechar', state=DISABLED)
        else:
            filemenu.entryconfigure('Fechar', state=NORMAL)

    elif menu == op_fer_desfazer:
        if flag_menu == 0:
            editmenu.entryconfigure('Desfazer', state=DISABLED)
        else:
            editmenu.entryconfigure('Desfazer', state=NORMAL)

    elif menu == op_fer_redimensionar:
        if flag_menu == 0:
            editmenu.entryconfigure('Redimensionar...', state=DISABLED)
        else:
            editmenu.entryconfigure('Redimensionar...', state=NORMAL)

    elif menu == op_fer_fcor:
        if flag_menu == 0:
            editmenu.entryconfigure('Filtro Colorido', state=DISABLED)
        else:
            editmenu.entryconfigure('Filtro Colorido', state=NORMAL)

    elif menu == op_fer_fpb:
        if flag_menu == 0:
            editmenu.entryconfigure('Filtro Preto e Branco', state=DISABLED)
        else:
            editmenu.entryconfigure('Filtro Preto e Branco', state=NORMAL)

    elif menu == op_aju_fechar:
        if flag_menu == 0:
            helpmenu.entryconfigure('Fechar', state=DISABLED)
        else:
            helpmenu.entryconfigure('Fechar', state=NORMAL)


# --------------------------------------------------------------------------------------------------------------------
def habilita_desabilita_frame(frame, hab_desab):

    global frame_jp  # 'Janela Principal'
    global frame_ja  # 'Janela Ajuda'
    global frame_sb  # 'Scale Bar'

    if frame == frame_jp:    # frame_root
        if hab_desab == 0:
            canvas_root.delete("all")
            canvas_root['bg'] = 'SystemButtonFace'
        else:
            pass

    elif frame == frame_ja:                  # frame_help ---------------------------
        if hab_desab == 0:
            frame_help.forget()
            bt_help.forget()
        else:
            frame_help.pack(fill=BOTH, side=TOP, expand=True)
            vbar_help.pack(side=RIGHT, fill=Y)
            canvas_help.pack(side=LEFT, expand=TRUE, fill=BOTH)
            canvas_help['bg'] = 'white'

    elif frame == frame_sb:                 # frame_scalebar ------------------------
        if hab_desab == 0:
            sc['state'] = DISABLED
            lsc['state'] = DISABLED
        else:
            sc['state'] = NORMAL
            lsc['state'] = NORMAL


# --------------------------------------------------------------------------------------------------------------------
def carrega_imagem():

    global imagem_original
    global filename
    global cv2image

    global op_arq_salvar
    global op_arquivo_fechar
    global op_fer_desfazer
    global op_fer_redimensionar
    global op_fer_fcor
    global op_fer_fpb
    global op_aju_fechar
    global frame_sb

    filename = fdlg.askopenfilename()  # Isto te permite selecionar um arquivo
    if not cv2.haveImageReader(filename):  # Returns true if the specified image can be decoded by OpenCV
        trata_erro(0)
    else:
        if len(filename) > 0:
            imagem_original = cv2.imread(filename)
            try:
                cv2image = imagem_original.copy()
            except (AttributeError, cv2.error):
                trata_erro(1)  # 'Provavelmente você está tentando abrir um arquivo que não é de imagem.'
            except:
                trata_erro(2)  # 'ERRO desconhecido'
            else:
                carrega_img_reseize_scrollbar(canvas_root, cv2image, 0)

                # habilita:
                habilita_desabilita_menu(op_arq_salvar, 1)
                habilita_desabilita_menu(op_arquivo_fechar, 1)
                habilita_desabilita_menu(op_fer_redimensionar, 1)
                habilita_desabilita_menu(op_fer_fcor, 1)
                habilita_desabilita_menu(op_fer_fpb, 1)

                # desabilita:
                habilita_desabilita_menu(op_fer_desfazer, 0)
                var_sc.set(gmin)
                habilita_desabilita_frame(frame_sb, 0)  # desabilia barra deslizante de contornos


# ====================================================================================================================
# PROGRAMA PRINCIPAL
# ====================================================================================================================

# definicao de constantes
# --------------------------------------------------------------------------------------------------------------------
janela_padrao = '1200x560'
# backgroud = 'SystemButtonFace'
backgroud = 'white'
foreground = 'black'

imagem_original = None
cv2image = None
tajuda = None
img_contorno = None
img_corrente = None
filename = None
filename1 = None

frame_jp = 'Janela Principal'
frame_ja = 'Janela Ajuda'
frame_sb = 'Scale Bar'

menu_arquivo = 'Menu Arquivo'
op_arq_abrir = 10
op_arq_salvar = 11
op_arquivo_fechar = 12
op_arq_sair = 13
menu_ferramentas = 'Menu Ferramentas'
op_fer_desfazer = 20
op_fer_redimensionar = 21
op_fer_fcor = 22
op_fer_fpb = 23
menu_ajuda = 'Menu Ajuda'
op_aj_sobre = 30
op_aju_fechar = 31

window_name = 'Contornos'
kernel_size = 3

hab_desab_filtro = [0, 0]

# Janela Principal
# --------------------------------------------------------------------------------------------------------------------
root = Tk()  # janela principal
root.title('Contornos')
root.geometry(janela_padrao)

# Menu Principal
# ----------------------------------------------------
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)

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
editmenu.add_command(label="Redimensionar...", command=reseize_win)
editmenu.add_command(label="Filtro Colorido", command=filtro_colorido)
editmenu.add_command(label="Filtro Preto e Branco", command=filtro_pretobranco)

# Menu Help
# ----------------------------------------------------
menubar.add_cascade(label="Ajuda", menu=helpmenu)
helpmenu.add_command(label="Sobre", command=help_window)
helpmenu.add_separator()
helpmenu.add_command(label="Fechar", command=fecha_help_window)

# cria area (Frame) com scrollbar para incluir figura
# --------------------------------------------------------------------------------------------------------------------
frame_root = Frame(root, height=560)
frame_root.pack(fill=BOTH, side=LEFT, expand=True)
frame_root['bg'] = backgroud
frame_help = Frame(root, height=560)

# Barra deslizante para filtro de contornos (frame_scalebar)
# -----------------------------------------------------
var_sc = IntVar()
gmin = 0
gmax = 900
Label(frame_root, text='C o n t o r n o s', font=('Ar Delaney', '30', 'bold'), bg=backgroud, fg=foreground).pack()
Label(frame_root, bg=backgroud, width=80).pack()
sc = Scale(frame_root, label='Gera contornos', from_=gmin, to=gmax, length=500, variable=var_sc, orient=HORIZONTAL,
           bg=backgroud, fg=foreground, font='7', command=contornos_cor)
sc_ltext = 'mais linhas          «                        Filtro                        »          menos linhas'
lsc = Label(frame_root, text=sc_ltext, bg=backgroud, fg=foreground, font='7')
sc.pack()
lsc.pack()
Label(frame_root, bg=backgroud, width=80).pack()

# Canvas onde sera carregada a imagem (frame_root)
# -----------------------------------------------------
canvas_root = Canvas(frame_root, bd=3, relief=GROOVE, scrollregion=(0, 0, 100, 100))  # SUNKEN, RAISED, GROOVE, RIDGE
canvas_root.pack(side=TOP, expand=True, fill=BOTH)
vbar_root = Scrollbar(canvas_root, orient=VERTICAL)
vbar_root.pack(side=RIGHT, fill=Y)
vbar_root.config(command=canvas_root.yview)
hbar_root = Scrollbar(canvas_root, orient=HORIZONTAL)
hbar_root.pack(side=BOTTOM, fill=X)
hbar_root.config(command=canvas_root.xview)
canvas_root.config(xscrollcommand=hbar_root.set, yscrollcommand=vbar_root.set)

# Canvas onde sera carregada a Ajuda (frame_help)
# -----------------------------------------------------
canvas_help = Canvas(frame_help, bd=3, relief=GROOVE, scrollregion=(0, 0, 0, 2700))
vbar_help = Scrollbar(frame_help, orient=VERTICAL)
vbar_help.config(command=canvas_help.yview)
canvas_help.config(width=500)
canvas_help.config(yscrollcommand=vbar_help.set)
bt_help = Button(canvas_help, text='X', font='bold', command=fecha_help_window)

estado_inicial_aplicacao()
habilita_desabilita_menu(op_aju_fechar, 0)

root.config(menu=menubar)
root.mainloop()
