from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j"

def connect_neo4j():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return driver

def run_cypher(driver, cypher_query: str):
    with driver.session() as session:
        result = session.run(cypher_query)
        return [record.data() for record in result] 

if __name__ == "__main__":
    driver = connect_neo4j()
    result = run_cypher(driver, "MATCH (n) RETURN n LIMIT 5")
    print("Sample nodes:", result)
    driver.close()