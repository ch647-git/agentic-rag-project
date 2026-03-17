import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import chromadb

# LlamaIndex Core & Workflow
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.workflow import StartEvent, StopEvent, Workflow, step
from llama_index.core.program import LLMTextCompletionProgram

# Connectors
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.groq import Groq
import gradio as gr

# 1. טעינת הגדרות
load_dotenv()

# הגדרת מודלים
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = CohereEmbedding(api_key=os.getenv("COHERE_API_KEY"), model_name="embed-multilingual-v3.0")

# --- שלב א': הכנת הנתונים ---
reader = SimpleDirectoryReader("./my_app_project", recursive=True, exclude_hidden=False)
raw_docs = reader.load_data()

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=50),
        Settings.embed_model,
    ]
)
nodes = pipeline.run(documents=raw_docs)

db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("final_modern_rag")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(nodes, storage_context=storage_context)
query_engine = index.as_query_engine(similarity_top_k=3)

# --- שלב ג': סכמה לחילוץ נתונים ---
class TechDecision(BaseModel):
    title: str = Field(description="כותרת ההחלטה")
    summary: str = Field(description="תמצית ההחלטה")
    source_tool: str = Field(description="הכלי המקור")

class UIRule(BaseModel):
    rule: str = Field(description="חוק הממשק")
    scope: str = Field(description="היקף היישום")

class WarningItem(BaseModel):
    area: str = Field(description="אזור רגיש")
    message: str = Field(description="תיאור האזהרה")
    severity: str = Field(description="חומרה")

class ExtractionSchema(BaseModel):
    decisions: List[TechDecision]
    rules: List[UIRule]
    warnings: List[WarningItem]

# --- שלב ב' + ג': Workflow אג'נטי ---
class AgenticRAG(Workflow):
    @step
    async def process_request(self, ev: StartEvent) -> StopEvent:
        query = ev.query
        structured_keywords = ["רשימה", "החלטות", "כללים", "חוקים", "אזהרות"]
        
        if any(word in query.lower() for word in structured_keywords):
            program = LLMTextCompletionProgram.from_defaults(
                output_cls=ExtractionSchema,
                prompt_template_str="חלץ מידע מהטקסט:\n{context}",
                llm=Settings.llm
            )
            all_text = "\n".join([d.text for d in raw_docs])
            data = program(context=all_text)
            res = "📋 **נתונים מובנים שחולצו:**\n\n"
            for d in data.decisions: res += f"🔹 **{d.title}**: {d.summary}\n"
            for r in data.rules: res += f"📏 **כלל**: {r.rule}\n"
            for w in data.warnings: res += f"⚠️ **{w.area}**: {w.message}\n"
            return StopEvent(result=res)
        else:
            response = query_engine.query(query)
            sources = set()
            for node in response.source_nodes:
                file_name = node.metadata.get('file_name', 'Unknown')
                path = node.metadata.get('file_path', '')
                tool = "Cursor" if ".cursor" in path else "Claude"
                sources.add(f"📄 `{file_name}` ({tool})")
            final_res = f"{str(response)}\n\n---\n**מקורות:**\n" + "\n".join(sources)
            return StopEvent(result=final_res)

# --- 5. עיצוב GRADIO מעודכן לגרסה 6.0 ---
async def run_agent(message, history):
    wf = AgenticRAG(timeout=60)
    return str(await wf.run(query=message))

custom_css = """
.gradio-container { background: linear-gradient(135deg, #020617 0%, #1e1b4b 100%) !important; }
#title-text { text-align: center; color: #ffffff !important; margin-bottom: 20px; }
.message.user { background: linear-gradient(90deg, #3b82f6, #2563eb) !important; color: white !important; border-radius: 15px !important; }
.message.bot { background: rgba(255, 255, 255, 0.1) !important; color: white !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 15px !important; }
footer {display: none !important}
"""

# בגרסה החדשה, הגדרות העיצוב עוברות ל-launch()
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Agentic Intelligence Hub", elem_id="title-text")
    gr.Markdown("### סריקת תיעוד פרויקט וקבלת תובנות בזמן אמת", elem_id="title-text")
    
    gr.ChatInterface(
        fn=run_agent,
        examples=["מה צבע האפליקציה?", "תן לי רשימת החלטות טכניות"]
    )

if __name__ == "__main__":
    # כאן אנחנו מעבירים את ה-css וה-theme כפי שהאזהרה ביקשה
    demo.launch(css=custom_css, theme=gr.themes.Soft())