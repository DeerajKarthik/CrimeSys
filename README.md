# CrimeSys: AI-Powered Crime Investigation with Knowledge Graphs

> **Modern, LLM-driven Q&A and graph analytics for crime data, built on Neo4j and the POLE model.**

---

## Features

- **Natural Language Q&A:** Ask complex crime-related questions in plain English.
- **LLM-to-Cypher Translation:** Uses open-source LLMs (LLaMA 3 via Ollama) to generate Cypher queries.
- **Neo4j Knowledge Graph:** Fully integrated with Neo4j Community Edition and the Manchester POLE crime dataset.
- **Interactive Graph Visualization:** Explore people, crimes, locations, and their relationships.
- **Modern, Minimal UI:** Streamlit app with a dark theme, animated answer cards, and a focus on clarity.
- **Explainable AI:** See the generated Cypher, reasoning steps, and a natural language summary for every answer.
- **Predefined & Custom Queries:** Try demo queries or ask your own—explore criminal networks, hotspots, and more.

---

## Example Questions

- “Find people involved in multiple crimes.”
- “What locations saw violent crimes in August 2017?”
- “Show connections between known gang members.”
- “Which officer is investigating the most open cases?”

---

## Tech Stack

- **Frontend:** Streamlit (custom dark theme, responsive, animated)
- **Backend:** Python, LangChain (or minimal LLM interface)
- **LLM:** LLaMA 3 (via Ollama), Mistral (optional)
- **Database:** Neo4j Community Edition
- **Visualization:** pyvis, networkx
- **Dataset:** [Manchester POLE crime dataset](https://github.com/neo4j-graph-examples/pole)

---

## Setup & Installation

### 1. **Clone the Repository**

```bash
git clone https://github.com/deerajkarthik/crimesys.git
cd crimesys
```

### 2. **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Set Up Neo4j and Import the POLE Dataset**

#### **Install Neo4j Community Edition**

```bash
# For Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 5' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
```

#### **Start Neo4j**

```bash
sudo systemctl enable neo4j
sudo systemctl start neo4j
```

#### **Set the Password**

```bash
# Default user: neo4j, default password: neo4j
cypher-shell -u neo4j -p neo4j "ALTER CURRENT USER SET PASSWORD FROM 'neo4j' TO 'crime12345';"
# Or, if first time:
neo4j-admin set-initial-password crime12345
```

#### **Download and Import the POLE Dataset**

```bash
git clone https://github.com/neo4j-graph-examples/pole.git
cd pole
cypher-shell -u neo4j -p crime12345 < import/cypher/create-schema.cypher
cypher-shell -u neo4j -p crime12345 < import/cypher/import-nodes.cypher
cypher-shell -u neo4j -p crime12345 < import/cypher/import-relationships.cypher
```

**Dataset Source:**  
[Manchester POLE crime dataset (Neo4j Graph Examples)](https://github.com/neo4j-graph-examples/pole)

---

### 4. **Set Up Ollama and LLaMA 3**

#### **Install Ollama**

See [Ollama installation instructions](https://ollama.com/download) for your OS.

#### **Download LLaMA 3 Model**

```bash
ollama pull llama3
```

#### **Start Ollama**

```bash
ollama serve
```

Ollama should be running at `http://localhost:11434`.

---

### 5. **Run the App**

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

- Enter a natural language question about crimes, people, locations, or relationships.
- Try the example queries for inspiration.
- View the answer, graph visualization, and technical details for each query.

---

## Data Model

This project uses the **POLE (Person, Object, Location, Event)** schema, with nodes like:
- `Person`, `Crime`, `Location`, `Officer`, `Object`, `Vehicle`, `Phone`, `Email`, `PostCode`, `Area`
and relationships like:
- `PARTY_TO`, `OCCURRED_AT`, `INVESTIGATED_BY`, `INVOLVED_IN`, `FAMILY_REL`, `KNOWS`, etc.

See the [POLE dataset repo](https://github.com/neo4j-graph-examples/pole) for full details.

---

## Author

Built by [Deeraj](https://www.linkedin.com/in/s-k-deeraj/) — AI enthusiast.

---

## ⭐️ Why CrimeSys?

CrimeSys is a showcase of modern AI, graph data, and UX—perfect for your portfolio, a data science demo, or as a foundation for real-world investigative tools.

---

## 📄 License

MIT License.  
Dataset: [Manchester POLE crime dataset](https://github.com/neo4j-graph-examples/pole) (public domain).
