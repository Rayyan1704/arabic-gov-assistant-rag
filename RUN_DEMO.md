# 🚀 Running the Demo App

## Quick Start

```bash
# 1. Install dependencies (if not already done)
pip install streamlit

# 2. Run the app
streamlit run app.py
```

**Access**: http://localhost:8501

## What You'll See

### Main Interface
- **Query input**: Enter Arabic or English questions
- **Settings sidebar**: Configure retrieval options
- **Example queries**: Click to try pre-made queries

### Features

#### 1. Category Detection
When you enter a query, the system automatically detects the category:
```
Query: "كيف أحصل على رخصة ليموزين؟"
→ Detected category: transportation
```

#### 2. Reranking
Two-stage retrieval for better accuracy:
- Stage 1: Get 20 candidates (fast)
- Stage 2: Rerank to top 5 (accurate)

#### 3. AI Answer Generation
Natural language answers powered by Gemini:
```
Q: كيف أحصل على رخصة ليموزين؟
A: للحصول على رخصة الليموزين في قطر، يجب عليك:
   1. زيارة موقع وزارة المواصلات
   2. تجهيز المستندات المطلوبة...
```

#### 4. Source Attribution
Shows which documents were used:
- File name
- Category
- Similarity score
- Full content

## Settings

### Category Detection
- **Enabled**: Searches within detected category only
- **Disabled**: Searches all documents

### Reranking
- **Enabled**: Uses cross-encoder for better ranking (~50ms slower)
- **Disabled**: Uses embedding similarity only (faster)

### AI Answer
- **Enabled**: Generates natural language answer with Gemini
- **Disabled**: Shows retrieved documents only

### Number of Sources
- Slider: 1-10 sources
- Default: 3 sources

## Example Queries

Try these queries in the app:

### Transportation
```
كيف أحصل على رخصة ليموزين في قطر؟
```

### Education
```
ما هي خطوات تسجيل المقررات في جامعة قطر؟
```

### Health
```
كيف أطلب استشارة طبية عاجلة؟
```

### Business
```
كيف أقدم عروض المناقصات؟
```

### Mixed (English)
```
How do I get a limousine license in Qatar?
```

## Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "GEMINI_API_KEY not found"
- Create `.env` file with your API key
- Or disable "Generate AI answer" in settings

### Error: "File not found: index/embeddings.npy"
- Run notebooks in order to generate indexes
- See `START_HERE.md` for setup instructions

### App is slow
- Disable reranking for faster results
- Reduce number of sources
- First load is slower (models loading)

## Performance

### Speed
- **Category detection**: <1ms
- **Embedding search**: <1ms
- **Reranking**: ~50ms
- **AI generation**: ~2-3 seconds

### Accuracy
- **Without reranking**: ~85% P@1
- **With reranking**: ~95% P@1
- **Category-specific**: +5% improvement

## Screenshots

Take screenshots of:
1. Main interface with query
2. Search results with AI answer
3. Category detection in action
4. Source details expanded
5. Settings sidebar

## Deployment

### Option 1: Streamlit Cloud (Free)
1. Push to GitHub
2. Go to streamlit.io
3. Connect your repo
4. Deploy!

**URL**: `your-app.streamlit.app`

### Option 2: Local Network
```bash
# Run on specific port
streamlit run app.py --server.port 8080

# Allow external connections
streamlit run app.py --server.address 0.0.0.0
```

**Access from other devices**: `http://your-ip:8501`

### Option 3: Docker
```bash
# Build image
docker build -t arabic-rag-app .

# Run container
docker run -p 8501:8501 arabic-rag-app
```

## Tips

### For Demos
1. Start with example queries
2. Show category detection
3. Compare with/without reranking
4. Show source attribution
5. Explain the technology

### For Development
1. Use "Rerun" button after code changes
2. Check terminal for errors
3. Use sidebar settings to test configurations
4. Monitor performance in terminal

### For Production
1. Enable caching (already done)
2. Add error handling
3. Add usage analytics
4. Set up monitoring
5. Add rate limiting

## Next Steps

### Immediate
- ✅ Test all features
- ✅ Try different queries
- ✅ Take screenshots
- ✅ Share with others

### Short-term
- Add more example queries
- Improve UI/UX
- Add query history
- Add feedback mechanism

### Long-term
- Deploy to production
- Add user authentication
- Add analytics dashboard
- Scale to more documents

---

**Enjoy your demo!** 🎉

**Questions?** Check `DAY5_6_GUIDE.md` for detailed documentation.
