"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { SpellChecker } from "@/lib/spell-checker"
import { Check, Plus, X, RefreshCw } from "lucide-react"

interface SpellingSuggestionsProps {
  word: string
  position: { x: number; y: number }
  onSuggestionSelect: (suggestion: string) => void
  onClose: () => void
  onAddToDictionary: (word: string) => void
}

export function SpellingSuggestions({
  word,
  position,
  onSuggestionSelect,
  onClose,
  onAddToDictionary,
}: SpellingSuggestionsProps) {
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const cardRef = useRef<HTMLDivElement>(null)
  const spellChecker = useRef(new SpellChecker())

  useEffect(() => {
    const loadSuggestions = async () => {
      setIsLoading(true)
      try {
        const suggestionList = await spellChecker.current.getSuggestions(word)
        setSuggestions(suggestionList)
      } catch (error) {
        console.error("Failed to load suggestions:", error)
        setSuggestions([])
      } finally {
        setIsLoading(false)
      }
    }

    loadSuggestions()
  }, [word])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (cardRef.current && !cardRef.current.contains(event.target as Node)) {
        onClose()
      }
    }

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose()
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    document.addEventListener("keydown", handleEscape)

    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
      document.removeEventListener("keydown", handleEscape)
    }
  }, [onClose])

  // Adjust position to keep popup within viewport
  const adjustedPosition = {
    x: Math.min(position.x, window.innerWidth - 280),
    y: Math.min(position.y, window.innerHeight - 300),
  }

  return (
    <Card
      ref={cardRef}
      className="fixed z-50 w-64 p-3 shadow-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800"
      style={{
        left: adjustedPosition.x,
        top: adjustedPosition.y,
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-red-500"></div>
          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">"{word}"</span>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="h-6 w-6 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
        >
          <X className="w-3 h-3" />
        </Button>
      </div>

      {/* Loading state */}
      {isLoading && (
        <div className="flex items-center justify-center py-4">
          <RefreshCw className="w-4 h-4 animate-spin text-slate-400" />
          <span className="ml-2 text-sm text-slate-500">Loading suggestions...</span>
        </div>
      )}

      {/* Suggestions */}
      {!isLoading && suggestions.length > 0 && (
        <div className="space-y-1 mb-3">
          <div className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-2">Suggestions:</div>
          {suggestions.map((suggestion, index) => (
            <Button
              key={index}
              variant="ghost"
              size="sm"
              onClick={() => onSuggestionSelect(suggestion)}
              className="w-full justify-start text-left h-8 px-2 text-sm hover:bg-blue-50 dark:hover:bg-blue-900/20"
            >
              <Check className="w-3 h-3 mr-2 text-green-500" />
              {suggestion}
            </Button>
          ))}
        </div>
      )}

      {/* No suggestions */}
      {!isLoading && suggestions.length === 0 && (
        <div className="text-center py-3 mb-3">
          <div className="text-sm text-slate-500 dark:text-slate-400">No suggestions found</div>
        </div>
      )}

      {/* Actions */}
      <Separator className="mb-3" />

      <div className="space-y-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onAddToDictionary(word)}
          className="w-full justify-start text-left h-8 px-2 text-sm hover:bg-green-50 dark:hover:bg-green-900/20"
        >
          <Plus className="w-3 h-3 mr-2 text-green-500" />
          Add to dictionary
        </Button>

        <Button
          variant="ghost"
          size="sm"
          onClick={onClose}
          className="w-full justify-start text-left h-8 px-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-700"
        >
          <X className="w-3 h-3 mr-2 text-slate-400" />
          Ignore
        </Button>
      </div>

      {/* Keyboard shortcuts hint */}
      <div className="mt-3 pt-2 border-t border-slate-100 dark:border-slate-700">
        <div className="text-xs text-slate-400 dark:text-slate-500">
          Press <kbd className="px-1 py-0.5 text-xs bg-slate-100 dark:bg-slate-700 rounded">Esc</kbd> to close
        </div>
      </div>
    </Card>
  )
}
