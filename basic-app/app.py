from shiny import App, ui, reactive, render
from htmltools import TagList

dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

app_ui = ui.page_fluid(
    ui.tags.style(
        """
        body {
            background: #f5f8fc;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        .linha-flex {
            display: flex;
            gap: 40px;
            justify-content: center;
            align-items: flex-start;
            margin-top: 32px;
        }
        .coluna-inputs {
            min-width: 280px;
            max-width: 340px;
            flex: 1;
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.07);
            padding: 32px 24px 24px 24px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }
        .coluna-grade {
            min-width: 350px;
            flex: 2;
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.07);
            padding: 24px;
        }
        h2 {
            text-align: center;
            margin-top: 32px;
            margin-bottom: 12px;
            color: #1967d2;
            letter-spacing: 1px;
        }
        label {
            color: #222;
            font-weight: 500;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 8px;
            font-size: 1em;
            outline: none;
            margin-top: 3px;
            box-sizing: border-box;
        }
        input[type="text"]:focus, input[type="number"]:focus {
            border-color: #1967d2;
        }
        .shiny-input-checkboxgroup label {
            font-weight: 400;
            margin-left: 3px;
        }
        .btn-primary {
            background: #1967d2;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 10px 0;
            font-size: 1.08em;
            cursor: pointer;
            font-weight: 600;
            transition: background .2s;
            margin-top: 10px;
        }
        .btn-primary:hover {
            background: #1652b9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            box-shadow: 0 2px 8px rgba(25,103,210,0.06);
        }
        th, td {
            border: 1px solid #e0e7ef;
            padding: 10px 7px;
            text-align: center;
        }
        th {
            background-color: #e7f1fa;
            color: #1652b9;
        }
        td {
            background: #f8fafc;
        }
        @media (max-width: 900px) {
            .linha-flex {
                flex-direction: column;
                align-items: stretch;
                gap: 18px;
            }
            .coluna-grade {
                min-width: unset;
            }
        }
        """
    ),
    ui.h2("Organizador de Estudos"),
    ui.div(
        ui.div(
            ui.input_text("atividade1", "Atividade 1", ""),
            ui.input_text("atividade2", "Atividade 2", ""),
            ui.input_text("atividade3", "Atividade 3", ""),
            ui.input_text("atividade4", "Atividade 4", ""),
            ui.input_text("atividade5", "Atividade 5", ""),
            ui.input_checkbox_group("dias", "Dias disponíveis", choices=dias_semana),
            ui.input_numeric("horas_dia", "Horas disponíveis por dia", value=2, min=1, max=10),
            ui.input_action_button("gerar", "Gerar Grade", class_="btn-primary"),
            class_="coluna-inputs"
        ),
        ui.div(
            ui.output_ui("tabela_grade"),
            class_="coluna-grade"
        ),
        class_="linha-flex"
    )
)

def server(input, output, session):
    @reactive.calc
    def grade():
        if input.gerar() == 0:
            return None

        atividades = [a for a in [
            input.atividade1(), input.atividade2(), input.atividade3(),
            input.atividade4(), input.atividade5()] if a.strip()]

        dias = input.dias()
        horas = int(input.horas_dia())
        if not atividades or not dias or horas <= 0:
            return None

        grade = {}
        total_slots = len(dias) * horas
        atividades_repetidas = (atividades * ((total_slots // len(atividades)) + 1))[:total_slots]

        idx = 0
        for dia in dias:
            grade[dia] = []
            for _ in range(horas):
                grade[dia].append(atividades_repetidas[idx])
                idx += 1
        return grade

    @output
    @render.ui
    def tabela_grade():
        g = grade()
        if not g:
            return ui.div("Preencha as informações e clique em 'Gerar Grade'.")

        horas = input.horas_dia()
        headers = [ui.tags.th("Hora " + str(h+1)) for h in range(horas)]
        body_rows = []

        for dia, atividades in g.items():
            cells = [ui.tags.td(atividade) for atividade in atividades]
            row = ui.tags.tr([ui.tags.th(dia)] + cells)
            body_rows.append(row)

        tabela = ui.tags.table(
            [ui.tags.thead(ui.tags.tr([ui.tags.th("Dia")] + headers)),
             ui.tags.tbody(body_rows)]
        )
        return TagList(tabela)

app = App(app_ui, server)
