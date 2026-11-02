# 🤖 QAgent Local — Lightweight Text-Triggered Multi-Agent System

Un système d'orchestration multi-agents léger, prévisible et **100% local** conçu pour s'affranchir des limitations du *function calling* (JSON halluciné) sur les petits modèles de langage (7B-8B).

---

## 🎯 Porquoi ce projet ?

L'intégration de frameworks lourds (comme CrewAI ou LangChain) avec des modèles locaux légers via Ollama entraîne souvent des erreurs de syntaxe JSON lors des appels d'outils (*MCP / stdio*). 

**QAgent** résout ce problème en remplaçant la couche de *function calling* complexe par un **pattern de commande textuelle (ReAct)** :
1. L'**Orchestrateur** (`Qwen 2.5 7B`) formule sa stratégie et émet des intentions sous forme de balises simples (`[READ: path]`).
2. Le **script Python** intercepte ces balises, gère l'I/O du disque dur de manière déterministe et sécurisée.
3. Le **Coder** (`Qwen 2.5-Coder 7B`) reçoit le contexte brut et génère le code sans surcouche ni pollution.

---

## 🏗️ Architecture du Système

```text
               ┌──────────────────────────────┐
               │    Instruction Utilisateur   │
               └──────────────┬───────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │       Orchestrateur       │
                │       (Qwen 2.5 7B)       │
                └─────────────┬─────────────┘
                              │ Émet [READ: ...]
                              ▼
                ┌───────────────────────────┐
                │   Python Execution Engine │
                │  (Lecture I/O sur disque) │
                └─────────────┬─────────────┘
                              │ Injection du contexte
                              ▼
                ┌───────────────────────────┐
                │           Coder           │
                │    (Qwen 2.5-Coder 7B)    │
                └─────────────┬─────────────┘
                              │ Extraction du Markdown
                              ▼
                ┌───────────────────────────┐
                │   Sauvegarde Auto Python  │
                │   (Mise à jour du fichier)│
                └───────────────────────────┘
```

---

## 📂 Structure du Répertoire

```text
.
├── qagent.py            # Script d'orchestration Python léger
├── test/
│   └── factorielle.py   # Exemple de fichier de test à analyser/corriger
└── README.md            # Documentation du projet
```

---

## 🛠️ Prérequis & Configuration

### 1. Dépendances Python
Le script utilise uniquement la bibliothèque officielle `ollama` :

```bash
pip install -r requirements.txt
```

### 2. Modèles Ollama
Assure-toi que les deux modèles nécessaires sont téléchargés sur ton instance Ollama :

```bash
ollama pull qwen2.5:7b
ollama pull qwen2.5-coder:7b
```

---

## 🚀 Guide d'Utilisation

Le script accepte directement des instructions en langage naturel via la ligne de commande.

### 1. Modifier ou corriger un fichier existant
```bash
python3 qagent.py "Analyse et corrige le fichier test/factorielle.py"
```

### 2. Créer un nouveau script de zéro
```bash
python3 qagent.py "Crée un script Python test/test_factorielle.py pour tester la fonction factorielle"
```

### 3. Demander une analyse ou une refactorisation
```bash
python3 qagent.py "Optimise la gestion des exceptions dans test/factorielle.py"
```

---

## 🔍 Exemple d'Exécution (Terminal)

```text
🚀 [Orchestrateur] Analyse de la demande : 'Corrige le fichier test/factorielle.py'

--- Réponse Orchestrateur ---
1. Identification du fichier : [READ: test/factorielle.py]
2. Analyse de la logique et correction via le codeur.

📂 [Python] Lecture automatique de : test/factorielle.py
💻 [Coder] Délégation de la production de code à Qwen-Coder...

--- Prompt envoyé au Coder ---
Contexte technique : ... (contenu lu) ...
Instructions : Corrige le fichier test/factorielle.py

--- Code généré par le Coder ---
```python
def factorielle(n):
    if n == 1: 
        return 1 
    elif n < 0: 
        raise ValueError(f"{n} est négatif, la factorielle n'est pas définie")
    else: 
        return n * factorielle(n - 1)
```

💾 [Python] Enregistrement automatique dans : test/factorielle.py
✅ Fichier test/factorielle.py mis à jour et enregistré avec succès !
```