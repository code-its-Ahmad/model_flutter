import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")

produce_data = {
    "fruits": ["apple", "banana", "orange", "grape", "strawberry", "pear", "cherry"],
    "vegetables": ["carrot", "broccoli", "tomato", "potato", "onion", "cucumber"],
    "weights": ["kg", "kilogram", "kilograms", "half kg", "half kilogram", "dozen", "doz"],
    "ignore_contexts": ["menu", "list", "offering", "selection"]
}

def recognize_produce(sentence):
    doc = nlp(sentence.lower())

    fruits = set(produce_data["fruits"])
    vegetables = set(produce_data["vegetables"])
    all_produce = fruits.union(vegetables)

    results = {}

    for token in doc:
        if token.text in all_produce:
            item = token.text
            item_type = "fruit" if item in fruits else "vegetable"

            if item not in results:
                results[item] = {
                    "item": item,
                    "quantity": None,
                    "weight": "kg", 
                    "type": item_type,
                    "price": None
                }

    return results

def add_quantity_and_price(results, sentence):
    quantity_pattern = r'(\d+(?:\.\d+)?)\s*(kg|kilogram|kilograms|half kg|half kilogram|dozen|doz)?\s*(\w+)'
    price_pattern = r'(\w+)(?:\s+(?:price|cost|is|costs))?\s+(\d+(?:\.\d+)?)\s*(?:dollar|usd|\$)|(\d+(?:\.\d+)?)\s*(?:dollar|usd|\$)(?:\s+(?:for|per))?\s+(\w+)|(\w+)(?:\s+(?:price|cost))?\s+(\d+(?:\.\d+)?)\s*(?:dollar|usd|\$)'

    quantity_matches = re.findall(quantity_pattern, sentence.lower())
    for match in quantity_matches:
        quantity, weight, item = match
        if item in results:
            quantity = float(quantity)
            if results[item]["quantity"] is None:
                results[item]["quantity"] = quantity
            else:
                results[item]["quantity"] += quantity
            if weight:
                results[item]["weight"] = weight

    price_matches = re.findall(price_pattern, sentence.lower())
    for match in price_matches:
        if match[0] and match[1]:
            item, price = match[0], match[1]
        elif match[2] and match[3]:
            price, item = match[2], match[3]
        elif match[4] and match[5]:
            item, price = match[4], match[5]
        else:
            continue

        if item in results:
            results[item]["price"] = float(price)

        dozen_pattern = rf'{item}\s+(?:per|a)?\s*(?:dozen|doz)'
        if re.search(dozen_pattern, sentence.lower()):
            results[item]["weight"] = "dozen"

    return results

def extract_produce_info(sentence):
    results = recognize_produce(sentence)
    results = add_quantity_and_price(results, sentence)
    return list(results.values())

# Test the function with the sample sentence
if __name__ == "__main__":
    test_sentence = "i have 10 kg apple, 1 kg apple price 20 dollar"
    result = extract_produce_info(test_sentence)
    print("Extracted information:")
    print(json.dumps(result, indent=2))
