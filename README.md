# 🤖 Agentic RAG - Multi-Tool Documentation Analyzer

### מערכת RAG מתקדמת לסריקה, אינדוקס וניתוח תיעוד פרויקט שנוצר על ידי כלי Agentic Coding.

---

## 📝 תיאור הפרויקט (Project Overview)
מערכת **Retrieval-Augmented Generation (RAG)** המיועדת לסריקה, אינדוקס וניתוח של תיעוד פרויקט שנוצר על ידי כלי פיתוח מבוססי סוכנים (כמו **Cursor, Claude Code ו-Kiro**). 

המערכת מאחדת את כל קבצי ה-`.md` משכבות שונות של הפרויקט לשכבת ידע אחת, ומאפשרת למפתחים לקבל תובנות מדויקות על החלטות טכניות, חוקי ממשק ומגבלות מערכת מתוך ההקשר המלא של הפרויקט.

---

## 🚀 תכונות עיקריות (Key Features)

* **Multi-Source Ingestion:** סריקה רקורסיבית של תיקיות כלי פיתוח (כגון `.cursor/`, `.claude/`) וזיהוי אוטומטי של המקור ב-Metadata.
* **Agentic Workflow:** ארכיטקטורת **Event-Driven** מבוססת LlamaIndex המפרידה בין שלבי העיבוד ומנהלת אירועים בצורה אסינכרונית.
* **Intelligent Routing:** נתב (Router) לוגי המבדיל בין סוגי שאילתות:
    * **חיפוש סמנטי (Semantic Search):** לשאלות תיאורטיות והבנת הקשר.
    * **חילוץ נתונים מובנה (Structured Extraction):** לשאלות הדורשות רשימות מדויקות, חוקי ממשק או אזהרות חומרה.
* **Modern UI:** ממשק Chat מתקדם ב-**Gradio 6.0+** בעיצוב Glassmorphism מודרני, עם ניגודיות גבוהה לקריאות מקסימלית.

---

## 🛠️ סטאק טכנולוגי (Tech Stack)

* **Framework:** LlamaIndex (Workflows, Ingestion Pipeline).
* **LLM:** Groq (Llama-3.3-70b-versatile).
* **Embeddings:** Cohere Multilingual v3.0 (תמיכה מלאה ב-RTL ובעברית).
* **Vector Database:** ChromaDB - פתרון אחסון מקומי המאפשר עבודה מהירה ושמירה על פרטיות המידע.
* **UI:** Gradio 6.0+.

---

## 📊 ארכיטקטורת ה-Workflow

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
StartEvent: קבלת שאילתה מהמשתמש דרך ממשק ה-Gradio והזרקתה למערכת ה-Workflow.

Router Step: הפעלת לוגיקת LLM לניתוח טקסטואלי וזיהוי כוונת המשתמש (Intent Detection). הנתב מחליט האם השאלה דורשת שליפה רחבה או חילוץ פרטים טכניים ספציפיים.

Execution Paths:

נתיב מובנה (Structured Path): שימוש בסכמת Pydantic מול LLMTextCompletionProgram כדי להפיק רשימות מסודרות (כגון רשימת חוקי עיצוב או אזהרות חומרה).

נתיב סמנטי (Semantic Path): ביצוע שאילתה וקטורית מול ChromaDB המבוססת על Cosine Similarity למציאת פיסות המידע הרלוונטיות ביותר.

Metadata Enrichment: הוספת נתוני מקור (שם קובץ, נתיב וכלי שיצר אותו) לכל פיסת מידע שנשלפה כדי להבטיח שקיפות.

StopEvent: איגוד וסינתזה של המידע לתשובה סופית קוהרנטית והצגתה למשתמש בממשק ה-Chat.

🔍 רפלקציה (Reflection)
מגבלות האג'נט: המערכת פועלת על בסיס "עולם סגור" - היא מוגבלת למידע המתועד בקבצים. היא אינה "מנחשת" מידע שלא קיים (Anti-Hallucination), מה שמבטיח אמינות אך מחייב תיעוד איכותי.

דיוק הניתוב: הנתב מזהה בהצלחה רבה בקשות לרשימות או חוקים. במקרים של שאלות קצרות מדי, הוא עשוי לבחור בחיפוש סמנטי כברירת מחדל כדי להבטיח הבנת הקשר רחב.

אבחון כשלים: קיימת רגישות למידע סותר בין כלים שונים (למשל הנחיית UI שונה ב-Cursor לעומת Claude). שדרוג עתידי יכלול שקלול של "זמן עדכון אחרון" (Timestamp).

חווית פיתוח ובטיחות: הבחירה ב-ChromaDB כבסיס נתונים מקומי הוכחה כנכונה עבור סביבת עבודה מאובטחת (כגון נטפרי), שכן היא מונעת חסימות API ושומרת על פרטיות המידע.

💻 הוראות הרצה (Setup & Run)
1. התקנת הספריות הנדרשות:
Bash
pip install llama-index llama-index-llms-groq llama-index-embeddings-cohere chromadb gradio python-dotenv
2. הגדרת מפתחות API בקובץ .env:
קטע קוד
GROQ_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
3. הרצת היישום:
Bash
python app.py
