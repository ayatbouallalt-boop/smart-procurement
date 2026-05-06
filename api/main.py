from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class RFQRequest(BaseModel):
    fournisseur_nom: str
    produit: str
    quantite: int
    delai_souhaite: int

@app.post("/generate-rfq")
def generate_rfq(req: RFQRequest):
    prompt = f"""
    Rédige un email professionnel de demande de prix (RFQ) en français pour :
    - Fournisseur : {req.fournisseur_nom}
    - Produit : {req.produit}
    - Quantité : {req.quantite}
    - Délai : {req.delai_souhaite} jours
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return {
        "email": response.choices[0].message.content
    }
    