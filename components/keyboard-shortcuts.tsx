"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Keyboard } from "lucide-react"

const shortcuts = [
  {
    category: "General",
    items: [
      { keys: ["Ctrl", "N"], description: "Create new note" },
      { keys: ["Ctrl", "S"], description: "Save as TXT (default)" },
      { keys: ["Ctrl", "Shift", "S"], description: "Save As... (show all formats)" },
      { keys: ["Ctrl", "F"], description: "Focus search" },
      { keys: ["Ctrl", "D"], description: "Delete current note" },
      { keys: ["Ctrl", "E"], description: "Export current note" },
      { keys: ["Ctrl", "/"], description: "Show keyboard shortcuts" },
    ],
  },
  {
    category: "Formatting",
    items: [
      { keys: ["Ctrl", "B"], description: "Bold text" },
      { keys: ["Ctrl", "I"], description: "Italic text" },
      { keys: ["Ctrl", "U"], description: "Underline text" },
      { keys: ["Ctrl", "Z"], description: "Undo" },
      { keys: ["Ctrl", "Shift", "Z"], description: "Redo" },
    ],
  },
  {
    category: "Navigation",
    items: [
      { keys: ["↑", "↓"], description: "Navigate between notes" },
      { keys: ["Escape"], description: "Close dialogs" },
      { keys: ["Tab"], description: "Navigate interface" },
    ],
  },
]

export function KeyboardShortcuts() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon" className="rounded-xl" title="Keyboard Shortcuts (Ctrl+/)">
          <Keyboard className="w-4 h-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Keyboard Shortcuts</DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {shortcuts.map((section) => (
            <div key={section.category} className="space-y-3">
              <h3 className="font-semibold text-slate-900 dark:text-slate-100">{section.category}</h3>
              <div className="space-y-2">
                {section.items.map((shortcut, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-slate-600 dark:text-slate-400">{shortcut.description}</span>
                    <div className="flex items-center gap-1">
                      {shortcut.keys.map((key, keyIndex) => (
                        <span key={keyIndex} className="flex items-center gap-1">
                          <kbd className="px-2 py-1 text-xs font-semibold text-slate-800 bg-slate-100 border border-slate-200 rounded dark:text-slate-200 dark:bg-slate-700 dark:border-slate-600">
                            {key}
                          </kbd>
                          {keyIndex < shortcut.keys.length - 1 && <span className="text-slate-400">+</span>}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  )
}
