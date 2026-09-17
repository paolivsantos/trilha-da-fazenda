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
    .link-btn {
        display: inline-block;
        margin-top: 6px;
        font-size: 11px;
        color: #00ad9d;
        text-decoration: none;
        border: 1px solid #00ad9d;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .link-btn:hover {
        background: #00ad9d;
        color: #121817;
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
    [
        "Visualizar Trilha",
        "👥 Cadastrar Elenco",
        "📅 Adicionar Marco Semanal",
        "⚙️ Configurações",
    ],
)

# 1. ABA DE CONFIGURAÇÕES (ADMIN)
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

# 2. ABA DE CADASTRAR ELENCO
elif aba == "👥 Cadastrar Elenco":
  st.sidebar.subheader("Novo Participante")

  with st.sidebar.form("form_elenco"):
    nome_peao = st.text_input("Nome do Participante")
    status_peao = st.selectbox(
        "Status Inicial", st.session_state["config_status"]
    )
    foto_peao = st.text_input(
        "URL da Foto", placeholder="https://exemplo.com/foto.jpg"
    )

    cadastrar_peao = st.form_submit_button("Cadastrar no Elenco")

    if cadastrar_peao and nome_peao:
      lista = st.session_state["participantes"]
      existe = any(p["nome"].lower() == nome_peao.lower() for p in lista)

      if not existe:
        novo_p = {
            "nome": nome_peao,
            "status": status_peao,
            "foto": (
                foto_peao
                if foto_peao
                else "https://via.placeholder.com/150"
            ),
            "semanas": {},
        }
        lista.append(novo_p)
        salvar_dados(ARQUIVO_DADOS, lista)
        st.sidebar.success(
            f"Participante {nome_peao} adicionado com sucesso!"
        )
      else:
        st.sidebar.error("Já existe um participante com esse nome.")

  st.subheader("👥 Elenco Atual Cadastrado")
  participantes = st.session_state["participantes"]
  if not participantes:
    st.info("Nenhum participante no elenco ainda.")
  else:
    cols_elenco = st.columns(4)
    for idx, p in enumerate(participantes):
      with cols_elenco[idx % 4]:
        st.markdown(
            f"""
                <div style="background: #1a2322; border: 1px solid #283735; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px;">
                    <img src="{p.get('foto', '')}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid #00ad9d; margin-bottom: 8px;">
                    <div style="font-weight: bold; color: #ffffff; font-size: 14px;">{p['nome']}</div>
                    <div style="font-size: 11px; color: #DB8645; text-transform: uppercase; margin-top: 4px;">{p['status']}</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

# 3. ABA DE ADICIONAR MARCO SEMANAL
elif aba == "📅 Adicionar Marco Semanal":
  st.sidebar.subheader("Lançamento da Semana")

  participantes = st.session_state["participantes"]

  if not participantes:
    st.warning(
        "Cadastre pelo menos um participante na aba 'Cadastrar Elenco' antes"
        " de lançar marcos."
    )
  else:
    nomes_participantes = [p["nome"] for p in participantes]

    with st.sidebar.form("form_marco"):
      participante_escolhido = st.selectbox(
          "Selecione o Participante", nomes_participantes
      )

      # Atualizar status geral opcional direto no lançamento
      atualizar_status = st.checkbox(
          "Atualizar status atual do peão?", value=False
      )
      novo_status_peao = st.selectbox(
          "Novo Status", st.session_state["config_status"]
      )

      st.markdown("---")
      semana = st.slider("Semana", 1, 14, 1)
      funcao = st.selectbox(
          "Função / Tarefa (Selo)", st.session_state["config_funcoes"]
      )
      descricao = st.text_area("Descrição do Acontecimento")
      url_link = st.text_input(
          "URL de Referência (Vídeo / Matéria)",
          placeholder="https://R7.com/...",
      )

      salvar_marco = st.form_submit_button("Salvar Marco na Trilha")

      if salvar_marco:
        for p in participantes:
          if p["nome"] == participante_escolhido:
            if atualizar_status:
              p["status"] = novo_status_peao
            if "semanas" not in p:
              p["semanas"] = {}
            # Salvando agora a lista com 3 elementos: [funcao, descricao, url]
            p["semanas"][str(semana)] = [funcao, descricao, url_link]
            break

        salvar_dados(ARQUIVO_DADOS, participantes)
        st.sidebar.success(
            f"Marco da Semana {semana} salvo para {participante_escolhido}!"
        )

  st.subheader("📋 Acompanhamento dos Marcos Lançados")
  if not participantes:
    st.info("Nenhum dado cadastrado.")
  else:
    for p in participantes:
      st.write(f"**{p['nome']}** (Status: *{p['status']}*)")
      semanas = p.get("semanas", {})
      if semanas:
        for s_num, dados_s in sorted(
            semanas.items(), key=lambda x: int(x[0])
        ):
          # Compatibilidade retroativa caso algum dado antigo tenha 2 ou 3 itens
          f_nome = dados_s[0]
          desc = dados_s[1]
          link = dados_s[2] if len(dados_s) > 2 else ""
          st.text(
              f"  - Semana {s_num}: [{f_nome}] {desc} | Link: {link if link else 'Nenhum'}"
          )
      else:
        st.text("  - Nenhum marco cadastrado.")
      st.markdown("---")

# 4. ABA DE VISUALIZAÇÃO
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
      for semana_num, dados_semana in sorted(
          semanas.items(), key=lambda x: int(x[0])
      ):
        func_nome = dados_semana[0]
        desc = dados_semana[1]
        url_link = dados_semana[2] if len(dados_semana) > 2 else ""

        icone = get_icone(func_nome)

        link_html = (
            f'<a href="{url_link}" target="_blank" class="link-btn">🔗 Ver'
            " Detalhes</a>"
            if url_link
            else ""
        )

        with cols[idx % len(cols)]:
          st.markdown(
              f"""
                  <div style="background: #212e2c; border: 1px solid #283735; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                      <div style="font-size: 10px; font-weight: bold; color: #DB8645; text-transform: uppercase;">Semana {semana_num}</div>
                      <div style="margin: 4px 0;"><span class="marco-selo">{icone} {func_nome}</span></div>
                      <div style="font-size: 12px; color: #d1c2a5; margin-top: 4px;">{desc}</div>
                      {link_html}
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
