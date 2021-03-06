import sublime, sublime_plugin
import os, re

class LsBookmarksCommand(sublime_plugin.WindowCommand):
    locations=[]

    def run(self):
        items=[]
        self.locations=[]
        for view in sublime.active_window().views():
            prefix=""
            if view.name():
                prefix=view.name()+":"
            elif view.file_name():
                prefix=os.path.basename(view.file_name())+":"
            for region in view.get_regions("bookmarks"):
                row,_=view.rowcol(region.a)
                line=re.sub('\s+', ' ', view.substr(view.line(region))).strip()
                items.append(prefix+str(row+1)+": "+line)
                self.locations.append((view, region))
        if len(items) > 0:
            sublime.active_window().show_quick_panel(items, self.go_there, sublime.MONOSPACE_FONT)
        else:
            sublime.status_message("No bookmarks found")

    def go_there(self, i):
        if i < 0 or i >= len(self.locations):
            return
        view, region = self.locations[i]
        sublime.active_window().focus_view(view)
        view.show_at_center(region)
        view.sel().clear()
        view.sel().add(region)

class LsBookmarksClearCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.yes_no_cancel_dialog("Clear all bookmarks?") == sublime.DIALOG_YES:
            for view in sublime.active_window().views():
                view.erase_regions("bookmarks");
