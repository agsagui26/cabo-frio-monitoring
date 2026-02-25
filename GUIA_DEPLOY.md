# 🚀 GUIA RÁPIDO - DEPLOY NO GITHUB PAGES

## ⏱️ Tempo: 10 minutos

---

## 📋 ARQUIVOS PARA UPLOAD

Você tem 3 arquivos prontos:

1. ✅ **index.html** (62 KB) - Dashboard completo
2. ✅ **report_data.json** (702 KB) - 1.492 comentários
3. ✅ **README.md** - Documentação

---

## 🔥 PASSO A PASSO

### 1️⃣ Acessar GitHub (1 min)
- Vá para: https://github.com/agsagui26/cabo-frio-monitoring
- Faça login se necessário

### 2️⃣ Deletar Arquivos Antigos (2 min)
1. Clique em `index.html`
2. Clique nos 3 pontinhos (...) > **Delete file**
3. Commit: "Removendo versão antiga"
4. Repita para `report_data.json`

### 3️⃣ Upload dos Novos Arquivos (3 min)
1. Clique em **Add file** > **Upload files**
2. Arraste os 3 arquivos:
   - `index.html`
   - `report_data.json`
   - `README.md`
3. Commit message: "Dashboard v3 FINAL - 1.492 comentários"
4. Clique em **Commit changes**

### 4️⃣ Aguardar Processamento (2 min)
⏳ GitHub está fazendo o deploy automático...

### 5️⃣ Acessar Dashboard (1 min)
1. Vá para: https://agsagui26.github.io/cabo-frio-monitoring/
2. Pressione **Ctrl + Shift + R** (limpar cache)
3. ✅ **PRONTO!**

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Após o deploy, verifique:

- [ ] Dashboard abre sem erros
- [ ] Header mostra "1.492 comentários"
- [ ] KPI "Total" mostra 1.492
- [ ] Ratio mostra 19.1:1
- [ ] Gráfico temporal aparece
- [ ] Mapa de calor funciona
- [ ] 4 abas navegam corretamente
- [ ] Busca funciona
- [ ] Nuvem de palavras clicável
- [ ] Mobile responsivo

---

## 🔄 FUTURAS ATUALIZAÇÕES

Quando tiver novos comentários:

### Opção 1: Via Interface (Mais Fácil)
1. Processe: `python3 process_social_data.py`
2. No GitHub, clique em `report_data.json`
3. Clique no lápis ✏️ (Edit)
4. Cole o novo conteúdo
5. Commit: "Atualização [data]"

### Opção 2: Via GitHub Desktop
1. Clone o repositório
2. Substitua `report_data.json`
3. Commit + Push
4. Dashboard atualiza automaticamente

---

## 🆘 PROBLEMAS COMUNS

### ❌ Dashboard mostra 569 comentários
**Causa:** Arquivo antigo ainda em cache  
**Solução:** Ctrl + Shift + R ou modo anônimo

### ❌ Gráficos não aparecem
**Causa:** Internet lenta ou bloqueador  
**Solução:** Aguardar ou desabilitar AdBlock

### ❌ "404 Not Found"
**Causa:** Arquivo não se chama `index.html`  
**Solução:** Renomear arquivo no GitHub

---

## 📱 COMPARTILHAR

Link para enviar à equipe:
```
https://agsagui26.github.io/cabo-frio-monitoring/
```

---

## ✅ ESTÁ PRONTO!

Seu dashboard profissional com 1.492 comentários está no ar! 🎉

**SAGUI Data Center** • 2026
