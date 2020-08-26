import sublime, sublime_plugin
import os, re

class ViewBookmarksCommand(sublime_plugin.WindowCommand):
    locations=[]

    def run(self):
        items=[]
        self.locations=[]
        all_files = list(filter(None, map(lambda f : f.file_name(), sublime.active_window().views())))
        common_prefix = os.path.commonprefix(all_files)
        for view in sublime.active_window().views():
            prefix=""
            if view.name():
                prefix=view.name()+":"
            elif view.file_name():
                prefix=view.file_name()+":"
                if prefix.startswith(common_prefix):
                    prefix = prefix[len(common_prefix):]
            for region in view.get_regions("bookmarks"):
                row,_=view.rowcol(region.a)
                line=re.sub('\s+', ' ', view.substr(view.line(region))).strip()
                items.append([prefix+str(row+1), line])
                self.locations.append((view, region))
        if len(items) > 0:
            sublime.active_window().show_quick_panel(items, self.go_there, sublime.MONOSPACE_FONT)
        else:
            sublime.active_window().show_quick_panel(["No bookmarks found"], None, sublime.MONOSPACE_FONT)

    def go_there(self, i):
        if i < 0 or i >= len(self.locations):
            return
        view, region = self.locations[i]
        sublime.active_window().focus_view(view)
        view.show_at_center(region)
        view.sel().clear()
        view.sel().add(region)

