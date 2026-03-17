# 🤖 Agentic RAG - Multi-Tool Documentation Analyzer

### מערכת RAG מתקדמת לסריקה, אינדוקס וניתוח תיעוד פרויקט שנוצר על ידי כלי Agentic Coding.

---

## 📝 תיאור הפרויקט (Project Overview)
מערכת **Retrieval-Augmented Generation (RAG)** מתקדמת המיועדת לסריקה, אינדוקס וניתוח של תיעוד פרויקט שנוצר על ידי כלי פיתוח מבוססי סוכנים (כמו **Cursor, Claude Code ו-Kiro**). 

המערכת מאחדת את כל קבצי ה-`.md` משכבות שונות של הפרויקט לשכבת ידע אחת, ומאפשרת למפתחים לקבל תובנות מדויקות על החלטות טכניות, חוקי ממשק ומגבלות מערכת מתוך ההקשר המלא של הפרויקט.

---

## 🚀 תכונות עיקריות (Key Features)

* # **Multi-Source Ingestion:** סריקה רקורסיבית של תיקיות כלי פיתוח (כגון `.cursor/`, `.claude/`) וזיהוי אוטומטי של המקור ב-Metadata.
* # **Agentic Workflow:** ארכיטקטורת **Event-Driven** מבוססת LlamaIndex המפרידה בין שלבי העיבוד ומנהלת אירועים בצורה אסינכרונית.
* # **Intelligent Routing:** נתב (Router) לוגי המבדיל בין סוגי שאילתות:
    * ## **חיפוש סמנטי (Semantic Search):** לשאלות תיאורטיות והבנת הקשר.
    * ## **חילוץ נתונים מובנה (Structured Extraction):** לשאלות הדורשות רשימות מדויקות, חוקי ממשק או אזהרות חומרה.
* # **Modern UI:** ממשק Chat מתקדם ב-**Gradio 6.0+** בעיצוב Glassmorphism מודרני, עם ניגודיות גבוהה לקריאות מקסימלית.

---

## 🛠️ סטאק טכנולוגי (Tech Stack)

* # **Framework:** LlamaIndex (Workflows, Ingestion Pipeline).
* # **LLM:** Groq (Llama-3.3-70b-versatile).
* # **Embeddings:** Cohere Multilingual v3.0 (תמיכה מלאה ב-RTL ובעברית).
* # **Vector Database:** ChromaDB - נבחר כפתרון אחסון מקומי המאפשר עבודה מהירה ושמירה על פרטיות המידע ללא תלות בענן חיצוני.
* # **UI:** Gradio 6.0+.

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
### 🔄 תהליך העבודה (Detailed Workflow)

* **StartEvent:** קבלת שאילתה והתחלת תהליך הניתוב האג'נטי.
* **Router Step:** ניתוח טקסטואלי לזיהוי כוונת המשתמש (**Intent Detection**) ובחירת מסלול השליפה.
* **Execution Paths:**
    * **נתיב מובנה:** הפעלת סכמת **Pydantic** מול `LLMTextCompletionProgram` לחילוץ אובייקטים מוגדרים ומדויקים.
    * **נתיב סמנטי:** שליפה וקטורית מ-**ChromaDB** המבוססת על דמיון סמנטי (**Cosine Similarity**).
* **StopEvent:** איגוד התשובה הסופית יחד עם מקורות המידע (**Metadata**) והצגתה בממשק המשתמש.

---

## 🔍 רפלקציה (Reflection)

* **מגבלות האג'נט:** האג'נט מוגבל למידע המתועד בקבצים בלבד. הוא תוכנן לפעול בשיטת **Anti-Hallucination**, ולכן איכות התשובה תלויה ישירות באיכות התיעוד המקורי.
* **דיוק הניתוב:** הנתב מזהה בהצלחה רבה בקשות לרשימות או חוקים. במקרים של שאלות קצרות מדי (למשל "צבע?"), המערכת מעדיפה חיפוש סמנטי כברירת מחדל כדי להבטיח הקשר רחב.
* **אבחון כשלים:** המערכת עלולה להתקשות במתן עדיפות למידע סותר אם קיים כזה בין שני כלים שונים (למשל החלטת עיצוב שונה ב-Cursor וב-Claude). **שדרוג עתידי:** הוספת שקלול של "זמן עדכון אחרון" לכל קובץ.
* **חווית פיתוח:** המעבר ל-**ChromaDB** הוכח כהחלטה נכונה עבור סביבת עבודה מאובטחת ומסוננת (כגון נטפרי), שכן הוא מונע חסימות API מיותרות ושומר על המידע מקומי.

---
    D -.-> G[File Name + Tool Source]
    G -.-> E
    end
