"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Plus,
  Search,
  Trash2,
  Moon,
  Sun,
  FileText,
  Edit3,
  Calendar,
  Clock,
  FileDown,
  FileType,
  FileIcon as FilePdf,
  Filter,
} from "lucide-react"
import { useTheme } from "next-themes"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { exportAsText, exportAsMarkdown, exportAsPDF } from "@/lib/export-utils"
import { RichTextEditor } from "@/components/rich-text-editor"
import { CategoryManager } from "@/components/category-manager"
import { KeyboardShortcuts } from "@/components/keyboard-shortcuts"

interface Category {
  id: string
  name: string
  color: string
}

interface Note {
  id: string
  title: string
  content: string
  categories: string[]
  createdAt: Date
  updatedAt: Date
}

export default function NotepadApp() {
  const [notes, setNotes] = useState<Note[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedNote, setSelectedNote] = useState<Note | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState<string[]>([])
  const [isEditing, setIsEditing] = useState(false)
  const { theme, setTheme } = useTheme()
  const searchInputRef = useRef<HTMLInputElement>(null)

  // Load data from localStorage on mount
  useEffect(() => {
    const savedNotes = localStorage.getItem("notepad-notes")
    const savedCategories = localStorage.getItem("notepad-categories")

    if (savedCategories) {
      setCategories(JSON.parse(savedCategories))
    }

    if (savedNotes) {
      const parsedNotes = JSON.parse(savedNotes).map((note: any) => ({
        ...note,
        categories: note.categories || [],
        createdAt: new Date(note.createdAt),
        updatedAt: new Date(note.updatedAt),
      }))
      setNotes(parsedNotes)
      if (parsedNotes.length > 0) {
        setSelectedNote(parsedNotes[0])
      }
    }
  }, [])

  // Save data to localStorage
  useEffect(() => {
    if (notes.length > 0) {
      localStorage.setItem("notepad-notes", JSON.stringify(notes))
    }
  }, [notes])

  useEffect(() => {
    localStorage.setItem("notepad-categories", JSON.stringify(categories))
  }, [categories])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case "n":
            e.preventDefault()
            createNewNote()
            break
          case "s":
            e.preventDefault()
            // Auto-save is already handled
            break
          case "f":
            e.preventDefault()
            searchInputRef.current?.focus()
            break
          case "d":
            e.preventDefault()
            if (selectedNote) {
              deleteNote(selectedNote.id)
            }
            break
          case "e":
            e.preventDefault()
            if (selectedNote) {
              exportAsText(selectedNote)
            }
            break
          case "/":
            e.preventDefault()
            // Keyboard shortcuts dialog will be triggered by the component
            break
        }
      }

      if (e.key === "Escape") {
        setIsEditing(false)
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [selectedNote])

  const createNewNote = useCallback(() => {
    const newNote: Note = {
      id: Date.now().toString(),
      title: "Untitled Note",
      content: "",
      categories: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    setNotes((prev) => [newNote, ...prev])
    setSelectedNote(newNote)
    setIsEditing(true)
  }, [])

  const updateNote = useCallback(
    (updates: Partial<Note>) => {
      if (!selectedNote) return

      const updatedNote = {
        ...selectedNote,
        ...updates,
        updatedAt: new Date(),
      }

      setNotes((prev) => prev.map((note) => (note.id === selectedNote.id ? updatedNote : note)))
      setSelectedNote(updatedNote)
    },
    [selectedNote],
  )

  const deleteNote = useCallback(
    (noteId: string) => {
      setNotes((prev) => prev.filter((note) => note.id !== noteId))
      if (selectedNote?.id === noteId) {
        const remainingNotes = notes.filter((note) => note.id !== noteId)
        setSelectedNote(remainingNotes.length > 0 ? remainingNotes[0] : null)
      }
    },
    [selectedNote, notes],
  )

  const filteredNotes = notes.filter((note) => {
    const matchesSearch =
      note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.content.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesCategory =
      selectedCategoryFilter.length === 0 || selectedCategoryFilter.some((catId) => note.categories.includes(catId))

    return matchesSearch && matchesCategory
  })

  const formatDate = (date: Date) => {
    const now = new Date()
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)

    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    } else if (diffInHours < 168) {
      return date.toLocaleDateString([], { weekday: "short" })
    } else {
      return date.toLocaleDateString([], { month: "short", day: "numeric" })
    }
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Sidebar */}
      <div className="w-80 border-r border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 backdrop-blur-xl">
        {/* Header */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 dark:from-slate-100 dark:to-slate-400 bg-clip-text text-transparent">
                Notes
              </h1>
            </div>
            <div className="flex items-center gap-1">
              <KeyboardShortcuts />
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                className="rounded-xl"
              >
                {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </Button>
            </div>
          </div>

          {/* Search */}
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input
              ref={searchInputRef}
              placeholder="Search notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 rounded-xl border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50"
            />
          </div>

          {/* Category Filter */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Filter by Category</span>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                    <Filter className="w-3 h-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => setSelectedCategoryFilter([])}>All Notes</DropdownMenuItem>
                  {categories.map((category) => (
                    <DropdownMenuItem key={category.id} onClick={() => setSelectedCategoryFilter([category.id])}>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: category.color }} />
                        {category.name}
                      </div>
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {selectedCategoryFilter.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {selectedCategoryFilter.map((catId) => {
                  const category = categories.find((cat) => cat.id === catId)
                  if (!category) return null
                  return (
                    <Badge
                      key={catId}
                      variant="secondary"
                      className="text-xs cursor-pointer"
                      style={{ backgroundColor: category.color + "20", color: category.color }}
                      onClick={() => setSelectedCategoryFilter([])}
                    >
                      {category.name} ×
                    </Badge>
                  )
                })}
              </div>
            )}
          </div>
        </div>

        {/* New Note Button */}
        <div className="p-4">
          <Button
            onClick={createNewNote}
            className="w-full rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Note
          </Button>
        </div>

        {/* Notes List */}
        <div className="flex-1 overflow-y-auto px-4 pb-4">
          {filteredNotes.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
              <p className="text-slate-500 dark:text-slate-400">
                {searchQuery || selectedCategoryFilter.length > 0 ? "No notes found" : "No notes yet"}
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredNotes.map((note) => (
                <Card
                  key={note.id}
                  className={`p-4 cursor-pointer transition-all duration-200 hover:shadow-md border-0 group ${
                    selectedNote?.id === note.id
                      ? "bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950/30 dark:to-purple-950/30 shadow-md"
                      : "bg-white/70 dark:bg-slate-800/50 hover:bg-white dark:hover:bg-slate-800/70"
                  }`}
                  onClick={() => {
                    setSelectedNote(note)
                    setIsEditing(false)
                  }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-slate-900 dark:text-slate-100 truncate flex-1">{note.title}</h3>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={(e) => {
                        e.stopPropagation()
                        deleteNote(note.id)
                      }}
                      className="w-6 h-6 text-slate-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>

                  {/* Categories */}
                  {note.categories.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-2">
                      {note.categories.slice(0, 3).map((catId) => {
                        const category = categories.find((cat) => cat.id === catId)
                        if (!category) return null
                        return (
                          <Badge
                            key={catId}
                            variant="secondary"
                            className="text-xs"
                            style={{ backgroundColor: category.color + "20", color: category.color }}
                          >
                            {category.name}
                          </Badge>
                        )
                      })}
                      {note.categories.length > 3 && (
                        <Badge variant="secondary" className="text-xs">
                          +{note.categories.length - 3}
                        </Badge>
                      )}
                    </div>
                  )}

                  <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 mb-2">
                    {note.content.replace(/<[^>]*>/g, "") || "No content"}
                  </p>
                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <Clock className="w-3 h-3" />
                    {formatDate(note.updatedAt)}
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {selectedNote ? (
          <>
            {/* Note Header */}
            <div className="p-6 border-b border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 backdrop-blur-xl">
              <div className="flex items-center justify-between mb-4">
                <Input
                  value={selectedNote.title}
                  onChange={(e) => updateNote({ title: e.target.value })}
                  className="text-2xl font-bold border-0 bg-transparent p-0 focus-visible:ring-0 text-slate-900 dark:text-slate-100"
                  placeholder="Note title..."
                />
                <div className="flex items-center gap-2">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="rounded-xl">
                        <FileDown className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => exportAsText(selectedNote)}>
                        <FileText className="w-4 h-4 mr-2" />
                        Export as TXT
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => exportAsMarkdown(selectedNote)}>
                        <FileType className="w-4 h-4 mr-2" />
                        Export as MD
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => exportAsPDF(selectedNote)}>
                        <FilePdf className="w-4 h-4 mr-2" />
                        Export as PDF
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                  <Button variant="ghost" size="icon" onClick={() => setIsEditing(!isEditing)} className="rounded-xl">
                    <Edit3 className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* Categories */}
              <div className="mb-4">
                <CategoryManager
                  categories={categories}
                  onCategoriesChange={setCategories}
                  selectedCategories={selectedNote.categories}
                  onSelectedCategoriesChange={(cats) => updateNote({ categories: cats })}
                />
              </div>

              <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  Created {formatDate(selectedNote.createdAt)}
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  Updated {formatDate(selectedNote.updatedAt)}
                </div>
              </div>
            </div>

            {/* Note Content */}
            <div className="flex-1 p-6">
              <RichTextEditor
                content={selectedNote.content}
                onChange={(content) => updateNote({ content })}
                placeholder="Start writing your note..."
              />
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="p-6 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-600 w-24 h-24 mx-auto mb-6 flex items-center justify-center">
                <FileText className="w-12 h-12 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2">Welcome to Notes</h2>
              <p className="text-slate-600 dark:text-slate-400 mb-6">Create your first note to get started</p>
              <Button
                onClick={createNewNote}
                className="rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Note
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
