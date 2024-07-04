# NERDTree Usage in Neovim

NERDTree is a file system explorer for Neovim. This section covers how to show hidden files and navigate between the tree and your text efficiently.

## Showing Hidden Files

Hidden files (like `.zshrc`) are now visible by default in NERDTree. If you need to toggle this setting:

1. Open NERDTree in Neovim (Ctrl+n)
2. Press `Shift+i` to toggle hidden files

## Toggling NERDTree

- Use `Ctrl+n` to open or close NERDTree

## Navigating Between NERDTree and Text

- Use `Ctrl+w w` to switch focus between NERDTree and your text buffer
- Alternatively, you can use `Ctrl+w h` to move left and `Ctrl+w l` to move right

## Other Useful NERDTree Commands

- `o`: Open files, directories and bookmarks
- `go`: Open selected file, but leave cursor in the NERDTree
- `t`: Open selected node/file in a new tab
- `T`: Open selected node/file in a new tab silently
- `i`: Open selected file in a split window
- `gi`: Open selected file in a split window, but leave cursor in the NERDTree
- `s`: Open selected file in a vertical split
- `gs`: Open selected file in a vertical split, but leave cursor in the NERDTree
- `x`: Close the current nodes parent
- `X`: Recursively close all children of the current node
- `P`: Jump to the root node
- `p`: Jump to current nodes parent
- `K`: Jump up inside directories at the current tree depth
- `J`: Jump down inside directories at the current tree depth
- `<C-J>`: Jump down to next sibling of the current directory
- `<C-K>`: Jump up to previous sibling of the current directory
- `R`: Recursively refresh the current directory
- `f`: Enter file filter mode
- `F`: Toggle file filters
- `B`: Toggle bookmark table

Remember, you can always type `?` in NERDTree to see the full list of available commands.
