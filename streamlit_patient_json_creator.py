import streamlit as st
import json
import os

# Liste des cibles à générer
TARGETS = ["Valorisation", "CCMU", "GEMSA", "CIM10", "CCAM", "Avis Spécialisé"]

# Création d'un dossier de sortie si nécessaire
OUTPUT_DIR = "dossiers_targets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialisation de la session
if 'patients' not in st.session_state:
    st.session_state.patients = []

# Initialisation des prompts systèmes par target
for target in TARGETS:
    if f"system_prompt_{target}" not in st.session_state:
        st.session_state[f"system_prompt_{target}"] = ""

st.title("Créateur de JSONL pour entraînement GPT - Données patients")

st.markdown("""
Cette application vous permet de saisir des dossiers patients avec les éléments classiques d’un dossier d’urgence.
Les données sont ensuite exportées en fichiers `.jsonl` par cible (target) pour entraîner un modèle GPT spécifique à chaque objectif.
""")

# Section de configuration des prompts système
st.sidebar.header("Prompts Système par Target")
for target in TARGETS:
    st.session_state[f"system_prompt_{target}"] = st.sidebar.text_area(
        f"Prompt Système - {target}",
        value=st.session_state[f"system_prompt_{target}"]
    )

# Formulaire principal
with st.form("patient_form"):
    st.subheader("Données d'entrée (Input pour l'I.A)")
    histoire = st.text_area("Histoire de la maladie")
    antecedents = st.text_area("Antécédents")
    traitements = st.text_area("Traitements habituels")
    motif = st.text_area("Motif de recours")
    constantes = st.text_area("Constantes")
    prescriptions = st.text_area("Prescriptions réalisées")
    observations = st.text_area("Observations des urgences")
    conclusion = st.text_area("Conclusion")

    st.subheader("Données de sortie (Target pour l'I.A)")
    target_values = {}
    for target in TARGETS:
        target_values[target] = st.text_input(f"{target}")

    submitted = st.form_submit_button("Ajouter le dossier")

    if submitted:
        dossier = {
            "input": {
                "Histoire de la maladie": histoire,
                "Antécédents": antecedents,
                "Traitements habituels": traitements,
                "Motif de recours": motif,
                "Constantes": constantes,
                "Prescriptions réalisées": prescriptions,
                "Observations des urgences": observations,
                "Conclusion": conclusion
            },
            "target": target_values
        }
        st.session_state.patients.append(dossier)
        st.success("Dossier ajouté avec succès.")

# Affichage du nombre de dossiers
st.info(f"Nombre de dossiers saisis : {len(st.session_state.patients)}")

# Bouton d'export par fichier JSONL
if st.session_state.patients:
    if st.button("Exporter les JSONL par Target"):
        for target in TARGETS:
            prompt = st.session_state[f"system_prompt_{target}"]
            lignes = []
            for dossier in st.session_state.patients:
                input_text = f"Prompt système : {prompt}\n"
                for key, value in dossier["input"].items():
                    input_text += f"{key} : {value}\n"

                output_text = dossier["target"].get(target, "")

                lignes.append(json.dumps({
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": input_text.strip()},
                        {"role": "assistant", "content": output_text}
                    ]
                }, ensure_ascii=False))

            filename = f"{OUTPUT_DIR}/{target.lower().replace(' ', '_')}.jsonl"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(lignes))

            with open(filename, "r", encoding="utf-8") as f:
                st.download_button(
                    label=f"Télécharger {target}.jsonl",
                    data=f.read(),
                    file_name=f"{target.lower().replace(' ', '_')}.jsonl",
                    mime="application/jsonl"
                )
