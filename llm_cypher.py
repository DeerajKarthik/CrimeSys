import requests
import json
import re

def fix_cypher(cypher: str) -> str:
    
    cypher = cypher.strip()

    cypher = re.sub(r"```cypher", "", cypher)
    cypher = re.sub(r"```", "", cypher)

    cypher = re.sub(r"^(A|Answer):", "", cypher.strip(), flags=re.IGNORECASE).strip()

    cypher = re.sub(r'\[:(\w+)\|(\w+)\]', r'[:\1|:\2]', cypher)

    cypher = cypher.replace('GROUP BY', 'WITH')

    cypher = cypher.rstrip(';')

    return cypher.strip()


def nl_to_cypher(query: str, schema: str = None) -> str:
    """
    Converts natural language query to Cypher using Ollama + LLM.
    """
    prompt = f"""You are an expert Cypher query generator for a Neo4j crime investigation knowledge graph using the POLE schema.

Use the following strict schema:

Node labels: AREA, Crime, Email, Location, Object, Officer, Person, Phone, PhoneCall, PostCode, Vehicle  
Relationships: CALLED, CALLER, CURRENT_ADDRESS, FAMILY_REL, HAS_EMAIL, HAS_PHONE, HAS_POSTCODE, INVESTIGATED_BY, INVOLVED_IN, KNOWS, KNOWS_LW, KNOWS_PHONE, LOCATION_IN_AREA, OCCURRED_AT, PARTY_TO, POSTCODE_IN_AREA  
Property keys: address, age, areaCode, badge_no, call_date, call_duration, call_time, call_type, charge, code, data, date, description, email_address, id, last_outcome, latitude, longitude, make, model, name, nhs_no, note, phoneNo, postcode, rank, reg, rel_type, source_id, style, surname, type, year

Cypher Syntax Guidelines:
- Use MATCH and alias nodes (e.g., (p:Person), (c:Crime))
- Use WITH for aggregations (no GROUP BY)
- Use only the given node labels, relationships, and property keys
- Return readable fields (e.g., p.name, c.type)
- Do not include markdown or formatting in your output
- Do not prefix with "A:", "Answer:", etc.
- Output only the final Cypher query, starting directly with MATCH or CALL

Example queries:

Q: What type of crimes were committed?  
MATCH (c:Crime)  
RETURN c.type AS crime_type, count(*) AS total  
ORDER BY total DESC

Q: Which location node had the most crimes?
A:
MATCH (c:Crime)-[:OCCURRED_AT]->(l:Location)
WITH l, count(c) AS total_crimes
RETURN l.address AS location, total_crimes AS crime_rate
ORDER BY crime_rate DESC
LIMIT 1

Q: Which address had the most crimes?
A:
MATCH (c:Crime)-[:OCCURRED_AT]->(l:Location)
RETURN l.address AS location, count(*) AS crime_count
ORDER BY crime_count DESC
LIMIT 1

Q: Which people are involved in more than 2 crimes?  
MATCH (p:Person)-[:PARTY_TO]->(c:Crime)  
WITH p, count(c) AS crime_count  
WHERE crime_count > 2  
RETURN p.name, p.surname, crime_count  
ORDER BY crime_count DESC

Q: Who are the people that know at least 2 others involved in crimes?  
MATCH (p:Person)-[:KNOWS]->(friend:Person)-[:PARTY_TO]->(:Crime)  
WITH p, count(DISTINCT friend) AS criminal_friends  
WHERE criminal_friends >= 2  
RETURN p.name, p.surname, criminal_friends  
ORDER BY criminal_friends DESC

User question: {query}
"""

    payload = {
        "model": "mistral:latest",  # or llama3:latest
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        cypher = data.get("response") or data.get("message")
        if not cypher:
            raise ValueError("No Cypher query returned by LLM.")

        return fix_cypher(cypher)

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "// Error: Could not generate Cypher query."

def results_to_nl(query: str, cypher: str, results: list) -> str:
    
    prompt = f"""
You are a helpful assistant. Given the user's question, the Cypher query, and the results, summarize the answer in clear, concise natural language.

User question: {query}
Cypher query: {cypher}
Results: {results}

Answer:
"""
    payload = {
        "model": "mistral:latest",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("response") or data.get("message")
        if not answer:
            raise ValueError("No answer returned by LLM.")
        answer = answer.strip().replace('Answer:', '').replace('A:', '').strip()
        return answer
    except Exception as e:
        print(f"[LLM NL ERROR] {e}")
        return "(Could not generate a natural language summary.)"
