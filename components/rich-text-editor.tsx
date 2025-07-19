"use client"

import type React from "react"

import { useRef, useEffect, useCallback, useState } from "react"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Bold, Italic, Underline, List, ListOrdered, Quote, Heading1, Heading2, Code, Undo, Redo } from "lucide-react"
import { SpellChecker } from "@/lib/spell-checker"
import { SpellingSuggestions } from "@/components/spelling-suggestions"

interface RichTextEditorProps {
  content: string
  onChange: (content: string) => void
  placeholder?: string
}

export function RichTextEditor({ content, onChange, placeholder = "Start writing..." }: RichTextEditorProps) {
  const editorRef = useRef<HTMLDivElement>(null)

  const [spellChecker] = useState(() => new SpellChecker())
  const [misspelledWords, setMisspelledWords] = useState<Set<string>>(new Set())
  const [suggestionPosition, setSuggestionPosition] = useState<{ x: number; y: number } | null>(null)
  const [selectedWord, setSelectedWord] = useState<{ word: string; range: Range } | null>(null)
  const [isSpellCheckEnabled, setIsSpellCheckEnabled] = useState(true)

  const executeCommand = useCallback(
    (command: string, value?: string) => {
      document.execCommand(command, false, value)
      if (editorRef.current) {
        onChange(editorRef.current.innerHTML)
      }
    },
    [onChange],
  )

  const checkSpelling = useCallback(async () => {
    if (!editorRef.current || !isSpellCheckEnabled) return

    const text = editorRef.current.innerText
    const words = text.match(/\b[a-zA-Z]+\b/g) || []
    const misspelled = new Set<string>()

    for (const word of words) {
      const isCorrect = await spellChecker.checkWord(word)
      if (!isCorrect) {
        misspelled.add(word.toLowerCase())
      }
    }

    setMisspelledWords(misspelled)
    highlightMisspelledWords()
  }, [spellChecker, isSpellCheckEnabled])

  const highlightMisspelledWords = useCallback(() => {
    if (!editorRef.current) return

    const walker = document.createTreeWalker(editorRef.current, NodeFilter.SHOW_TEXT, null)

    const textNodes: Text[] = []
    let node
    while ((node = walker.nextNode())) {
      textNodes.push(node as Text)
    }

    textNodes.forEach((textNode) => {
      const text = textNode.textContent || ""
      const words = text.match(/\b[a-zA-Z]+\b/g)

      if (words) {
        let html = text
        words.forEach((word) => {
          if (misspelledWords.has(word.toLowerCase())) {
            const regex = new RegExp(`\\b${word}\\b`, "g")
            html = html.replace(regex, `<span class="misspelled-word" data-word="${word}">${word}</span>`)
          }
        })

        if (html !== text) {
          const wrapper = document.createElement("div")
          wrapper.innerHTML = html
          const parent = textNode.parentNode
          if (parent) {
            while (wrapper.firstChild) {
              parent.insertBefore(wrapper.firstChild, textNode)
            }
            parent.removeChild(textNode)
          }
        }
      }
    })
  }, [misspelledWords])

  const handleInput = useCallback(() => {
    if (editorRef.current) {
      onChange(editorRef.current.innerHTML)
    }
  }, [onChange])

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      // Handle keyboard shortcuts for formatting
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case "b":
            e.preventDefault()
            executeCommand("bold")
            break
          case "i":
            e.preventDefault()
            executeCommand("italic")
            break
          case "u":
            e.preventDefault()
            executeCommand("underline")
            break
          case "z":
            e.preventDefault()
            if (e.shiftKey) {
              executeCommand("redo")
            } else {
              executeCommand("undo")
            }
            break
        }
      }
    },
    [executeCommand],
  )

  const handleEditorClick = useCallback(async (e: React.MouseEvent) => {
    const target = e.target as HTMLElement
    if (target.classList.contains("misspelled-word")) {
      const word = target.getAttribute("data-word")
      if (word) {
        const rect = target.getBoundingClientRect()
        setSuggestionPosition({ x: rect.left, y: rect.bottom + 5 })

        const range = document.createRange()
        range.selectNodeContents(target)
        setSelectedWord({ word, range })
      }
    } else {
      setSuggestionPosition(null)
      setSelectedWord(null)
    }
  }, [])

  useEffect(() => {
    if (editorRef.current && editorRef.current.innerHTML !== content) {
      editorRef.current.innerHTML = content
    }
  }, [content])

  useEffect(() => {
    if (content && isSpellCheckEnabled) {
      setTimeout(checkSpelling, 500)
    }
  }, [content, checkSpelling, isSpellCheckEnabled])

  return (
    <div className="border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden bg-white dark:bg-slate-900">
      {/* Toolbar */}
      <div className="flex items-center gap-1 p-3 border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("undo")}
          className="h-8 w-8 p-0"
          title="Undo (Ctrl+Z)"
        >
          <Undo className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("redo")}
          className="h-8 w-8 p-0"
          title="Redo (Ctrl+Shift+Z)"
        >
          <Redo className="w-4 h-4" />
        </Button>

        <Separator orientation="vertical" className="h-6 mx-1" />

        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("formatBlock", "h1")}
          className="h-8 w-8 p-0"
          title="Heading 1"
        >
          <Heading1 className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("formatBlock", "h2")}
          className="h-8 w-8 p-0"
          title="Heading 2"
        >
          <Heading2 className="w-4 h-4" />
        </Button>

        <Separator orientation="vertical" className="h-6 mx-1" />

        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("bold")}
          className="h-8 w-8 p-0"
          title="Bold (Ctrl+B)"
        >
          <Bold className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("italic")}
          className="h-8 w-8 p-0"
          title="Italic (Ctrl+I)"
        >
          <Italic className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("underline")}
          className="h-8 w-8 p-0"
          title="Underline (Ctrl+U)"
        >
          <Underline className="w-4 h-4" />
        </Button>

        <Separator orientation="vertical" className="h-6 mx-1" />

        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("insertUnorderedList")}
          className="h-8 w-8 p-0"
          title="Bullet List"
        >
          <List className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("insertOrderedList")}
          className="h-8 w-8 p-0"
          title="Numbered List"
        >
          <ListOrdered className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("formatBlock", "blockquote")}
          className="h-8 w-8 p-0"
          title="Quote"
        >
          <Quote className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => executeCommand("formatBlock", "pre")}
          className="h-8 w-8 p-0"
          title="Code Block"
        >
          <Code className="w-4 h-4" />
        </Button>

        <Separator orientation="vertical" className="h-6 mx-1" />

        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsSpellCheckEnabled(!isSpellCheckEnabled)}
          className={`h-8 w-8 p-0 spell-check-status ${isSpellCheckEnabled ? "spell-check-active" : "disabled"}`}
          title={`Spell Check ${isSpellCheckEnabled ? "On" : "Off"}`}
          data-spell-check-toggle
        >
          <span className="text-xs font-bold">ABC</span>
        </Button>
      </div>

      {/* Editor */}
      <div
        ref={editorRef}
        contentEditable
        onInput={(e) => {
          handleInput()
          setTimeout(checkSpelling, 100) // Debounce spell check
        }}
        onKeyDown={handleKeyDown}
        onClick={handleEditorClick}
        className="min-h-[400px] p-4 focus:outline-none text-slate-700 dark:text-slate-300 text-lg leading-relaxed"
        style={{ wordBreak: "break-word" }}
        suppressContentEditableWarning={true}
        data-placeholder={placeholder}
      />
      {suggestionPosition && selectedWord && (
        <SpellingSuggestions
          word={selectedWord.word}
          position={suggestionPosition}
          onSuggestionSelect={(suggestion) => {
            if (selectedWord.range) {
              selectedWord.range.deleteContents()
              selectedWord.range.insertNode(document.createTextNode(suggestion))
              onChange(editorRef.current?.innerHTML || "")
              setSuggestionPosition(null)
              setSelectedWord(null)
              setTimeout(checkSpelling, 100)
            }
          }}
          onClose={() => {
            setSuggestionPosition(null)
            setSelectedWord(null)
          }}
          onAddToDictionary={(word) => {
            spellChecker.addToDictionary(word)
            setMisspelledWords((prev) => {
              const newSet = new Set(prev)
              newSet.delete(word.toLowerCase())
              return newSet
            })
            setSuggestionPosition(null)
            setSelectedWord(null)
            setTimeout(checkSpelling, 100)
          }}
        />
      )}
    </div>
  )
}
