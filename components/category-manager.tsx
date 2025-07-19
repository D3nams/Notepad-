"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Plus, X, Tag, Settings } from "lucide-react"

interface Category {
  id: string
  name: string
  color: string
}

interface CategoryManagerProps {
  categories: Category[]
  onCategoriesChange: (categories: Category[]) => void
  selectedCategories: string[]
  onSelectedCategoriesChange: (categories: string[]) => void
}

const PRESET_COLORS = [
  "#ef4444",
  "#f97316",
  "#f59e0b",
  "#eab308",
  "#84cc16",
  "#22c55e",
  "#10b981",
  "#14b8a6",
  "#06b6d4",
  "#0ea5e9",
  "#3b82f6",
  "#6366f1",
  "#8b5cf6",
  "#a855f7",
  "#d946ef",
  "#ec4899",
  "#f43f5e",
]

export function CategoryManager({
  categories,
  onCategoriesChange,
  selectedCategories,
  onSelectedCategoriesChange,
}: CategoryManagerProps) {
  const [newCategoryName, setNewCategoryName] = useState("")
  const [selectedColor, setSelectedColor] = useState(PRESET_COLORS[0])
  const [isOpen, setIsOpen] = useState(false)

  const addCategory = () => {
    if (newCategoryName.trim()) {
      const newCategory: Category = {
        id: Date.now().toString(),
        name: newCategoryName.trim(),
        color: selectedColor,
      }
      onCategoriesChange([...categories, newCategory])
      setNewCategoryName("")
      setSelectedColor(PRESET_COLORS[0])
    }
  }

  const removeCategory = (categoryId: string) => {
    onCategoriesChange(categories.filter((cat) => cat.id !== categoryId))
    onSelectedCategoriesChange(selectedCategories.filter((id) => id !== categoryId))
  }

  const toggleCategorySelection = (categoryId: string) => {
    if (selectedCategories.includes(categoryId)) {
      onSelectedCategoriesChange(selectedCategories.filter((id) => id !== categoryId))
    } else {
      onSelectedCategoriesChange([...selectedCategories, categoryId])
    }
  }

  return (
    <div className="space-y-3">
      {/* Selected Categories */}
      <div className="flex flex-wrap gap-2">
        {selectedCategories.map((categoryId) => {
          const category = categories.find((cat) => cat.id === categoryId)
          if (!category) return null
          return (
            <Badge
              key={categoryId}
              variant="secondary"
              className="cursor-pointer hover:opacity-80"
              style={{ backgroundColor: category.color + "20", color: category.color, borderColor: category.color }}
              onClick={() => toggleCategorySelection(categoryId)}
            >
              {category.name}
              <X className="w-3 h-3 ml-1" />
            </Badge>
          )
        })}
      </div>

      {/* Category Selection */}
      <div className="flex flex-wrap gap-2">
        {categories
          .filter((cat) => !selectedCategories.includes(cat.id))
          .map((category) => (
            <Badge
              key={category.id}
              variant="outline"
              className="cursor-pointer hover:opacity-80"
              style={{ borderColor: category.color, color: category.color }}
              onClick={() => toggleCategorySelection(category.id)}
            >
              <Tag className="w-3 h-3 mr-1" />
              {category.name}
            </Badge>
          ))}
      </div>

      {/* Manage Categories Dialog */}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            className="text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
          >
            <Settings className="w-4 h-4 mr-1" />
            Manage Categories
          </Button>
        </DialogTrigger>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Manage Categories</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            {/* Add New Category */}
            <div className="space-y-3">
              <Input
                placeholder="Category name"
                value={newCategoryName}
                onChange={(e) => setNewCategoryName(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addCategory()}
              />

              {/* Color Picker */}
              <div className="flex flex-wrap gap-2">
                {PRESET_COLORS.map((color) => (
                  <button
                    key={color}
                    className={`w-6 h-6 rounded-full border-2 ${selectedColor === color ? "border-slate-400" : "border-transparent"}`}
                    style={{ backgroundColor: color }}
                    onClick={() => setSelectedColor(color)}
                  />
                ))}
              </div>

              <Button onClick={addCategory} className="w-full">
                <Plus className="w-4 h-4 mr-2" />
                Add Category
              </Button>
            </div>

            {/* Existing Categories */}
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-slate-700 dark:text-slate-300">Existing Categories</h4>
              {categories.map((category) => (
                <div
                  key={category.id}
                  className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800"
                >
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full" style={{ backgroundColor: category.color }} />
                    <span className="text-sm">{category.name}</span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeCategory(category.id)}
                    className="text-red-500 hover:text-red-700 h-6 w-6 p-0"
                  >
                    <X className="w-3 h-3" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
