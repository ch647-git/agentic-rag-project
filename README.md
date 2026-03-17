🤖 Agentic RAG - Multi-Tool Documentation Analyzer
מערכת RAG (Retrieval-Augmented Generation) מתקדמת המיועדת לסריקה, אינדוקס וניתוח של תיעוד פרויקט שנוצר על ידי כלי Agentic Coding (כמו Cursor, Claude Code ו-Kiro).

המערכת מאחדת את כל קבצי ה-.md משכבות שונות של הפרויקט לשכבת ידע אחת, ומאפשרת למפתחים לקבל תובנות מדויקות על החלטות טכניות, חוקי ממשק ומגבלות מערכת מתוך ההקשר המלא של הפרויקט.

🚀 תכונות עיקריות (Key Features)
Multi-Source Ingestion: סריקה רקורסיבית של תיקיות כלי פיתוח (כגון .cursor/, .claude/) וזיהוי אוטומטי של המקור ב-Metadata.

Agentic Workflow: ארכיטקטורת Event-Driven מבוססת LlamaIndex המפרידה בין שלבי העיבוד ומנהלת אירועים בצורה אסינכרונית.

Intelligent Routing: נתב (Router) לוגי המבדיל בין סוגי שאילתות:

חיפוש סמנטי (Semantic Search): לשאלות תיאורטיות והבנת הקשר.

חילוץ נתונים מובנה (Structured Extraction): לשאלות הדורשות רשימות מדויקות, חוקי ממשק או אזהרות חומרה.

Modern UI: ממשק Chat מתקדם ב-Gradio בעיצוב Glassmorphism מודרני, עם ניגודיות גבוהה לקריאות מקסימלית.

🛠️ סטאק טכנולוגי (Tech Stack)
Framework: LlamaIndex (Workflows, Ingestion Pipeline).

LLM: Groq (Llama-3.3-70b-versatile).

Embeddings: Cohere Multilingual v3.0 (תמיכה מלאה ב-RTL ובעברית).

Vector Database: ChromaDB - נבחר כפתרון אחסון מקומי המאפשר עבודה מהירה ושמירה על פרטיות המידע ללא תלות בענן חיצוני.

UI: Gradio 6.0+.

📊 ארכיטקטורת ה-Workflow
קטע קוד
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
הפרויקט מבוסס על זרימת עבודה (Workflow) מונעת אירועים:

StartEvent: קבלת שאילתה והתחלת תהליך הניתוב.

Router Step: ניתוח טקסטואלי לזיהוי כוונת המשתמש (Intent Detection).

Execution Paths:

נתיב מובנה: הפעלת סכמת Pydantic מול LLMTextCompletionProgram לחילוץ אובייקטים מוגדרים.

נתיב סמנטי: שליפה וקטורית מ-ChromaDB המבוססת על דמיון סמנטי (Cosine Similarity).

StopEvent: איגוד התשובה עם מקורות המידע (Metadata) והצגתה בממשק.

🔍 רפלקציה (Reflection)
מגבלות האג'נט: האג'נט מוגבל למידע המתועד בקבצים. הוא אינו "מנחש" מידע שלא קיים (Anti-Hallucination) ולכן איכות התשובה תלויה ישירות באיכות התיעוד של כלי הקידוד.

דיוק הניתוב: הנתב מזהה בהצלחה רבה בקשות לרשימות או חוקים. במקרים של שאלות קצרות מדי (למשל "צבע?"), הוא עשוי לבחור בחיפוש סמנטי כברירת מחדל.

אבחון כשלים: המערכת עלולה להתקשות במתן עדיפות למידע סותר אם קיים כזה בין שני כלים שונים (למשל החלטת עיצוב שונה ב-Cursor וב-Claude). שדרוג עתידי יכלול שקלול של "זמן עדכון אחרון".

חווית פיתוח: המעבר ל-ChromaDB הוכח כנכון עבור סביבת עבודה מאובטחת (כגון נטפרי), שכן הוא מונע חסימות API מיותרות מול שרתי ענן וקטוריים.

💻 הוראות הרצה
התקינו את הספריות הנדרשות:


pip install llama-index llama-index-llms-groq llama-index-embeddings-cohere chromadb gradio python-dotenv
הגדירו מפתחות API בקובץ .env:

קטע קוד
GROQ_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
הריצו את היישום:


python app.py