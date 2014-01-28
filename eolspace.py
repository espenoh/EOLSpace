from gi.repository import GObject, Gtk, Gedit

ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="EOLSpace_menu" action="EOLSpacing"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class EOLSpace(GObject.Object, Gedit.WindowActivatable):
  __gtype_name__ = "EOLSpace"

  window = GObject.property(type=Gedit.Window)

  def __init__(self):
    GObject.Object.__init__(self)

  def do_activate(self):
    self._insert_menu()
    #pass

  def do_deactivate(self):
    pass

  def do_update_state(self):
    pass

  def _insert_menu(self):
    # Get the Gtk.UIManager
    manager = self.window.get_ui_manager()

    # Create a new action group
    self._action_group = Gtk.ActionGroup("EOLSpacePluginActions")
    self._action_group.add_actions([("EOLSpacing", None, _("Run EOLSpace check"),
                                     None, _("Run EOLSpace check"),
                                     self.mark_spaces_at_end_of_line )])

    # Insert the action group
    manager.insert_action_group(self._action_group, -1)

    # Merge the UI
    self._ui_id = manager.add_ui_from_string(ui_str)

  def do_update_state(self):
    self._action_group.set_sensitive(self.window.get_active_document() != None)

  def mark_spaces_at_end_of_line(self, action):
    doc = self.window.get_active_document()
    cursor_line = doc.get_iter_at_mark(doc.get_insert()).get_line()
    buffer_end = doc.get_end_iter()

    doc.create_tag("RedBG", background_set="True",background="Red")

    for line in range(buffer_end.get_line() + 1):
        line_end = doc.get_iter_at_line(line)
        if not line_end.ends_line():
            line_end.forward_to_line_end()
        itr = line_end.copy()
        while itr.backward_char():
            if (line == cursor_line and
                (itr.compare(doc.get_iter_at_mark(doc.get_insert())) < 0)):
                itr.forward_char()
                break
            if not itr.get_char() in (" ", "\t"):
                itr.forward_char()
                break

        doc.apply_tag_by_name("RedBG", itr, line_end)

