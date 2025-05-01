import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Carga variables de entorno desde .env (debe contener OPENAI_API_KEY)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ No se encontró OPENAI_API_KEY en el entorno")

# Crea el cliente de OpenAI
client = OpenAI(api_key=api_key)

def run_prompt(input_file: str, output_file: str):
    """
    Lee un prompt, lo envía a GPT-4 y guarda la respuesta.
    """
    prompt_text = Path(input_file).read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_text}],
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()
    Path(output_file).write_text(result, encoding="utf-8")
    print(f"✅ Generado -> {output_file}")

if __name__ == "__main__":
    # Mapeo entrada → salida
    base_in  = Path(__file__).parent / "prompts"
    base_out = Path(__file__).parent / "responses"

    prompts = {
        "doc_prompt.md":         "doc_response.md",
        "userstories_prompt.md": "userstories_response.md",
        "testcases_prompt.md":   "testcases_response.md"
    }

    # Itera y genera cada archivo de salida
    for inp, outp in prompts.items():
        in_path  = base_in  / inp
        out_path = base_out / outp
        run_prompt(str(in_path), str(out_path))