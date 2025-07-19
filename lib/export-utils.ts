import { jsPDF } from "jspdf"

export interface Note {
  id: string
  title: string
  content: string
  categories: string[]
  createdAt: Date
  updatedAt: Date
}

// Helper function to strip HTML tags
function stripHtml(html: string): string {
  const tmp = document.createElement("div")
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ""
}

// Helper function to convert HTML to plain text with basic formatting
function htmlToPlainText(html: string): string {
  return html
    .replace(/<h[1-6][^>]*>(.*?)<\/h[1-6]>/gi, "\n$1\n" + "=".repeat(50) + "\n")
    .replace(/<strong[^>]*>(.*?)<\/strong>/gi, "**$1**")
    .replace(/<b[^>]*>(.*?)<\/b>/gi, "**$1**")
    .replace(/<em[^>]*>(.*?)<\/em>/gi, "*$1*")
    .replace(/<i[^>]*>(.*?)<\/i>/gi, "*$1*")
    .replace(/<u[^>]*>(.*?)<\/u>/gi, "_$1_")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<p[^>]*>/gi, "")
    .replace(/<[^>]*>/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

// Export as plain text (.txt) - DEFAULT
export function exportAsText(note: Note): void {
  const content = `${note.title}\n${"=".repeat(note.title.length)}\n\n${htmlToPlainText(note.content)}\n\n---\nCreated: ${note.createdAt.toLocaleString()}\nLast Updated: ${note.updatedAt.toLocaleString()}`
  downloadFile(content, `${sanitizeFileName(note.title)}.txt`, "text/plain")
}

// Export as markdown (.md)
export function exportAsMarkdown(note: Note): void {
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
    .replace(/<[^>]*>/g, "")
    .replace(/\n{3,}/g, "\n\n")

  const markdownContent = `# ${note.title}\n\n${content}\n\n---\n*Created: ${note.createdAt.toLocaleString()}*  \n*Last Updated: ${note.updatedAt.toLocaleString()}*`
  downloadFile(markdownContent, `${sanitizeFileName(note.title)}.md`, "text/markdown")
}

// Export as PDF (.pdf)
export function exportAsPDF(note: Note): void {
  const doc = new jsPDF()

  // Add title
  doc.setFontSize(18)
  doc.setFont("helvetica", "bold")
  doc.text(note.title, 20, 20)

  // Add a line under title
  doc.setLineWidth(0.5)
  doc.line(20, 25, 190, 25)

  // Add content
  doc.setFontSize(12)
  doc.setFont("helvetica", "normal")
  const plainContent = stripHtml(note.content)
  const splitText = doc.splitTextToSize(plainContent, 170)
  doc.text(splitText, 20, 35)

  // Add metadata at bottom
  doc.setFontSize(8)
  doc.setTextColor(100)
  const pageHeight = doc.internal.pageSize.height
  doc.text(`Created: ${note.createdAt.toLocaleString()}`, 20, pageHeight - 20)
  doc.text(`Last Updated: ${note.updatedAt.toLocaleString()}`, 20, pageHeight - 10)

  doc.save(`${sanitizeFileName(note.title)}.pdf`)
}

// Export as HTML (.html)
export function exportAsHTML(note: Note): void {
  const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${note.title}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        h1 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .metadata { color: #666; font-size: 0.9em; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }
        blockquote { border-left: 4px solid #ddd; margin: 0; padding-left: 20px; color: #666; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
        code { background: #f0f0f0; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>${note.title}</h1>
    <div class="content">${note.content}</div>
    <div class="metadata">
        <p><strong>Created:</strong> ${note.createdAt.toLocaleString()}</p>
        <p><strong>Last Updated:</strong> ${note.updatedAt.toLocaleString()}</p>
    </div>
</body>
</html>`
  downloadFile(htmlContent, `${sanitizeFileName(note.title)}.html`, "text/html")
}

// Export as JSON (.json)
export function exportAsJSON(note: Note): void {
  const jsonData = {
    id: note.id,
    title: note.title,
    content: note.content,
    plainTextContent: stripHtml(note.content),
    categories: note.categories,
    createdAt: note.createdAt.toISOString(),
    updatedAt: note.updatedAt.toISOString(),
    exportedAt: new Date().toISOString(),
    metadata: {
      wordCount: stripHtml(note.content)
        .split(/\s+/)
        .filter((word) => word.length > 0).length,
      characterCount: stripHtml(note.content).length,
      version: "1.0",
    },
  }
  downloadFile(JSON.stringify(jsonData, null, 2), `${sanitizeFileName(note.title)}.json`, "application/json")
}

// Export as XML (.xml)
export function exportAsXML(note: Note): void {
  const xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<note>
    <id>${note.id}</id>
    <title><![CDATA[${note.title}]]></title>
    <content><![CDATA[${note.content}]]></content>
    <plainTextContent><![CDATA[${stripHtml(note.content)}]]></plainTextContent>
    <categories>
        ${note.categories.map((cat) => `<category>${cat}</category>`).join("\n        ")}
    </categories>
    <createdAt>${note.createdAt.toISOString()}</createdAt>
    <updatedAt>${note.updatedAt.toISOString()}</updatedAt>
    <exportedAt>${new Date().toISOString()}</exportedAt>
</note>`
  downloadFile(xmlContent, `${sanitizeFileName(note.title)}.xml`, "application/xml")
}

// Export as RTF (.rtf)
export function exportAsRTF(note: Note): void {
  const plainText = stripHtml(note.content)
  const rtfContent = `{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}}
\\f0\\fs24 {\\b ${note.title}}\\par
\\par
${plainText.replace(/\n/g, "\\par\n")}\\par
\\par
---\\par
Created: ${note.createdAt.toLocaleString()}\\par
Last Updated: ${note.updatedAt.toLocaleString()}\\par
}`
  downloadFile(rtfContent, `${sanitizeFileName(note.title)}.rtf`, "application/rtf")
}

// Export as CSV (.csv)
export function exportAsCSV(note: Note): void {
  const csvContent = `"Field","Value"
"ID","${note.id}"
"Title","${note.title.replace(/"/g, '""')}"
"Content","${stripHtml(note.content).replace(/"/g, '""')}"
"Categories","${note.categories.join("; ")}"
"Created","${note.createdAt.toISOString()}"
"Updated","${note.updatedAt.toISOString()}"
"Word Count","${
    stripHtml(note.content)
      .split(/\s+/)
      .filter((word) => word.length > 0).length
  }"
"Character Count","${stripHtml(note.content).length}"`
  downloadFile(csvContent, `${sanitizeFileName(note.title)}.csv`, "text/csv")
}

// Export as Assembly (.asm)
export function exportAsASM(note: Note): void {
  const plainText = stripHtml(note.content)
  const asmContent = `; ${note.title}
; Generated on ${new Date().toLocaleString()}
; Original created: ${note.createdAt.toLocaleString()}

section .data
    title db '${note.title}', 0
    content db '${plainText.replace(/'/g, "\\'")}', 0
    newline db 10, 0

section .text
    global _start

_start:
    ; Print title
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, title      ; message
    mov edx, ${note.title.length}  ; length
    int 0x80            ; system call

    ; Print newline
    mov eax, 4
    mov ebx, 1
    mov ecx, newline
    mov edx, 1
    int 0x80

    ; Print content
    mov eax, 4
    mov ebx, 1
    mov ecx, content
    mov edx, ${stripHtml(note.content).length}
    int 0x80

    ; Exit program
    mov eax, 1          ; sys_exit
    xor ebx, ebx        ; exit status
    int 0x80`
  downloadFile(asmContent, `${sanitizeFileName(note.title)}.asm`, "text/plain")
}

// Export as NASM (.nasm)
export function exportAsNASM(note: Note): void {
  const plainText = stripHtml(note.content)
  const nasmContent = `; ${note.title}
; NASM Assembly - Generated on ${new Date().toLocaleString()}

%define SYS_WRITE 4
%define SYS_EXIT  1
%define STDOUT    1

section .data
    title: db '${note.title}', 10, 0
    title_len equ $ - title
    
    content: db '${plainText.replace(/'/g, "\\'")}', 10, 0
    content_len equ $ - content
    
    footer: db '---', 10, 'Created: ${note.createdAt.toLocaleString()}', 10, 0
    footer_len equ $ - footer

section .text
    global _start

_start:
    ; Write title
    mov eax, SYS_WRITE
    mov ebx, STDOUT
    mov ecx, title
    mov edx, title_len
    int 0x80
    
    ; Write content
    mov eax, SYS_WRITE
    mov ebx, STDOUT
    mov ecx, content
    mov edx, content_len
    int 0x80
    
    ; Write footer
    mov eax, SYS_WRITE
    mov ebx, STDOUT
    mov ecx, footer
    mov edx, footer_len
    int 0x80
    
    ; Exit
    mov eax, SYS_EXIT
    xor ebx, ebx
    int 0x80`
  downloadFile(nasmContent, `${sanitizeFileName(note.title)}.nasm`, "text/plain")
}

// Export as C (.c)
export function exportAsC(note: Note): void {
  const plainText = stripHtml(note.content).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\n/g, "\\n")
  const cContent = `/*
 * ${note.title}
 * Generated on ${new Date().toLocaleString()}
 * Original created: ${note.createdAt.toLocaleString()}
 */

#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("${note.title}\\n");
    printf("${"=".repeat(note.title.length)}\\n\\n");
    
    printf("${plainText}\\n\\n");
    
    printf("---\\n");
    printf("Created: ${note.createdAt.toLocaleString()}\\n");
    printf("Last Updated: ${note.updatedAt.toLocaleString()}\\n");
    
    return 0;
}`
  downloadFile(cContent, `${sanitizeFileName(note.title)}.c`, "text/plain")
}

// Export as Python (.py)
export function exportAsPython(note: Note): void {
  const plainText = stripHtml(note.content).replace(/\\/g, "\\\\").replace(/"/g, '\\"')
  const pyContent = `#!/usr/bin/env python3
"""
${note.title}
Generated on ${new Date().toLocaleString()}
Original created: ${note.createdAt.toLocaleString()}
"""

def main():
    title = "${note.title}"
    content = """${plainText}"""
    
    print(title)
    print("=" * len(title))
    print()
    print(content)
    print()
    print("---")
    print(f"Created: ${note.createdAt.toLocaleString()}")
    print(f"Last Updated: ${note.updatedAt.toLocaleString()}")

if __name__ == "__main__":
    main()`
  downloadFile(pyContent, `${sanitizeFileName(note.title)}.py`, "text/plain")
}

// Export as JavaScript (.js)
export function exportAsJavaScript(note: Note): void {
  const plainText = stripHtml(note.content).replace(/\\/g, "\\\\").replace(/`/g, "\\`")
  const jsContent = `/**
 * ${note.title}
 * Generated on ${new Date().toLocaleString()}
 * Original created: ${note.createdAt.toLocaleString()}
 */

const noteData = {
    title: "${note.title}",
    content: \`${plainText}\`,
    createdAt: "${note.createdAt.toISOString()}",
    updatedAt: "${note.updatedAt.toISOString()}",
    categories: ${JSON.stringify(note.categories)}
};

function displayNote() {
    console.log(noteData.title);
    console.log("=".repeat(noteData.title.length));
    console.log();
    console.log(noteData.content);
    console.log();
    console.log("---");
    console.log(\`Created: \${new Date(noteData.createdAt).toLocaleString()}\`);
    console.log(\`Last Updated: \${new Date(noteData.updatedAt).toLocaleString()}\`);
}

// Run if in Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    displayNote();
}

// Export for browser/module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = noteData;
}`
  downloadFile(jsContent, `${sanitizeFileName(note.title)}.js`, "application/javascript")
}

// Export as LaTeX (.tex)
export function exportAsLaTeX(note: Note): void {
  const plainText = stripHtml(note.content)
    .replace(/\\/g, "\\textbackslash{}")
    .replace(/[{}]/g, "\\$&")
    .replace(/[#$%&_]/g, "\\$&")
    .replace(/\^/g, "\\textasciicircum{}")
    .replace(/~/g, "\\textasciitilde{}")

  const texContent = `\\documentclass[12pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[margin=1in]{geometry}
\\usepackage{fancyhdr}
\\usepackage{datetime}

\\title{${note.title.replace(/[{}]/g, "\\$&")}}
\\author{Notes App Export}
\\date{${note.createdAt.toLocaleDateString()}}

\\pagestyle{fancy}
\\fancyhf{}
\\rhead{\\thepage}
\\lhead{${note.title.replace(/[{}]/g, "\\$&")}}

\\begin{document}

\\maketitle

\\section*{Content}
${plainText}

\\vfill

\\section*{Metadata}
\\begin{itemize}
    \\item Created: ${note.createdAt.toLocaleString()}
    \\item Last Updated: ${note.updatedAt.toLocaleString()}
    \\item Categories: ${note.categories.join(", ")}
\\end{itemize}

\\end{document}`
  downloadFile(texContent, `${sanitizeFileName(note.title)}.tex`, "application/x-latex")
}

// Export as YAML (.yaml)
export function exportAsYAML(note: Note): void {
  const yamlContent = `---
title: "${note.title}"
id: "${note.id}"
content: |
  ${stripHtml(note.content).split("\n").join("\n  ")}
categories:
${note.categories.map((cat) => `  - "${cat}"`).join("\n")}
metadata:
  created_at: "${note.createdAt.toISOString()}"
  updated_at: "${note.updatedAt.toISOString()}"
  exported_at: "${new Date().toISOString()}"
  word_count: ${
    stripHtml(note.content)
      .split(/\s+/)
      .filter((word) => word.length > 0).length
  }
  character_count: ${stripHtml(note.content).length}
---`
  downloadFile(yamlContent, `${sanitizeFileName(note.title)}.yaml`, "application/x-yaml")
}

// Export as SQL (.sql)
export function exportAsSQL(note: Note): void {
  const plainText = stripHtml(note.content).replace(/'/g, "''")
  const sqlContent = `-- ${note.title}
-- Generated on ${new Date().toLocaleString()}

CREATE TABLE IF NOT EXISTS notes (
    id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    categories TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

INSERT INTO notes (id, title, content, categories, created_at, updated_at) VALUES (
    '${note.id}',
    '${note.title.replace(/'/g, "''")}',
    '${plainText}',
    '${note.categories.join(", ")}',
    '${note.createdAt.toISOString()}',
    '${note.updatedAt.toISOString()}'
);

-- Query to retrieve this note:
-- SELECT * FROM notes WHERE id = '${note.id}';`
  downloadFile(sqlContent, `${sanitizeFileName(note.title)}.sql`, "application/sql")
}

// Helper function to sanitize filename
function sanitizeFileName(filename: string): string {
  return (
    filename
      .replace(/[<>:"/\\|?*]/g, "-")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "")
      .toLowerCase()
      .substring(0, 100) || "untitled"
  )
}

// Helper function to download file with toast notification
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

  // Show toast notification if available
  if (typeof window !== "undefined" && (window as any).showToast) {
    ;(window as any).showToast({
      type: "success",
      title: "File Saved",
      description: `Successfully saved as ${fileName}`,
    })
  }
}

// Export format definitions for UI
export const exportFormats = [
  { name: "Plain Text", extension: "txt", icon: "FileText", action: exportAsText, description: "Simple text format" },
  {
    name: "Markdown",
    extension: "md",
    icon: "FileType",
    action: exportAsMarkdown,
    description: "Markdown format with formatting",
  },
  {
    name: "PDF Document",
    extension: "pdf",
    icon: "FileIcon",
    action: exportAsPDF,
    description: "Portable document format",
  },
  { name: "HTML Web Page", extension: "html", icon: "Globe", action: exportAsHTML, description: "Web page format" },
  { name: "JSON Data", extension: "json", icon: "Braces", action: exportAsJSON, description: "Structured data format" },
  {
    name: "XML Document",
    extension: "xml",
    icon: "Code",
    action: exportAsXML,
    description: "Extensible markup language",
  },
  {
    name: "Rich Text Format",
    extension: "rtf",
    icon: "FileType2",
    action: exportAsRTF,
    description: "Rich text document",
  },
  {
    name: "CSV Spreadsheet",
    extension: "csv",
    icon: "Table",
    action: exportAsCSV,
    description: "Comma-separated values",
  },
  { name: "Assembly Code", extension: "asm", icon: "Cpu", action: exportAsASM, description: "x86 Assembly language" },
  {
    name: "NASM Assembly",
    extension: "nasm",
    icon: "Cpu",
    action: exportAsNASM,
    description: "Netwide Assembler format",
  },
  { name: "C Source Code", extension: "c", icon: "Code2", action: exportAsC, description: "C programming language" },
  {
    name: "Python Script",
    extension: "py",
    icon: "FileCode",
    action: exportAsPython,
    description: "Python programming language",
  },
  {
    name: "JavaScript",
    extension: "js",
    icon: "FileCode2",
    action: exportAsJavaScript,
    description: "JavaScript code",
  },
  {
    name: "LaTeX Document",
    extension: "tex",
    icon: "FileType",
    action: exportAsLaTeX,
    description: "LaTeX typesetting format",
  },
  {
    name: "YAML Config",
    extension: "yaml",
    icon: "Settings",
    action: exportAsYAML,
    description: "YAML configuration format",
  },
  { name: "SQL Database", extension: "sql", icon: "Database", action: exportAsSQL, description: "SQL database script" },
]
