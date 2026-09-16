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

# Arquivos JSON locais para persistência
ARQUIVO_DADOS = "dados_trilha.json"


def carregar_dados(arquivo, padrao):
  if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
      return json.load(f)
  return padrao


def salvar_dados(arquivo, dados):
  with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)


# Configurações padrão iniciais caso os arquivos não existam
status_padrao = ["No Jogo", "Eliminado", "Finalista", "Expulso", "Desistente"]
funcoes_padrao = [
    "Chapéu do Fazendeiro",
    "Trato dos Bichos",
    "Limpeza",
    "Horta",
    "Na Roça",
]

# Inicializa estados
if "participantes" not in st.session_state:
  st.session_state["participantes"] = carregar_dados(ARQUIVO_DADOS, [])
if "config_status" not in st.session_state:
  st.session_state["config_status"] = carregar_dados(
      "config_status.json", status_padrao
  )
if "config_funcoes" not in st.session_state:
  st.session_state["config_funcoes"] = carregar_dados(
      "config_funcoes.json", funcoes_padrao
  )

# Título do App
st.title("🤠 Trilha da Roça - A Fazenda")
st.markdown("Painel de gerenciamento, configuração e linha do tempo dos peões.")

# --- PAINEL LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Painel de Controle")
aba = st.sidebar.radio(
    "Navegação",
    ["Visualizar Trilha", "Cadastrar / Editar Peão", "⚙️ Configurações"],
)

# 1. ABA DE CONFIGURAÇÕES (ADMIN COM EDIÇÃO INTELIGENTE E EXCLUSÃO)
if aba == "⚙️ Configurações":
  st.subheader("⚙️ Gerenciamento de Status e Funções")

  col_cfg1, col_cfg2 = st.columns(2)

  # --- GERENCIAR STATUS ---
  with col_cfg1:
    st.markdown("### 📊 Status Permitidos")
    novo_status = st.text_input("Novo Status", key="input_novo_status")
    if st.button("Adicionar Status"):
      if (
          novo_status
          and novo_status not in st.session_state["config_status"]
      ):
        st.session_state["config_status"].append(novo_status)
        salvar_dados("config_status.json", st.session_state["config_status"])
        st.success(f"Status '{novo_status}' adicionado!")
        st.rerun()

    st.markdown("---")
    st.write("Editar ou remover status existentes:")

    for i, s_atual in enumerate(st.session_state["config_status"]):
      c1, c2, c3 = st.columns([3, 1, 1])
      with c1:
        edit_status = st.text_input(
            f"Editar Status {i}",
            value=s_atual,
            key=f"edit_status_{i}",
            label_visibility="collapsed",
        )
      with c2:
        # O botão só fica habilitado se o texto digitado for diferente do valor original salvo
        is_changed_status = edit_status.strip() != s_atual
        if st.button(
            "💾 Salvar",
            key=f"save_status_{i}",
            disabled=not is_changed_status,
        ):
          if edit_status:
            st.session_state["config_status"][i] = edit_status.strip()
            salvar_dados(
                "config_status.json", st.session_state["config_status"]
            )
            st.success("Atualizado!")
            st.rerun()
      with c3:
        if st.button("🗑️ Excluir", key=f"del_status_{i}"):
          if len(st.session_state["config_status"]) > 1:
            st.session_state["config_status"].pop(i)
            salvar_dados(
                "config_status.json", st.session_state["config_status"]
            )
            st.warning("Removido!")
            st.rerun()
          else:
            st.error("Mínimo de 1 status exigido.")

  # --- GERENCIAR FUNÇÕES / SELOS ---
  with col_cfg2:
    st.markdown("### 🏷️ Funções / Selos")
    nova_funcao = st.text_input("Nova Função", key="input_nova_funcao")
    if st.button("Adicionar Função"):
      if (
          nova_funcao
          and nova_funcao not in st.session_state["config_funcoes"]
      ):
        st.session_state["config_funcoes"].append(nova_funcao)
        salvar_dados("config_funcoes.json", st.session_state["config_funcoes"])
        st.success(f"Função '{nova_funcao}' adicionada!")
        st.rerun()

    st.markdown("---")
    st.write("Editar ou remover funções existentes:")

    for j, f_atual in enumerate(st.session_state["config_funcoes"]):
      cf1, cf2, cf3 = st.columns([3, 1, 1])
      with cf1:
        edit_funcao = st.text_input(
            f"Editar Função {j}",
            value=f_atual,
            key=f"edit_funcao_{j}",
            label_visibility="collapsed",
        )
      with cf2:
        # O botão só fica habilitado se o texto digitado for diferente do valor original salvo
        is_changed_funcao = edit_funcao.strip() != f_atual
        if st.button(
            "💾 Salvar",
            key=f"save_funcao_{j}",
            disabled=not is_changed_funcao,
        ):
          if edit_funcao:
            st.session_state["config_funcoes"][j] = edit_funcao.strip()
            salvar_dados(
                "config_funcoes.json", st.session_state["config_funcoes"]
            )
            st.success("Atualizado!")
            st.rerun()
      with cf3:
        if st.button("🗑️ Excluir", key=f"del_funcao_{j}"):
          if len(st.session_state["config_funcoes"]) > 1:
            st.session_state["config_funcoes"].pop(j)
            salvar_dados(
                "config_funcoes.json", st.session_state["config_funcoes"]
            )
            st.warning("Removido!")
            st.rerun()
          else:
            st.error("Mínimo de 1 função exigida.")

# 2. ABA DE CADASTRO / EDIÇÃO
elif aba == "Cadastrar / Editar Peão":
  st.sidebar.subheader("Novo Momento do Peão")

  with st.sidebar.form("form_cadastro"):
    nome = st.text_input("Nome do Participante")

    # Select populado pelas configurações dinâmicas
    status = st.selectbox(
        "Status do Participante", st.session_state["config_status"]
    )
    foto = st.text_input("URL da Foto do Peão")

    st.markdown("---")
    semana = st.slider("Semana", 1, 14, 1)

    # Select populado pelas funções dinâmicas cadastradas
    funcao = st.selectbox(
        "Função / Tarefa (Selo)", st.session_state["config_funcoes"]
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
          p["semanas"][str(semana)] = [funcao, descricao]
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
            "semanas": {str(semana): [funcao, descricao]},
        }
        lista.append(novo_p)

      salvar_dados(ARQUIVO_DADOS, lista)
      st.sidebar.success(
          f"Registro da Semana {semana} salvo para {nome} com sucesso!"
      )

# 3. ABA DE VISUALIZAÇÃO
else:
  st.subheader("📋 Linha do Tempo Ativa")

  participantes = st.session_state["participantes"]

  if not participantes:
    st.info(
        "Nenhum participante cadastrado ainda. Use a barra lateral para"
        " começar."
    )


  def get_icone(texto_funcao):
    t = texto_funcao.lower()
    if "fazendeiro" in t or "chapéu" in t:
      return "🤠"
    elif any(
        x in t
        for x in [
            "bichos",
            "animal",
            "vaca",
            "cavalo",
            "ave",
            "porco",
            "trato",
        ]
    ):
      return "🐄"
    elif "limpeza" in t or "limpar" in t or "lixo" in t:
      return "🧹"
    elif "horta" in t or "planta" in t or "cultivo" in t:
      return "🌱"
    elif "roça" in t or "indicação" in t or "votação" in t:
      return "🔥"
    elif "festa" in t or "vip" in t:
      return "🎉"
    return "⭐"


  for p in participantes:
    status_texto = p.get("status", "No Jogo")
    is_no_jogo = any(
        s in status_texto.lower() for s in ["no jogo", "campeão", "finalista"]
    )
    badge_class = "status-badge no-jogo" if is_no_jogo else "status-badge"

    st.markdown(
        f"""
      <div class="participante-card">
          <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px; border-bottom: 2px dashed #283735; padding-bottom: 12px;">
              <img src="{p.get('foto', '')}" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 3px solid #00ad9d;">
              <div>
                  <h3 style="margin: 0 0 5px 0; color: #ffffff;">{p['nome']}</h3>
                  <span class="{badge_class}">{status_texto}</span>
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
      for semana_num, (func_nome, desc) in sorted(
          semanas.items(), key=lambda x: int(x[0])
      ):
        icone = get_icone(func_nome)
        with cols[idx % len(cols)]:
          st.markdown(
              f"""
                  <div style="background: #212e2c; border: 1px solid #283735; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                      <div style="font-size: 10px; font-weight: bold; color: #DB8645; text-transform: uppercase;">Semana {semana_num}</div>
                      <div style="margin: 4px 0;"><span class="marco-selo">{icone} {func_nome}</span></div>
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
