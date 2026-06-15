"""Gradio-Oberfläche für die Erdlinge-Auswertungsskripte.

Jedes CLI-Skript ist als eigener Tab verfügbar. Auf jedem Tab können die
benötigten Dateien hochgeladen werden; per "Ausführen" wird die jeweilige
``process``-Funktion ausgeführt und die erzeugte Excel-Datei sowie die
Log-Ausgabe zurückgegeben. Die Kernlogik der Skripte bleibt unverändert.
"""

import contextlib
import datetime
import io
import os
import tempfile
import traceback

import gradio as gr

import aag_erstattungen
import abrechnungen
import ag_belastung
import lohnjournal
import kontoabgleich_gls
import kontoabgleich_paypal


def _paths(files):
    """Normalisiert die von Gradio gelieferten Datei-Referenzen zu Pfaden."""
    if not files:
        return []
    if not isinstance(files, list):
        files = [files]
    return [f if isinstance(f, str) else f.name for f in files]


def _run(fn, files, out_name, **kwargs):
    """Führt eine ``process``-Funktion aus und fängt stdout als Log ein."""
    buf = io.StringIO()
    try:
        paths = _paths(files)
        if not paths:
            raise OSError("Bitte mindestens eine Datei hochladen.")
        tmpdir = tempfile.mkdtemp(prefix="erdlinge_")
        out_path = os.path.join(tmpdir, out_name)
        with contextlib.redirect_stdout(buf):
            result = fn(paths, output_path=out_path, **kwargs)
        return result, buf.getvalue()
    except Exception as exc:  # noqa: BLE001 - Fehler sollen im Log landen
        buf.write(f"\nFEHLER: {exc}\n")
        buf.write(traceback.format_exc())
        return None, buf.getvalue()


def _make_tab(label, description, fn, out_name, with_year=True, file_types=(".pdf",), single_file=False):
    with gr.Tab(label):
        gr.Markdown(description)
        with gr.Row():
            with gr.Column():
                files = gr.File(
                    label="Datei hochladen" if single_file else "Dateien hochladen",
                    file_count="single" if single_file else "multiple",
                    file_types=list(file_types),
                )
                year = gr.Dropdown(choices=[str(y) for y in range(2022, 2041)], value=str(datetime.date.today().year), label="Jahr") if with_year else None
                btn = gr.Button("Ausführen", variant="primary")
            with gr.Column():
                out_file = gr.File(label="Ergebnis (Excel)")
                logs = gr.Textbox(label="Protokoll", lines=15)

        if with_year:
            btn.click(
                lambda f, y: _run(fn, f, out_name.replace(".xlsx", f"_{y}.xlsx"), year=y),
                inputs=[files, year],
                outputs=[out_file, logs],
            )
        else:
            btn.click(
                lambda f: _run(fn, f, out_name),
                inputs=[files],
                outputs=[out_file, logs],
            )


def build_app():
    with gr.Blocks(title="Erdlinge Skripte", theme=gr.themes.Default(primary_hue=gr.themes.colors.green), analytics_enabled=False) as demo:
        gr.Markdown("# Erdlinge Skripte\nLade die Dokumente hoch und klicke auf **Ausführen**.")

        _make_tab(
            "AAG Erstattungen",
            "PDF(s) der AAG-Erstattungen hochladen. Ergebnis: Excel mit U1- und U2-Tabelle.",
            aag_erstattungen.process,
            "AAG_Erstattungen.xlsx",
            with_year=False,
        )
        _make_tab(
            "Verdienstabrechnungen",
            "PDF(s) der Gehaltsabrechnungen hochladen.",
            abrechnungen.process,
            "abrechnungen.xlsx",
        )
        _make_tab(
            "AG Belastung",
            "Genau ein PDF der AG-Belastung hochladen (Dateiname = Monat).",
            ag_belastung.process,
            "ag_belastung.xlsx",
            with_year=False,
            single_file=True,
        )
        _make_tab(
            "Lohnjournal",
            "Genau ein PDF des Lohnjournals hochladen.",
            lohnjournal.process,
            "lohnjournal.xlsx",
            with_year=False,
            single_file=True,
        )
        _make_tab(
            "Kontoabgleich GLS",
            "GLS-Konto-CSV und GLS-Buchhaltungs-XLSX hochladen.",
            kontoabgleich_gls.process,
            "kontoabgleich_gls.xlsx",
            with_year=False,
            file_types=(".csv", ".xls", ".xlsx"),
        )
        _make_tab(
            "Kontoabgleich PayPal",
            "PayPal-Konto-CSV und PayPal-Buchhaltungs-XLSX hochladen.",
            kontoabgleich_paypal.process,
            "kontoabgleich_paypal.xlsx",
            with_year=False,
            file_types=(".csv", ".xls", ".xlsx"),
        )

    return demo


if __name__ == "__main__":
    build_app().launch()
