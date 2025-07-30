import streamlit as st
import pandas as pd
from recherche_concours_selenium import get_concours_with_selenium

st.title("📅 Concours FFE — Résultats Automatiques")

with st.spinner("🔍 Récupération des concours depuis ffecompet.ffe.com..."):
    concours = get_concours_with_selenium()

if not concours:
    st.error("❌ Aucun concours trouvé.")
else:
    df = pd.DataFrame(concours)

    # 🧪 Optionnel : filtrer par discipline contenant une lettre (ex: 'E')
    filtre = st.text_input("Filtrer les disciplines (ex: E, P, D, ...)", value="")

    if filtre:
        df = df[df["disciplines"].str.contains(filtre, case=False, na=False)]

    # ✅ Affichage triable
    st.dataframe(
        df.sort_values(by="date", ascending=True),
        use_container_width=True
    )

    st.success(f"{len(df)} concours affichés")
