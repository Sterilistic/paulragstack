'use client'

import React, { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Search, Loader2 } from 'lucide-react'

interface SearchResult {
  id: number
  title: string
  url: string
  content: string
  similarity: number
}

interface SearchResponse {
  essays: SearchResult[]
  insights: string
}

export default function Home() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, limit: 5 }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Search failed:', error)
    }
    setLoading(false)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Paul Graham Essay Search
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            Search through Paul Graham's essays using AI-powered semantic search
          </p>
          
          <div className="flex gap-2 mb-12">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <Input
                placeholder="Search essays..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pl-10 h-12 text-lg"
              />
            </div>
            <Button 
              onClick={handleSearch} 
              disabled={loading || !query.trim()}
              className="h-12 px-6 text-lg"
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                'Search'
              )}
            </Button>
          </div>
        </div>

        {results && (
          <div className="max-w-3xl mx-auto">
            {/* Key Insights Section */}
            <div className="mb-12 bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Key Insights
              </h2>
              <div className="prose prose-gray max-w-none">
                {results.insights.split('•').map((insight, index) => (
                  insight.trim() && (
                    <div key={index} className="flex gap-2 mb-3">
                      <ul className="list-disc pl-5 text-gray-700">
                        <li>{insight.trim()}</li>
                      </ul>
                    </div>
                  )
                ))}
              </div>
            </div>

            <h2 className="text-xl font-semibold text-gray-700 mb-6">
              Relevant Essays
            </h2>
            <div className="space-y-6">
              {results.essays.map((result) => (
                <Card key={result.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <CardHeader className="bg-gray-50 border-b">
                    <CardTitle className="flex items-center justify-between">
                      <a
                        href={result.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 hover:underline text-xl"
                      >
                        {result.title}
                      </a>
                      <span className="text-sm text-gray-500">
                        {(result.similarity * 100).toFixed(1)}% match
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-6">
                    <div className="prose prose-gray max-w-none">
                      <p className="text-gray-600 line-clamp-3 mb-4 text-base leading-relaxed">
                        {result.content.substring(0, 300)}...
                      </p>
                      <a
                        href={result.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1 mt-4 font-medium"
                      >
                        Read full essay
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                        </svg>
                      </a>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {query && !loading && (!results || results.essays.length === 0) && (
          <div className="text-center text-gray-600 mt-12">
            No results found for "{query}"
          </div>
        )}
      </main>
    </div>
  )
} 