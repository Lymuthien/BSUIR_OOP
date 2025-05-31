# LAB 2

Completed by Kozlova Tatsiana, group 353504

## Functional requirements

The program is a console-based document editor that allows users to create,
edit, format, and save documents.

### Document management

- Create, open, edit, and delete documents. You can create and open only md documents,
  but save it to different types and formats.
- Support different document types (PlainText, Markdown, RichText).
- Save/load documents in various formats (TXT, JSON, XML).

### Text Editing & Formatting

- Insert, delete, and modify text.
- Apply formatting (bold, italic, strikethrough).
- Support copy, cut, and paste operations.

### Undo/Redo System

- Ability to undo/redo text modifications.

### Storage Options

- Store documents in local files, the cloud.

### User Roles & Permissions

- Roles: Viewer (read-only), Editor (edit access), Admin (manage users & permissions)
- Notify users of document changes

### Settings & Customization

- Manage global editor settings (font size)

## Commands

### Document management

To **create**, **open** and **delete** document enter 'c', 'o' or 'd' in the main menu.

While working with document:

- ctrl+s - **Save** document. To save enter filename(path), type, format, and storage.
- ctrl+d - Exit from editing document.

### Text Editing & Formatting

While working with document:

- insert text -> ctrl+b - **Bold** text
- insert text -> ctrl+i - **Italic** text
- insert text -> ctrl+n - **Strikethrough** text
- f1..6 - Set doc style themes
- insert text -> ctrl+c - copy
- ctrl+v - paste
- ctrl+x - cut

### Undo/Redo System

While working with document:

- ctrl+z - undo
- ctrl+y - redo

If you exit from document, you cant restore history.

### User Roles & Permissions

While working with document:

- ctrl+r - Give role. Only admin can manage.

Notifying dont work if document is changed not from program but from storage.

### Settings & Customization

While working with document:

- ctrl+t - Increase **font**
- ctrl+u - Decrease font


