"""Gradio front end for the grammar and spell checker.

The correction logic is untouched and still lives in Model.py - this module
only provides the interface. Hugging Face Spaces offers Docker as a paid SDK,
so the Flask version (flask_app.py, with its Dockerfile) is kept for running
locally and this exists to give the project a public URL.
"""
import gradio as gr

from Model import SpellCheckerModule

# Loaded once at import. Spaces keeps the process warm between requests, so the
# 850 MB model is paid for on cold start rather than per correction.
checker = SpellCheckerModule()

# TextBlob.correct() is called per word and is slow - roughly a second for a
# long paragraph - so the input is capped rather than left to time out.
MAX_CHARS = 1200


def correct(text):
    text = (text or "").strip()
    if not text:
        return "", "", "Enter some text to correct."
    if len(text) > MAX_CHARS:
        return "", "", f"Text is {len(text)} characters; the limit is {MAX_CHARS}."

    spelled = checker.correct_spell(text)
    grammared = checker.correct_grammar(spelled)

    changed = []
    if spelled != text:
        changed.append("spelling")
    if grammared != spelled:
        changed.append("grammar")
    note = ("Corrected " + " and ".join(changed) + "."
            if changed else "No changes - the text already looks correct.")
    return spelled, grammared, note


with gr.Blocks(title="Grammar & Spell Checker", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# Grammar &amp; Spell Checker\n"
        "Two passes, because they fail differently. **TextBlob** fixes spelling, "
        "where a dictionary is the right tool. A **T5 grammar model** "
        "(`prithivida/grammar_error_correcter_v1`) fixes grammar, where context "
        "is required."
    )

    with gr.Row():
        with gr.Column():
            src = gr.Textbox(
                label="Your text",
                placeholder="He dont has no idea how many informations was missing.",
                lines=6,
                max_lines=12,
            )
            go = gr.Button("Correct", variant="primary")
        with gr.Column():
            out_spell = gr.Textbox(label="After spelling pass", lines=4, show_copy_button=True)
            out_gram = gr.Textbox(label="After grammar pass", lines=4, show_copy_button=True)
            status = gr.Markdown()

    gr.Examples(
        examples=[
            ["He dont has no idea how many informations was missing from the report."],
            ["She go to schol every day and have a apple for lunch."],
            ["Their going to recieve the packge tommorow morning."],
            ["I has been working on this projet since to years."],
        ],
        inputs=src,
    )

    go.click(correct, inputs=src, outputs=[out_spell, out_gram, status])
    src.submit(correct, inputs=src, outputs=[out_spell, out_gram, status])

if __name__ == "__main__":
    demo.launch()
