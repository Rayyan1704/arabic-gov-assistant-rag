# 🤖 Gemini API Setup Guide

## What is Gemini?

Google Gemini is a powerful AI model that can:
- Generate natural language responses in Arabic and English
- Understand context and provide accurate answers
- Cite sources and provide structured information
- **FREE tier available** - No credit card required!

## Step 1: Get Your API Key (5 minutes)

### 1. Visit Google AI Studio
Go to: https://makersuite.google.com/app/apikey

### 2. Sign in with Google Account
Use any Google account (Gmail, etc.)

### 3. Create API Key
- Click "Create API Key"
- Select "Create API key in new project" (or use existing)
- Copy the key (starts with `AIza...`)

### 4. Save Your Key
**Important**: Save this key somewhere safe! You'll need it in the next step.

## Step 2: Configure Your Project (2 minutes)

### 1. Create `.env` File
In your project root, create a file named `.env`:

```bash
# On Windows
copy .env.example .env

# On Mac/Linux
cp .env.example .env
```

### 2. Add Your API Key
Open `.env` and replace `your_api_key_here` with your actual key:

```
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
```

**Important**: 
- Don't share this file!
- Don't commit it to GitHub (already in `.gitignore`)
- Keep it secret!

## Step 3: Test Your Setup (1 minute)

Run the test script:

```bash
python test_gemini.py
```

**Expected output**:
```
Testing Gemini API...
================================================================================

Query: اشرح لي ما هو الذكاء الاصطناعي

Response:
الذكاء الاصطناعي هو فرع من علوم الحاسوب يهدف إلى إنشاء أنظمة...

================================================================================
✅ Gemini API working correctly!
```

If you see this, you're ready to go! 🎉

## Step 4: Use the RAG System

### Option A: Jupyter Notebook (Recommended)
```bash
jupyter notebook notebooks/04_rag_with_gemini.ipynb
```

### Option B: Complete RAG System
```bash
jupyter notebook notebooks/06_complete_rag_system.ipynb
```

### Option C: Python Script
```python
from src.retrieval import RetrieverSystem
from src.llm_generator import AnswerGenerator
from sentence_transformers import SentenceTransformer

# Load components
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
retriever = RetrieverSystem.load_index(...)
generator = AnswerGenerator()

# Ask question
query = "كيف أحصل على رخصة ليموزين؟"
query_emb = model.encode([query])[0]
contexts = retriever.search(query_emb, k=10)
result = generator.generate_answer(query, contexts)

print(result['answer'])
```

## Troubleshooting

### Error: "GEMINI_API_KEY not found"
**Solution**: Make sure you created `.env` file with your API key

### Error: "Invalid API key"
**Solution**: 
1. Check if you copied the full key (starts with `AIza`)
2. Make sure there are no extra spaces
3. Generate a new key if needed

### Error: "API quota exceeded"
**Solution**: 
- Free tier: 60 requests per minute
- Wait a minute and try again
- Or upgrade to paid tier

### Error: "Module not found: google.generativeai"
**Solution**: 
```bash
pip install google-generativeai python-dotenv
```

## API Limits

### Free Tier (No Credit Card)
- **Requests**: 60 per minute
- **Tokens**: 32,000 per minute
- **Cost**: FREE! 🎉

### Paid Tier (Optional)
- **Cost**: ~$0.01 per 100 queries
- **Limits**: Much higher
- **Billing**: Only pay for what you use

For most testing and development, **free tier is enough**!

## Example Queries

Try these in your RAG system:

### Arabic Queries
```
كيف أحصل على رخصة ليموزين؟
ما هي خطوات تسجيل المقررات في جامعة قطر؟
كيف أطلب استشارة طبية عاجلة؟
ما هي متطلبات تقديم العروض للمناقصات؟
كيف أحصل على شهادة من وزارة المواصلات؟
```

### English Queries
```
How do I get a limousine license in Qatar?
What are the steps to register courses at Qatar University?
How do I request an urgent medical consultation?
```

## Security Best Practices

### ✅ DO:
- Keep `.env` file private
- Add `.env` to `.gitignore`
- Use environment variables
- Rotate keys periodically

### ❌ DON'T:
- Commit API keys to GitHub
- Share keys in public
- Hardcode keys in code
- Use same key for production and testing

## Cost Estimation

### Free Tier Usage
- **Your project**: ~34 documents
- **Typical query**: 3 retrieved chunks + answer generation
- **Estimated cost**: FREE (within limits)

### If You Exceed Free Tier
- **100 queries**: ~$0.01
- **1,000 queries**: ~$0.10
- **10,000 queries**: ~$1.00

Very affordable! 💰

## Alternative: Use Without API

If you don't want to use Gemini API, you can use the free version:

```bash
jupyter notebook notebooks/05_rag_no_api.ipynb
```

**Pros**:
- Completely free
- No API needed
- Works offline

**Cons**:
- Returns raw chunks (not natural language)
- Less user-friendly
- No answer synthesis

## Next Steps

Once your API is working:

1. ✅ Test with sample queries
2. ✅ Try the interactive chat
3. ✅ Evaluate answer quality
4. ✅ Deploy as web app (optional)

## Support

### Official Documentation
- [Gemini API Docs](https://ai.google.dev/docs)
- [Python SDK](https://github.com/google/generative-ai-python)

### Common Issues
- [API Key Issues](https://ai.google.dev/docs/api_key)
- [Rate Limits](https://ai.google.dev/docs/rate_limits)
- [Pricing](https://ai.google.dev/pricing)

### Project Issues
- Check `FINAL_SUMMARY.md` for troubleshooting
- Review `DAY2_COMPLETE.md` for setup issues
- Open GitHub issue if stuck

---

**Ready to build amazing AI applications!** 🚀
