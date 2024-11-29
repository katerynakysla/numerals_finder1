import gradio as gr
import re

patterns = [
    r'\b\w*багат\w*|\w*мало\b',
    r'\b\w*багац\w*\b',
    r'\bобо\w*\b',
    r'\b\w*кільк\w*\b',
    r'\bпівтор\w+\b',
    r'\b\w*льйон\w*\b',
    r'\b\w*льярд\w*\b',
    r'\bтисяч\w*\b',
    r'\bнул\w+\b',
    r'\b(сто|ста|сотн\w+|сотен\w*)\b',
    r'\b(одн\w*|один\w*|один)\b',
    r'\b\w*два|двом|дві|\w*двох\w*\b',
    r'\b(три|три\w+|трьох\w*|трьом\w*|тре\w+|трі\w+|тро\w+)\b',
    r'\bчотир\w+\b',
    r"\bп['’ʼ]ят\w*\b",
    r'\b(шіст\w+|шест\w+)\b',
    r'\b(сім\w*|сем\w+)\b',
    r'\b(вісім\w*|восьм\w+|вісьм\w+)\b',
    r"\bдев['’ʼ]ят\w*\b",
    r"\bдев['’ʼ]ян\w*\b",
    r'\b\w*десят\w+\b',
    r'\w+дцят\w+\b',
    r'\b(сорок|сорок\w+)\b',
    r'\b(\w*перш\w+|\w*друг\w+|\w*четвер\w+|\w*шост\w+|\w*сьом\w+|\w*восьм\w+|\w*девʼят\w+|\w*девʼян\w+|\w*сот\w+|\w*тисяч\w+|\w*пʼят\w+)\b',
    r'\b(половин\w+|трет\w+|чверт\w+|ціл\w+)\b',
]

def find_numerals(text):
    numerals_found = []
    temp_group = []

    text = re.sub(r"[’ʼ]", "'", text)

    text_lower = text.lower()

    words = re.findall(r"[a-zа-яіїєґ'’ʼ]+|[.,!?;]", text_lower, re.IGNORECASE)

    for word in words:
        matched = False
        for pattern in patterns:
            if re.fullmatch(pattern, word.strip(",.!?;-_*@#$%^&")):
                matched = True
                temp_group.append(word.strip(",.!?;-_*@#$%^&"))
                break
        
        if not matched and temp_group:
            numerals_found.append(' '.join(temp_group))
            temp_group = []

    if temp_group:
        numerals_found.append(' '.join(temp_group))

    return numerals_found

def process_text(text):
    if not text.strip():
        return "❗ Будь ласка, введіть текст!"
    numerals = find_numerals(text)
    if numerals:
        return f"✅ Знайдено числівники: {', '.join(numerals)}"
    else:
        return "❌ Числівників не знайдено."

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.HTML("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&display=swap');

            h1 {
                font-family: 'Dela Gothic One', sans-serif;
                color: #333;
                text-align: center;
                font-size: 3rem;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            }

            .gradio-button:hover {
                background-color: #45a049;
                transition: background-color 0.3s ease, transform 0.2s ease;
                transform: scale(1.1);
            }

            .gradio-container {
                opacity: 0;
                animation: fadeIn 1s forwards;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .gradio-textbox:focus {
                border: 2px solid #4CAF50;
                box-shadow: 0 0 10px rgba(76, 175, 80, 0.7);
                transition: all 0.3s ease;
            }
        </style>
        """)

        gr.HTML("<h1>Пошук числівників</h1>")

        text_input = gr.Textbox(
            placeholder="Введіть текст...",
            label="",
            show_label=False,
            lines=5,
            max_lines=4,
            scale=2
        )

        text_output = gr.Textbox(
            label="",
            show_label=False,
            lines=5,
            max_lines=4,
            scale=2
        )

        search_button = gr.Button("Шукати", size="lg", scale=5)

        search_button.click(process_text, inputs=text_input, outputs=text_output)

    demo.launch(share=True)