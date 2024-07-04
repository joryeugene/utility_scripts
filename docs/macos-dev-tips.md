# macOS Developer Tips and Tricks

## Vim Tips

### Search Navigation
- After searching with `/`:
  - `n`: Go to next match
  - `N`: Go to previous match
  - `*`: Search for word under cursor (forward)
  - `#`: Search for word under cursor (backward)

### Other Vim Tips
- `:%s/foo/bar/g`: Replace 'foo' with 'bar' globally
- `:.,$s/foo/bar/g`: Replace from current line to end of file
- `Ctrl + v`: Enter visual block mode
- `gd`: Go to definition (in supported file types)
- `:set number`: Show line numbers
- `:set relativenumber`: Show relative line numbers

## macOS Developer Tips

1. Use Homebrew for package management:
   ```
   brew install <package-name>
   ```

2. Enable 'Tab' navigation in modal dialogs:
   System Preferences > Keyboard > Shortcuts > "Use keyboard navigation to move focus between controls"

3. Use Spotlight as a quick calculator:
   Cmd + Space, then type your calculation

4. Quick Look files in Finder:
   Select a file and press Space

5. Take screenshots:
   - Cmd + Shift + 3: Full screen
   - Cmd + Shift + 4: Selected area
   - Cmd + Shift + 5: Screen recording or screenshot options

6. Use Mission Control for window management:
   Ctrl + Up Arrow

7. Use custom Dock spacers:
   ```
   defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="spacer-tile";}' && killall Dock
   ```

## Command Line and Alias Tips

1. Use `z` for quick directory navigation:
   ```
   z project_name
   ```

2. Utilize the `update` alias for system updates:
   ```
   update
   ```

3. Quick edit of config files:
   ```
   zshconfig
   nvimconfig
   ```

4. Git aliases:
   ```
   gst   # git status
   ga    # git add
   gc    # git commit
   gp    # git push
   ```

5. Directory listing:
   ```
   l     # detailed list
   la    # list all, including hidden
   ```

6. Quick Python virtual environment:
   ```
   venv myproject
   activate
   ```

## Claude CLI Environment Management

1. Activate Claude environment:
   ```
   activate_claude
   ```

2. Deactivate Claude environment:
   ```
   deactivate_claude
   ```

3. Switch to system Python:
   ```
   use_system_python
   ```

4. Switch to pyenv-managed Python:
   ```
   use_pyenv
   ```

5. Run Claude CLI with specific options:
   ```
   claude --stream "Your prompt here"
   claude --use-role developer "How to implement authentication in FastAPI?"
   ```

6. Index documents for RAG:
   ```
   claude --index
   ```

7. Set new context path:
   ```
   claude --set-context-path "~/projects/current/docs"
   ```

## Quick Environment Switching

1. Create aliases for different project environments:
   ```
   alias proj1_env='activate_claude && cd ~/projects/project1'
   alias proj2_env='deactivate_claude && use_pyenv && cd ~/projects/project2'
   ```

2. Use iTerm2 profiles for different environments:
   - Create new profiles in iTerm2 preferences
   - Set different working directories and startup commands for each profile

3. Use Visual Studio Code workspaces:
   - Create a workspace file for each project
   - Use the command palette (Cmd + Shift + P) to switch workspaces quickly

4. Utilize tmux for managing multiple environments in one terminal:
   - `Ctrl + b c`: Create a new window
   - `Ctrl + b n`: Move to the next window
   - `Ctrl + b p`: Move to the previous window

Remember to customize these tips and create new aliases or shortcuts based on your specific workflow and needs.
