import { useState } from 'react'
import axios from 'axios'
import { api } from './api'
import './App.css'

interface UploadResult {
  filename: string
  num_pages: number
  num_chunks: number
  num_chunks_stored: number
}

interface RetrievedChunk {
  content: string
  filename: string
  page: number
  score: number
}

interface ChatResponse {
  question: string
  answer: string
  retrieved_chunks: RetrievedChunk[]
}

function getErrorMessage(err: unknown, fallback: string): string {
  if (axios.isAxiosError(err)) {
    return err.response?.data?.detail ?? err.message
  }
  return fallback
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)
  const [uploadError, setUploadError] = useState('')

  const [question, setQuestion] = useState('')
  const [asking, setAsking] = useState(false)
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState<RetrievedChunk[]>([])
  const [askError, setAskError] = useState('')
  const [hasAsked, setHasAsked] = useState(false)

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setUploadError('')
    setUploadResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await api.post<UploadResult>('/api/documents/upload', formData)
      setUploadResult(res.data)
    } catch (err) {
      setUploadError(getErrorMessage(err, 'Upload failed'))
    } finally {
      setUploading(false)
    }
  }

  const handleAsk = async () => {
    if (!question.trim()) return

    setAsking(true)
    setHasAsked(true)
    setAskError('')
    setAnswer('')
    setSources([])

    try {
      const res = await api.post<ChatResponse>('/api/chat', { question })
      setAnswer(res.data.answer)
      setSources(res.data.retrieved_chunks)
    } catch (err) {
      setAskError(getErrorMessage(err, 'Failed to get an answer'))
    } finally {
      setAsking(false)
    }
  }

  return (
    <div className="container">
      <header className="page-header">
        <h1>RAG Document Q&amp;A</h1>
        <p className="subtitle">Upload a PDF, then ask questions about its contents.</p>
      </header>

      <section className="card">
        <div className="step-heading">
          <span className="step-badge">1</span>
          <h2>Upload a PDF</h2>
        </div>

        <div className="field">
          <label className="field-label" htmlFor="pdf-input">
            Document
          </label>
          <div className="row">
            <input
              id="pdf-input"
              type="file"
              accept="application/pdf"
              onChange={(e) => {
                setFile(e.target.files?.[0] ?? null)
                setUploadResult(null)
                setUploadError('')
              }}
            />
            <button onClick={handleUpload} disabled={!file || uploading}>
              {uploading ? 'Uploading…' : 'Upload'}
            </button>
          </div>
        </div>

        {uploadResult && (
          <p className="message success">
            Uploaded <strong>{uploadResult.filename}</strong> — {uploadResult.num_pages} page
            {uploadResult.num_pages === 1 ? '' : 's'}, {uploadResult.num_chunks_stored} chunks
            stored.
          </p>
        )}
        {uploadError && <p className="message error">{uploadError}</p>}
      </section>

      <section className="card">
        <div className="step-heading">
          <span className="step-badge">2</span>
          <h2>Ask a question</h2>
        </div>

        <div className="field">
          <label className="field-label" htmlFor="question-input">
            Question
          </label>
          <div className="row">
            <input
              id="question-input"
              type="text"
              placeholder="e.g. What is this document about?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            />
            <button onClick={handleAsk} disabled={!question.trim() || asking}>
              {asking ? 'Asking…' : 'Ask'}
            </button>
          </div>
        </div>

        {askError && <p className="message error">{askError}</p>}

        {asking && <p className="hint">Retrieving relevant chunks and generating an answer…</p>}

        {!hasAsked && !askError && (
          <p className="hint">Upload a document above, then ask a question to see the answer and its sources here.</p>
        )}

        {answer && (
          <div className="answer-block">
            <h3>Answer</h3>
            <p>{answer}</p>
          </div>
        )}

        {sources.length > 0 && (
          <div className="sources-block">
            <h3>Sources</h3>
            <ul>
              {sources.map((chunk, i) => (
                <li key={i}>
                  <div className="source-meta">
                    <strong>{chunk.filename}</strong>
                    <span className="source-meta-sep">·</span>
                    <span>page {chunk.page}</span>
                    <span className="source-meta-sep">·</span>
                    <span>score {chunk.score.toFixed(3)}</span>
                  </div>
                  <p className="source-content">{chunk.content}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </div>
  )
}

export default App
