import json
import os
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Trilha da Roça - Gerenciador", page_icon="🤠", layout="wide"
)

# Estilização CSS personalizada com a paleta de cores (#00ad9d e #DB8645)
st.markdown(
    """
    <style>
    .main {
        background-color: #121817;
        color: #f4e8d1;
    }
    .participante-card {
        background: #1a2322;
        border: 2px solid #283735;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        background: #DB8645;
        color: #fff;
    }
    .status-badge.no-jogo {
        background: #00ad9d;
        color: #121817;
    }
    .marco-selo {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 173, 157, 0.15);
        border: 1px solid #00ad9d;
        color: #00ad9d;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Arquivo JSON local para persistência dos dados
ARQUIVO_DADOS = "dados_trilha.json"


def carregar_dados():
  if os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
      return json.load(f)
  return []


def salvar_dados(dados):
  with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)


# Carrega os participantes
if "participantes" not in st.session_state:
  st.session_state["participantes"] = carregar_dados()

# Título do App
st.title("🤠 Trilha da Roça - A Fazenda")
st.markdown(
    "Painel de gerenciamento e visualização da linha do tempo dos peões."
)

# --- PAINEL LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Gerenciamento")
aba = st.sidebar.radio("Navegação", ["Visualizar Trilha", "Cadastrar / Editar"])

if aba == "Cadastrar / Editar":
  st.sidebar.subheader("Novo Momento do Peão")

  with st.sidebar.form("form_cadastro"):
    nome = st.text_input("Nome do Participante")
    status = st.selectbox(
        "Status Atual", ["No Jogo", "Eliminado", "Finalista", "Expulso"]
    )
    foto = st.text_input("URL da Foto do Peão")

    st.markdown("---")
    semana = st.slider("Semana", 1, 14, 1)
    tipo_acao = st.selectbox(
        "Tipo de Ação (Selo)",
        [
            "Chapéu do Fazendeiro",
            "Trato dos Bichos",
            "Limpeza",
            "Horta",
            "Na Roça",
            "Outro",
        ],
    )
    descricao = st.text_area("Descrição do Acontecimento")

    enviar = st.form_submit_button("Salvar na Trilha")

    if enviar and nome:
      lista = st.session_state["participantes"]
      encontrado = False

      for p in lista:
        if p["nome"].lower() == nome.lower():
          p["status"] = status
          if foto:
            p["foto"] = foto
          if "semanas" not in p:
            p["semanas"] = {}
          p["semanas"][str(semana)] = [tipo_acao, descricao]
          encontrado = True
          break

      if not encontrado:
        novo_p = {
            "nome": nome,
            "status": status,
            "foto": (
                foto
                if foto
                else "https://via.placeholder.com/150"
            ),
            "semanas": {str(semana): [tipo_acao, descricao]},
        }
        lista.append(novo_p)

      salvar_dados(lista)
      st.sidebar.success(
          f"Registro da Semana {semana} salvo para {nome} com sucesso!"
      )

# --- ÁREA PRINCIPAL ---
st.subheader("📋 Linha do Tempo Ativa")

participantes = st.session_state["participantes"]

if not participantes:
  st.info(
      "Nenhum participante cadastrado ainda. Use a barra lateral para"
      " começar."
  )


def get_icone(tipo):
  t = tipo.lower()
  if "fazendeiro" in t or "chapéu" in t:
    return "🤠"
  elif "bichos" in t:
    return "🐄"
  elif "limpeza" in t:
    return "🧹"
  elif "horta" in t:
    return "🌱"
  elif "roça" in t:
    return "🔥"
  return "⭐"


for p in participantes:
  is_no_jogo = any(
      s in p["status"].lower() for s in ["no jogo", "campeão", "finalista"]
  )
  badge_class = "status-badge no-jogo" if is_no_jogo else "status-badge"

  st.markdown(
      f"""
    <div class="participante-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px; border-bottom: 2px dashed #283735; padding-bottom: 12px;">
            <img src="{p.get('foto', '')}" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 3px solid #00ad9d;">
            <div>
                <h3 style="margin: 0 0 5px 0; color: #ffffff;">{p['nome']}</h3>
                <span class="{badge_class}">{p['status']}</span>
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  semanas = p.get("semanas", {})
  if semanas:
    cols = st.columns(min(len(semanas), 4))
    idx = 0
    for semana_num, (tipo_acao, desc) in sorted(
        semanas.items(), key=lambda x: int(x[0])
    ):
      icone = get_icone(tipo_acao)
      with cols[idx % len(cols)]:
        st.markdown(
            f"""
                <div style="background: #212e2c; border: 1px solid #283735; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: bold; color: #DB8645; text-transform: uppercase;">Semana {semana_num}</div>
                    <div style="margin: 4px 0;"><span class="marco-selo">{icone} {tipo_acao}</span></div>
                    <div style="font-size: 12px; color: #d1c2a5; margin-top: 4px;">{desc}</div>
                </div>
                """,
            unsafe_allow_html=True,
        )
      idx += 1
  else:
    st.markdown(
        "<p style='color: #bfa888; font-size: 12px;'>Nenhum marco cadastrado"
        " para este participante.</p>",
        unsafe_allow_html=True,
    )
