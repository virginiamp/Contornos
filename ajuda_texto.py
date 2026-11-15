"""
Texto da janela de Ajuda do Contornos.

Para alterar a ajuda basta editar o texto abaixo. Marcacoes disponiveis:
    [t]...[/t]   titulo de secao
    [m]...[/m]   nome de menu, botao ou campo (azul e negrito)
    [b]...[/b]   negrito
    [i]...[/i]   italico
    [u]...[/u]   sublinhado
    [e]...[/e]   texto de erro (vermelho)
    [s]...[/s]   referencia a Secao de Erros (vermelho e italico)

Linhas que contem TAB (\t) sao exibidas como tabela: o texto apos o TAB
fica alinhado na segunda coluna, inclusive quando quebra de linha.
"""

TEXTO_AJUDA = """\
[b]CONTORNOS[/b] é um aplicativo que transforma uma imagem escolhida em sua versão apenas com linhas de contorno.

Para isso você deverá abrir sua imagem através do Menu [m]'Arquivo'[/m], e depois selecionar uma das opções de Filtro através do Menu [m]'Ferramentas'[/m]. Se desejar redimensionar sua imagem você poderá fazê-lo [u]antes[/u] da escolha do Filtro.

Enquanto você não abrir sua imagem, apenas algumas opções dos Menus [m]'Arquivo'[/m] e [m]'Ajuda'[/m] estarão habilitadas para seleção.


[t]Descrição do Menu Principal[/t]

Na barra de tarefas é apresentado o Menu Principal que inclui as opções: [m]'Arquivo'[/m], [m]'Ferramentas'[/m] e [m]'Ajuda'[/m].

[b]Menu[/b] [m]'Arquivo'[/m]: selecionando esta opção você poderá escolher entre: [m]'Abrir...'[/m], [m]'Salvar como...'[/m], [m]'Fechar'[/m] e [m]'Sair'[/m]. Veja [i]Descrição do Menu Arquivo[/i] para mais informações.

[b]Menu[/b] [m]'Ferramentas'[/m]: selecionando esta opção você poderá escolher entre: [m]'Desfazer'[/m], [m]'Redimensionar...'[/m], [m]'Filtro Colorido'[/m] e [m]'Filtro Preto e Branco'[/m]. Veja [i]Descrição do Menu Ferramentas[/i] para mais informações.

[b]Menu[/b] [m]'Ajuda'[/m]: selecionando esta opção você poderá escolher entre: [m]'Sobre'[/m] e [m]'Fechar'[/m]. Veja [i]Descrição do Menu Ajuda[/i] para mais informações.


[t]Descrição do Menu Arquivo[/t]

[b]Menu[/b] [m]'Abrir...'[/m]: selecionando esta opção uma janela de diretórios será aberta para que você possa buscar o arquivo de imagem que deseja transformar. A imagem escolhida será carregada na janela principal do aplicativo. Se você fechar a janela de diretórios sem escolher um arquivo, nada será alterado. Caso o aplicativo não consiga abrir seu arquivo uma mensagem de erro será gerada. Veja a [s]Seção de Erros[/s] para mais informações.

[u]Estado inicial:[/u]\tHabilitado.
[u]Habilitado:[/u]\tSempre.
[u]Desabilitado:[/u]\tNunca.
[u]Selecionado:[/u]\tHabilita as opções de Menu:
\t[m]'Arquivo'[/m]
\t   - todas
\t[m]'Ferramentas'[/m]
\t   - [m]'Redimensionar...'[/m]
\t   - [m]'Filtro Colorido'[/m]
\t   - [m]'Filtro Preto e Branco'[/m]
\tDesabilita a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Desfazer'[/m]

[b]Menu[/b] [m]'Salvar como...'[/m]: selecionando esta opção uma janela de diretórios será aberta para que você possa escolher onde deseja salvar a imagem que está carregada na tela principal do aplicativo. O aplicativo permite que a imagem seja salva em formato PNG ou BMP, sendo PNG o formato padrão.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando houver imagem carregada na janela principal do aplicativo.
[u]Desabilitado:[/u]\tQuando não houver imagem carregada na janela principal do aplicativo.
[u]Selecionado:[/u]\tNenhum outro Menu será habilitado ou desabilitado.

[b]Menu[/b] [m]'Fechar'[/m]: selecionando esta opção a imagem carregada na janela principal do aplicativo será fechada.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando houver imagem carregada na janela principal do aplicativo.
[u]Desabilitado:[/u]\tQuando não houver imagem carregada na janela principal do aplicativo.
[u]Selecionado:[/u]\tDesabilita as [m]'barras deslizantes de geração de contornos'[/m] e as opções de Menu:
\t[m]'Arquivo'[/m]
\t   - [m]'Salvar como...'[/m]
\t   - [m]'Fechar'[/m]
\t[m]'Ferramentas'[/m]
\t   - todas

[b]Menu[/b] [m]'Sair'[/m]: selecionando esta opção a aplicação será encerrada fechando todas as janelas.

[u]Estado inicial:[/u]\tHabilitado.
[u]Habilitado:[/u]\tSempre.
[u]Desabilitado:[/u]\tNunca.
[u]Selecionado:[/u]\tNenhum outro Menu será habilitado ou desabilitado.


[t]Descrição do Menu Ferramentas[/t]

[b]Menu[/b] [m]'Desfazer'[/m]: selecionando esta opção a imagem original será carregada novamente na janela principal do aplicativo sem nenhuma modificação.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando alguma mudança na imagem original tiver sido feita através das opções de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Redimensionar...'[/m]
\t   - [m]'Filtro Colorido'[/m]
\t   - [m]'Filtro Preto e Branco'[/m]
[u]Desabilitado:[/u]\tQuando não houver imagem carregada na janela principal do aplicativo.
\tQuando nenhuma mudança na imagem original tiver sido feita e efetivada.
[u]Selecionado:[/u]\tDesabilita as [m]'barras deslizantes de geração de contornos'[/m] e a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Desfazer'[/m]
\tHabilita a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Redimensionar...'[/m]

[b]Menu[/b] [m]'Redimensionar...'[/m]: selecionando esta opção uma nova janela será aberta para que você possa determinar um fator de redimensionamento da sua imagem original.

Na [b]caixa de texto[/b] [m]'Porcentagem:'[/m] você poderá incluir o valor, em porcentagem, que deseja que sua nova imagem tenha em relação à imagem original. O valor padrão é 100, ou seja, nenhuma mudança (100% da imagem original).

O valor inserido deve ser um número inteiro entre 1 e 1000, caso contrário um erro aparecerá abaixo da caixa de texto. Veja a [s]Seção de Erros[/s] para mais informações.

Clicando no [b]botão[/b] [m]'OK'[/m] você confirma a alteração e será mostrada sua nova imagem na janela principal do aplicativo. A janela de redimensionamento permanece aberta.

Clicando no [b]botão[/b] [m]'Cancelar'[/m] será mostrada sua imagem original na janela principal do aplicativo. A janela de redimensionamento permanece aberta.

Clicando no [b]botão[/b] [m]'Fechar'[/m] você fecha a janela de redimensionamento mantendo o estado corrente da sua imagem.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando sua imagem for carregada no aplicativo através da opção de Menu:
\t[m]'Arquivo'[/m]
\t   - [m]'Abrir...'[/m]
[u]Desabilitado:[/u]\tQuando não houver nenhuma imagem carregada na janela principal do aplicativo.
\tQuando sua imagem original for modificada através das opções de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Filtro Colorido'[/m]
\t   - [m]'Filtro Preto e Branco'[/m]
[u]Selecionado:[/u]\tCaso a mudança tenha sido efetivada através do [b]botão[/b] [m]'OK'[/m], habilita a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Desfazer'[/m]
\tCaso a mudança não tenha sido efetivada através do [b]botão[/b] [m]'Cancelar'[/m], desabilita a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Desfazer'[/m]

[b]Menu[/b] [m]'Filtro Colorido'[/m]: selecionando esta opção a imagem carregada na janela principal do aplicativo será transformada numa imagem de contornos com o máximo de linhas encontradas.

A nova imagem terá as linhas coloridas e o fundo preto. Você poderá graduar a quantidade de linhas que deseja que sua imagem apresente mexendo nas [m]'barras deslizantes de geração de contornos'[/m] (gradiente mínimo e gradiente máximo). Quanto mais para a direita as barras, menos linhas terá sua imagem.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando houver uma imagem na janela principal do aplicativo.
[u]Desabilitado:[/u]\tQuando não houver uma imagem na janela principal do aplicativo.
[u]Selecionado:[/u]\tHabilita as [m]'barras deslizantes de geração de contornos'[/m] e a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Desfazer'[/m]
\tDesabilita a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Redimensionar...'[/m]

[b]Menu[/b] [m]'Filtro Preto e Branco'[/m]: selecionando esta opção a imagem carregada na janela principal do aplicativo será transformada numa imagem de contornos com o máximo de linhas encontradas.

A nova imagem terá as linhas pretas e o fundo branco. Você poderá graduar a quantidade de linhas que deseja que sua imagem apresente mexendo nas [m]'barras deslizantes de geração de contornos'[/m] (gradiente mínimo e gradiente máximo). Quanto mais para a direita as barras, menos linhas terá sua imagem.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando houver uma imagem na janela principal do aplicativo.
[u]Desabilitado:[/u]\tQuando não houver uma imagem na janela principal do aplicativo.
[u]Selecionado:[/u]\tHabilita as [m]'barras deslizantes de geração de contornos'[/m] e a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Desfazer'[/m]
\tDesabilita a opção de Menu:
\t[m]'Ferramentas'[/m]
\t   - [m]'Redimensionar...'[/m]


[t]Descrição do Menu Ajuda[/t]

[b]Menu[/b] [m]'Sobre'[/m]: selecionando esta opção esta janela de Ajuda com a descrição do Aplicativo aparecerá no lado direito da janela principal.

[u]Estado inicial:[/u]\tHabilitado.
[u]Habilitado:[/u]\tSempre.
[u]Desabilitado:[/u]\tNunca.
[u]Selecionado:[/u]\tHabilita a opção de Menu:
\t[m]'Ajuda'[/m]
\t   - [m]'Fechar'[/m]

[b]Menu[/b] [m]'Fechar'[/m]: selecionando esta opção a janela de Ajuda será encerrada. O mesmo acontece clicando no [b]botão[/b] [m]'X'[/m] no alto desta janela.

[u]Estado inicial:[/u]\tDesabilitado.
[u]Habilitado:[/u]\tQuando a janela de Ajuda estiver aberta.
[u]Desabilitado:[/u]\tQuando a janela de Ajuda estiver fechada.
[u]Selecionado:[/u]\tDesabilita a opção de Menu:
\t[m]'Ajuda'[/m]
\t   - [m]'Fechar'[/m]


[t]Seção de Erros[/t]

[b]Erros do Menu[/b] [m]'Abrir...'[/m]: uma janela separada será aberta com o número do erro, uma breve descrição do problema e uma sugestão para correção.

[e]ERRO #0! Arquivo não pode ser aberto.[/e]
[e]Provavelmente você está tentando abrir um arquivo que está protegido.[/e]

[e]ERRO #1! Formato desconhecido.[/e]
[e]Provavelmente você está tentando abrir um arquivo que não é de imagem.[/e]

[e]ERRO #2! Desconhecido.[/e]

[b]Erros do Menu[/b] [m]'Redimensionar...'[/m]: o erro irá aparecer embaixo da caixa de texto [m]'Porcentagem:'[/m]. Em todos os casos o erro desaparecerá quando:
   - o [b]botão[/b] [m]'OK'[/m] for clicado e o campo estiver preenchido corretamente;
   - o [b]botão[/b] [m]'Cancelar'[/m] for clicado.

[e]Campo não deve estar vazio![/e]: este erro ocorrerá se a caixa de texto estiver vazia e o [b]botão[/b] [m]'OK'[/m] for clicado.

[e]Valor deve ser nº inteiro![/e]: este erro ocorrerá se a caixa de texto tiver um valor que não seja um número inteiro e o [b]botão[/b] [m]'OK'[/m] for clicado.

[e]Valor deve estar entre 1 e 1000![/e]: este erro ocorrerá se a caixa de texto tiver um número menor que 1 (zero ou negativo) ou maior que 1000 e o [b]botão[/b] [m]'OK'[/m] for clicado.

[e]Porcentagem pequena demais para esta imagem![/e]: este erro ocorrerá se, com a porcentagem escolhida, a nova imagem ficar com menos de 1 pixel de largura ou de altura (por exemplo, 1% de uma imagem pequena).
"""
