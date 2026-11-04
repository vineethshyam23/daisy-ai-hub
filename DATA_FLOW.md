# Data Flow

## 1. Standard AI Tool Request

A user submits an email to the Email Assistant:

```
Browser
  │
  ├─ [1] User types email content, selects tone + reply type
  ├─ [2] Frontend calls POST /email/reply
  │       Headers: Authorization: Bearer <api-token>
  │       Body: { email_content, tone, reply_type, length, priority, ... }
  │
Backend (FastAPI)
  │
  ├─ [3] auth middleware: validates Bearer token against cached Secret Manager value
  ├─ [4] route: routes/email.py receives request, instantiates EmailService()
  ├─ [5] service: services/email_service.py loads prompt template from config/prompt.yml
  ├─ [6] LLM module: modules/llm.py calls vertexai.GenerativeModel.generate_content()
  ├─ [7] Vertex AI Gemini returns completion
  │
  └─ [8] Response: { content: "Dear..." } → Frontend renders reply
```

**Latency**: 2-8 seconds depending on input length. No streaming in v1 (Gemini response is buffered before returning).

---

## 2. Multi-Modal Document Analysis

A user uploads a PDF to the Document Analyzer:

```
Browser
  │
  ├─ [1] User uploads PDF (or image) + types a question
  ├─ [2] Frontend sends POST /productivity/document-analysis
  │       Body: multipart/form-data with file + instruction_text
  │
Backend
  │
  ├─ [3] auth middleware validates token
  ├─ [4] route validates file type (PDF, PNG, JPG, WEBP) and size
  ├─ [5] service: reads file bytes into memory
  ├─ [6] LLM module: assembles Gemini Parts:
  │         Part.from_text(prompt_template + instruction)
  │         Part.from_data(file_bytes, mime_type)  ← inline document
  ├─ [7] Gemini processes text + document together
  │
  └─ [8] Response: structured analysis with citations → Frontend renders
```

**Key pattern**: documents are sent inline (not stored in GCS) for simplicity. For large files or high volume, GCS + GCS URI would be the right move.

---

## 3. Auth Flow (login)

```
Browser
  │
  ├─ [1] User enters email + password on /login
  ├─ [2] Firebase Auth SDK: signInWithEmailAndPassword()
  ├─ [3] Firebase returns ID token (JWT, 1 hour expiry)
  ├─ [4] Pinia auth store: saves user object + token
  │
  └─ [5] All subsequent Firebase/Firestore calls use this ID token automatically
         (Firebase SDK handles refresh)
```

The Firebase ID token is **not** sent to the FastAPI backend. Backend auth uses a separate shared Bearer token.

---

## 4. Image Generation

```
Browser
  │
  ├─ [1] User enters prompt, selects aspect ratio + count
  ├─ [2] Frontend sends POST /images/generate
  │
Backend
  │
  ├─ [3] auth validated
  ├─ [4] modules/image_generation.py calls:
  │       ImageGenerationModel.from_pretrained("imagen-4.0-generate-001")
  │       .generate_images(prompt, number_of_images, aspect_ratio)
  ├─ [5] Vertex AI Imagen 4 returns image bytes
  ├─ [6] Backend base64-encodes each image
  │
  └─ [7] Response: { images: ["data:image/png;base64,..."] }
         Frontend renders inline
```

---

## 5. Invoice Validation

```
Browser
  │
  ├─ [1] User uploads two Excel files: invoice + Jira export
  ├─ [2] Frontend sends POST /invoice-validator/validate
  │
Backend
  │
  ├─ [3] auth validated
  ├─ [4] modules/invoice_validator.py:
  │         Reads invoice sheet (Deckblatt tab)
  │         Reads Jira export
  │         Loads product code mapping from config/para.py
  │         Cross-references line items by product code
  │         Flags mismatches: missing items, quantity discrepancies, unrecognized codes
  ├─ [5] Generates annotated Excel output (colour-coded mismatches via openpyxl)
  │
  └─ [6] Response: base64-encoded Excel file → Frontend triggers download
```

This is entirely local computation — no AI model involved. Gemini is not called.

---

## Token and Secret Flow

```
Cloud Run Backend startup
  │
  ├─ auth.py: __init__ reads config/gcp.yml → gets secret_name + project_number
  ├─ Calls Secret Manager API: projects/{number}/secrets/{name}/versions/latest
  ├─ Stores token in self.api_token (in-memory, process lifetime)
  │
Per-request
  │
  └─ verify_api_token(): compares Authorization header value to self.api_token
                         401 if missing or mismatch
```

**Rotation**: update the secret value in Secret Manager, restart the Cloud Run instance. No redeployment needed.
