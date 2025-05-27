from shiny.express import input, render, ui
import os
# Interface simples
ui.page_opts(title="Tradutor de Frases para Libras", fillable=True)

ui.input_text("frase", "Digite uma frase:", "")

ui.hr()

with ui.output_ui("imagens"):
    pass

# Dicionário de sinais com imagens próprias
sinais = {
    "oi": "imagens/oi.png",
    "obrigado": "imagens/obrigado.png",
    "amor": "imagens/amor.png"
}

# Função para pegar imagem da letra
def imagem_letra(letra):
    caminho = f"imagens/letras/{letra.upper()}.png"
    if os.path.exists(caminho):
        return caminho
    else:
        return None

@render.ui
def imagens():
    frase = input.frase().lower().split()
    elementos = []

    for palavra in frase:
        if palavra in sinais:
            elementos.append(ui.tags.div(
                ui.tags.p(f"{palavra} (sinal próprio)"),
                ui.tags.img(src=sinais[palavra], height="100px")
            ))
        else:
            elementos.append(ui.tags.p(f"{palavra} (soletrado)"))
            for letra in palavra:
                img = imagem_letra(letra)
                if img:
                    elementos.append(ui.tags.img(src=img, height="50px"))
                else:
                    elementos.append(ui.tags.span(f"[sem imagem: {letra}]"))

    return ui.tags.div(*elementos)