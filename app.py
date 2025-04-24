from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Inserisci qui la tua API Key
openai.api_key = ("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")

# Prompt system avanzato con benchmark e riferimento ai valori OMI
system_prompt = """
Sei un consulente esperto in budgeting immobiliare. Il tuo compito è aiutare un real estate manager a costruire un budget base zero, partendo da dati raccolti tramite una survey.

Utilizza i seguenti benchmark tecnici, espressi in €/mq, per stimare i costi delle varie voci. Considera la superficie indicata, i servizi attivi, la presenza geografica, il modello operativo e gli investimenti previsti.

Benchmark di riferimento (€ / mq):

| Ambito | Voce di Costo | Ordinaria | Straordinaria | Totale | % TCO |
|--------|----------------|-----------|----------------|--------|--------|
| HARD   | SPECIALI       | 1.27      | 0.22           | 1.49   | 0.35%  |
| HARD   | ARREDI         | 0.29      | 1.81           | 2.10   | 0.50%  |
| HARD   | EDILE          | 0.35      | 1.75           | 2.10   | 0.50%  |
| SOFT   | PULIZIE        | 6.00      | 0.50           | 6.50   | 1.20%  |
| SOFT   | MANUTENZIONE   | 8.00      | 1.50           | 9.50   | 1.50%  |
| SOFT   | RECEPTION      | 5.00      | 0.00           | 5.00   | 0.90%  |

📍 Per il RENT, considera i valori di riferimento OMI (Osservatorio del Mercato Immobiliare dell'Agenzia delle Entrate), in funzione di:
- Destinazione d'uso (es. Uffici, Commerciale, Sanità…)
- Localizzazione geografica
- Grado di centralità (centrale / semicentrale / periferica)

🧠 Se un dato è mancante, fai un’ipotesi ragionevole basata su settore, superficie, distribuzione geografica e modello operativo.

Output atteso:
- TCO stimato: €XXX.XXX
- ➤ RENT: €XX.XXX — [es. 220€/mq x 500mq, valori OMI Uffici in zona CENTRO]
- ➤ OPEX: €XX.XXX — [es. Pulizie + Manutenzione su 500mq con benchmark 28€/mq]
- ➤ CAPEX: €XX.XXX — [es. Investimenti arredi 150€/mq su 300mq]
- ➤ Costi di Governo: €XX.XXX — [es. Governance mista + CAFM = 5% del TCO]

Fornisci anche:
- Commento finale con ipotesi e suggerimenti di ottimizzazione
"""

@app.route('/api/gpt', methods=['POST'])
def get_budget():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        result = response['choices'][0]['message']['content']
        return jsonify({"result": result})

    except Exception as e:
        print(f"Errore nel backend: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
