from agents.qa_agent import answer_with_rag
from agents.verify_agent import verify_answer
from agents.format_agent import format_output

def route_question(question, vectordb, output_format):
    result = answer_with_rag(question, vectordb)
    verified = verify_answer(result)
    final = format_output(verified, output_format)
    return final
