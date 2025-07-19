import { jsPDF } from "jspdf"

export interface Note {
  id: string
  title: string
  content: string
  categories?: string[]
  createdAt: Date
  updatedAt: Date
}

// Helper function to strip HTML tags
function stripHtml(html: string): string {
  const tmp = document.createElement("div")
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ""
}

// Export as plain text (.txt)
export function exportAsText(note: Note): void {
  const content = `${note.title}\n\n${stripHtml(note.content)}`
  downloadFile(content, `${note.title.replace(/\s+/g, "-").toLowerCase()}.txt`, "text/plain")
}

// Export as markdown (.md)
export function exportAsMarkdown(note: Note): void {
  // Convert HTML to basic markdown
  const content = note.content
    .replace(/<h1[^>]*>(.*?)<\/h1>/gi, "# $1\n\n")
    .replace(/<h2[^>]*>(.*?)<\/h2>/gi, "## $1\n\n")
    .replace(/<h3[^>]*>(.*?)<\/h3>/gi, "### $1\n\n")
    .replace(/<strong[^>]*>(.*?)<\/strong>/gi, "**$1**")
    .replace(/<b[^>]*>(.*?)<\/b>/gi, "**$1**")
    .replace(/<em[^>]*>(.*?)<\/em>/gi, "*$1*")
    .replace(/<i[^>]*>(.*?)<\/i>/gi, "*$1*")
    .replace(/<u[^>]*>(.*?)<\/u>/gi, "_$1_")
    .replace(/<blockquote[^>]*>(.*?)<\/blockquote>/gi, "> $1\n\n")
    .replace(/<pre[^>]*>(.*?)<\/pre>/gi, "```\n$1\n```\n\n")
    .replace(/<ul[^>]*>(.*?)<\/ul>/gi, "$1\n")
    .replace(/<ol[^>]*>(.*?)<\/ol>/gi, "$1\n")
    .replace(/<li[^>]*>(.*?)<\/li>/gi, "- $1\n")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<p[^>]*>/gi, "")
    .replace(/<[^>]*>/g, "") // Remove any remaining HTML tags
    .replace(/\n{3,}/g, "\n\n") // Clean up excessive newlines

  const markdownContent = `# ${note.title}\n\n${content}`
  downloadFile(markdownContent, `${note.title.replace(/\s+/g, "-").toLowerCase()}.md`, "text/markdown")
}

// Export as PDF (.pdf)
export function exportAsPDF(note: Note): void {
  const doc = new jsPDF()

  // Add title
  doc.setFontSize(18)
  doc.text(note.title, 20, 20)

  // Add content with word wrap (strip HTML)
  doc.setFontSize(12)
  const plainContent = stripHtml(note.content)
  const splitText = doc.splitTextToSize(plainContent, 170)
  doc.text(splitText, 20, 30)

  // Add metadata
  doc.setFontSize(8)
  doc.setTextColor(150)
  const dateStr = new Date(note.updatedAt).toLocaleString()
  doc.text(`Last updated: ${dateStr}`, 20, doc.internal.pageSize.height - 10)

  // Save PDF
  doc.save(`${note.title.replace(/\s+/g, "-").toLowerCase()}.pdf`)
}

// Helper function to download file
function downloadFile(content: string, fileName: string, contentType: string): void {
  const blob = new Blob([content], { type: contentType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
