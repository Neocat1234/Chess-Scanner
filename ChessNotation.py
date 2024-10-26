import re
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Set your Azure Form Recognizer endpoint and key
endpoint = "https://....cognitiveservices.azure.com/"
key = "..."

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

def analyze_layout():
    # Sample document URL
    formUrl = "https://uscf1-nyc1.aodhosting.com/CL-AND-CR-ALL/CL-ALL/1946/1946_09_1.pdf"

    # Create an instance of DocumentAnalysisClient
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Analyze the document layout
    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-layout", formUrl
    )
    result = poller.result()

    # Initialize an empty list to store chess moves
    chess_moves = []

    # Iterate over the extracted lines from the document
    for page in result.pages:
        for line in page.lines:
            print("Extracted line content:", line.content)  # Debugging
            # Check if the line contains chess notation
            if re.match(r"\b[PpRrNnBbQqKk][x-]?[a-h][1-8]\b", line.content):
                # Extract chess notation moves using regex pattern matching
                moves = re.findall(r"\b[PpRrNnBbQqKk][x-]?[a-h][1-8]\b", line.content)
                print("Extracted chess moves:", moves)  # Debugging
                # Add the extracted moves to the list
                chess_moves.extend(moves)

    # Extract the result of the game
    game_result = extract_game_result(result)

    # Convert old notation to algebraic notation
    algebraic_moves = [convert_to_algebraic(move) for move in chess_moves]

    # Print or store the extracted chess moves and game result
    print("Extracted Chess Moves (Algebraic Notation):")
    for move in algebraic_moves:
        print(move)
    print("\nGame Result:", game_result)

def extract_game_result(result):
    # Iterate over the lines and extract the game result
    for page in result.pages:
        for line in page.lines:
            # Check if the line contains the game result
            if "White wins" in line.content:
                return "White wins"
            elif "Black wins" in line.content:
                return "Black wins"
            elif "Draw" in line.content:
                return "Draw"
    return "Result not found"

if __name__ == "__main__":
    analyze_layout()
