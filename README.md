# 🤖 Agentic RAG - Multi-Tool Documentation Analyzer

### מערכת RAG מתקדמת המאחדת ומנתחת תיעוד פרויקט מכלי Agentic Coding (Cursor, Claude Code, Kiro).

---

## 📝 תיאור הפרויקט (Project Overview)
פרויקט זה מציג מערכת **Retrieval-Augmented Generation (RAG)** המיועדת לסריקה, אינדוקס וניתוח של תיעוד פרויקט שנוצר על ידי סוכני בינה מלאכותית. 

המערכת פותרת את בעיית ה"מידע המפוזר" על ידי איחוד קבצי ה-`.md` מתיקיות שונות (כגון `.cursor/rules`, `.claude/`) לשכבת ידע אחת, ומאפשרת למפתחים לקבל תובנות מדויקות על החלטות ארכיטקטוניות וחוקי פיתוח בזמן אמת.

---

## 🚀 תכונות עיקריות (Key Features)

* **Multi-Source Ingestion:** סריקה אוטומטית של `.cursor/`, `.claude/` ותיקיות פרויקט נוספות.
* **Agentic Workflow:** שימוש ב-LlamaIndex Workflows לניהול אירועים אסינכרוני.
* **Intelligent Routing:** נתב חכם המפריד בין חיפוש סמנטי כללי לבין חילוץ נתונים מובנה (חוקים, רשימות, מגבלות).
* **Modern UI:** ממשק צ'אט מבוסס **Gradio 6.0+** בעיצוב נקי ונגיש.

---

## 🛠️ סטאק טכנולוגי (Tech Stack)

* **Framework:** LlamaIndex
* **LLM:** Groq (Llama-3.3-70b-versatile)
* **Embeddings:** Cohere Multilingual v3.0
* **Vector Database:** ChromaDB (Local & Secure)
* **UI:** Gradio

---

## 📊 תרשים זרימה (Workflow Diagram)

המערכת משתמשת בארכיטקטורת Event-Driven:

```mermaid
graph TD
    A[User Query] --> B{Router Step}
    B -- "Structured Search<br>(Lists/Rules)" --> C[Extraction Pipeline]
    B -- "Semantic Search<br>(General Info)" --> D[Vector DB Retrieval]
    C --> E[Response Synthesizer]
    D --> E
    E --> F[Gradio UI Output]
    
    subgraph "Metadata Enrichment"
    D -.-> G[File Name + Tool Source]
    G -.-> E
    end
⚙️ שלבי העבודה (Detailed Workflow Steps)
# StartEvent: קבלת שאילתה מהמשתמש והזרקתה למערכת.

# Router Step: זיהוי כוונת המשתמש (Intent Detection) – האם הוא מחפש הסבר כללי או רשימה טכנית מוגדרת.

# Execution Paths:

## נתיב מובנה (Structured Path): חילוץ אובייקטים מוגדרים (Pydantic) עבור חוקי ממשק או מגבלות.

## נתיב סמנטי (Semantic Path): שליפה וקטורית מ-ChromaDB המבוססת על דמיון סמנטי.

# Metadata Enrichment: הצמדת מקור המידע (שם הקובץ והכלי) לכל תשובה.

# StopEvent: יצירת תשובה סופית והצגתה בממשק.

🔍 רפלקציה (Reflection)
# אמינות: המערכת פועלת במודל "עולם סגור" למניעת הזיות (Anti-Hallucination).

# דיוק: הנתב מבטיח מענה אופטימלי לסוג השאלה (סמנטי vs מובנה).

# פרטיות: השימוש ב-ChromaDB מקומי מבטיח שהמידע נשאר בתוך הארגון/המחשב האישי.

# אתגרים: המערכת רגישה לסתירות בין קבצי תיעוד שונים, דבר שיטופל בעתיד באמצעות שקלול זמני עדכון.

💡 דוגמאות לשאילתות (Query Examples)
ה-Agent יודע לענות על שאלות כגון:

"מהם חוקי העיצוב (CSS) שהוגדרו עבור רכיבי הכפתורים בפרויקט?"

"האם יש מגבלות חומרה שתועדו בתהליך הפיתוח עם Claude?"

"תמצת לי את החלטות הארכיטקטורה שהתקבלו בתיקיית .cursor."

"הצג רשימה של כל ה-Endpoints של ה-API שתועדו בתיעוד הפנימי."

💻 הוראות הרצה (Setup & Run)
1. התקנת ספריות:
Bash
pip install llama-index llama-index-llms-groq llama-index-embeddings-cohere chromadb gradio python-dotenv
2. הגדרת משתני סביבה (.env):
קטע קוד
GROQ_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
3. הרצת היישום:
Bash
python app.py
