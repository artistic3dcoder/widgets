"""Module for commonly used gui elements."""

# EXTERNAL
from typing import Union, Callable, Dict, List, Self, Tuple, Optional
from PySide2 import QtCore
from PySide2.QtGui import (QIcon, QPixmap)
from PySide2.QtWidgets import (QWidget, QFrame, QMessageBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSlider,
                               QComboBox, QGroupBox, QCheckBox, QSpacerItem, QPushButton, QSizePolicy, QSpinBox,
                               QLayout)

# INTERNAL
from messaging import (Failure, Success, Logger)


class GuiElements(QWidget):
    _log = Logger()

    @classmethod
    def horizontal_spacer(cls, line_width: int = 8) -> QFrame:
        """Construct and return a horizontal spacer item."""
        item = QFrame()
        item.setFrameStyle(QFrame.HLine)
        item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        item.setLineWidth(line_width)
        return item

    @classmethod
    def prompt_question(cls, text: str = None, informative_text: str = None, default_yes: bool = False,
                        multi_prompt: bool = False) -> Union[QMessageBox.Yes, QMessageBox.No, QMessageBox.YesToAll, QMessageBox.NoToAll]:
        """Prompts user with a yes/no question.

        Example:
            import gui_elements as ge

            # EXAMPLE OF MUTLI PROMPT. THIS WOULD BE USED WHEN YOU WANT THE RESULT TO OF THE PROMPT TO BE APPLIED
            # OVER AN ITERATIVE PROCESS SO YOU DO NOT HAVE TO KEEP PROMPTING THE USER.
            txt = "Remove element?"
            info = "Remove this item from the group? If No, " \
                   "the item will not be added to the new group."
            result = ge.GuiElements.prompt_question(text=txt, informative_text=info, multi_prompt=True)
            # NOW THAT WE HAVE THE RESULT, DETERMINE THE CHECK STATE
            _multi_true = True if result == QMessageBox.YesToAll else False
            _multi_false = True if result == QMessageBox.NoToAll else False
            _yes = True if result == QMessageBox.Yes else False
            _no = True if result == QMessageBox.No else False

            # EXAMPLE OF SINGLE PROMPT, THIS IS FOR A STRAIGHT YES NO QUESTION
            result = ge.GuiElements.prompt_question(text=txt, informative_text=info, multi_prompt=False)
            # NOW THAT WE HAVE THE RESULT, DETERMINE THE CHECK STATE
            _yes = True if result == QMessageBox.Yes else False
            _no = True if result == QMessageBox.No else False
        """
        question_box = QMessageBox()
        question_box.setText(text)
        question_box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        question_box.setInformativeText(informative_text)
        question_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if multi_prompt:
            question_box.setStandardButtons(
                QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.NoToAll)
        if default_yes:
            question_box.setDefaultButton(QMessageBox.Yes)
        else:
            question_box.setDefaultButton(QMessageBox.No)
        result = question_box.exec_()
        return result

    @classmethod
    def message_box(cls, message: str = None, ok_cancel_option: bool = False) -> bool:
        """Create a message box that is always on top.

        Args:
            message: message to convey to user.
            yes_no_option: when True, provide the user with an Ok, Cancel option.

        Example:
            import gui_elements as ge

            # EXAMPLE OF MUTLI PROMPT. THIS WOULD BE USED WHEN YOU WANT THE RESULT TO OF THE PROMPT TO BE APPLIED
            # OVER AN ITERATIVE PROCESS SO YOU DO NOT HAVE TO KEEP PROMPTING THE USER.
            text = "You Did it."
            ge.GuiElements.message_box(message=text)
        """

        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if ok_cancel_option:
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msgBox.exec_()
        if ret == QMessageBox.Ok:
            return True
        else:
            return False

    @classmethod
    def multi_input_dialog(cls, parent: QWidget = None, title: str = 'Multiple Input Dialog Box', header: str = None,
                           data: Dict = None, yes_label: str = 'Yes', no_label: str = 'No',
                           yes_callback: Callable = None, no_callback: Callable = None) -> List:
        """Create a multi prompt popup window allowing the calling code to query data from the user.

        Args:
            title: title of window
            header: short description to relay to the end user. This is placed at the top of the prompt
            yes_label: Alternate text than using the default 'Yes'
            no_label: Alternate text than using the default 'No'
            data: This is a dictionary where each entry in the dictionary is a dictionary describing a single
                         item in the multi input dialog.
                         REQUIRED options supported  in each entry:
                             'type' (data_type): str, int, float, list
                             'default' (default data_type value): the default value
                             'help' (str): popup help information
                             'items' (list): list type ONLY, items to display in the list
                             'label' (str): label for item
            yes_callback: method to call when yes button is pressed
            no_callback: method to call when no button is pressed (OPTIONAL)

        Example:
            from gui_elements import GuiElements

            _title = 'my dialog title'
            _header = 'example header'
            _yes = 'Yes Please'
            _no = 'No Thanks'

            str_options = {'type': str, 'default': 'a default string', 'help': 'help associated with the str'}
            int_options = {'type': int, 'default': 42, 'min':0, 'max':100, 'help': 'help associated with the int'}
            float_options = {'type': float,'default': 3.214, 'min':0.0, 'max':100.0,'help': 'help associated with the float'}
            multi_options = {'type': list, 'default': 'x', 'items': ['a','b','c','x','y','z'], 'help': 'help associated with the list'}

            _data = {'str label': str_options,
                     'int label': int_options,
                     'float label': float_options,
                     'multi choice': multi_options}

            result = GuiElements.multi_input_dialog(title=_title, header=_header, yes_label=_yes, no_label=_no, data=_data)
        """
        widget = QWidget(parent)
        layout = QVBoxLayout()
        header_widget = QLabel(header)
        layout.addWidget(header_widget)

        hbox = QHBoxLayout()
        label = QLabel(data['label'])
        if 'type' in data:
            item = None
            if data['type'] == str:
                item = QLineEdit()
            elif data['type'] == float:
                item = DoubleSlider()
            elif data['type'] == int:
                item = QSlider()
            elif data['type'] == list:
                item = QComboBox()

            if item:
                # SET MIN MAX VALUES FOR SLIDERS
                if data['type'] == float or data['type'] == int:
                    if 'min' in data or 'max' in data:
                        if 'min' in data:
                            item.setMinimum(data['min'])
                        if 'max' in data:
                            item.setMaximum(data['max'])
                # POPULATE LIST
                if 'items' in data and data['type'] == list:
                    for list_item in data['items']:
                        item.addItem(str(list_item))
                # SET DEFAULTS
                if 'default' in data:
                    if data['type'] == str:
                        item.setText(data['default'])
                    elif data['type'] == float or data['type'] == int:
                        item.setValue(data['default'])
                    elif data['type'] == list:
                        if data['default'] in data['items']:
                            item.setCurrentIndex(data['items'].index(data['default']))

                if 'help' in data:
                    item.setToolTip(data['help'])
            hbox.addWidget(label)
            hbox.addWidget(item)
            widget.item = item
            layout.addLayout(hbox)

        # ADD YES NOT BUTTONS
        hbox_buttons = QHBoxLayout()
        yes = QPushButton(yes_label)
        no = QPushButton(no_label)
        if no_callback:
            no.pressed.connect(lambda: no_callback())
        no.pressed.connect(widget.close)
        yes.pressed.connect(lambda: yes_callback())
        hbox_buttons.addWidget(yes)
        hbox_buttons.addWidget(no)
        layout.addLayout(hbox_buttons)

        widget.setLayout(layout)

        return widget


class DoubleSlider(QSlider):
    """A QSlider with a double value."""
    def __init__(self, *args, **kwargs) -> None:
        QSlider.__init__(self, *args, **kwargs)

        # Set integer max and min. These stay constant.
        self.setMinimum(0)
        self._max_int = 10000
        self.setMaximum(self._max_int)

        # The "actual" min and max values seen by user
        self._min_value = 0.0
        self._max_value = 100.0

    @property
    def _value_range(self) -> float:
        """Return value range of slider."""
        return self._max_value - self._min_value

    def setMinimum(self, value: float) -> None:
        """Set range of slider."""
        self.setRange(value, self._max_value)

    def setMaximum(self, value: float) -> None:
        """Set max of slider."""
        self.setRange(self._min_value, value)

    def setRange(self, minimum: float, maximum: float) -> None:
        """Set range of slider."""
        old_value = self.value()
        self._min_value = minimum
        self._max_value = maximum
        self.setValue(old_value)

    def value(self) -> float:
        """Return value of slider."""
        return float(self.value()) / self._max_int * self._value_range

    def setValue(self, value: float) -> None:
        """Set value of slider."""
        self.setValue(int(value / self._value_range * self._max_int))

    def proportion(self) -> float:
        """Return proportion of slider."""
        return (self.value() - self._min_value) / self._value_range


class Group(QGroupBox):
    """A collapsible group box."""
    def __init__(self, title: str, minus_icon: str, plus_icon: str, v_orient: bool = True, init_visible: bool = False,
                 label: str = None, align_label_left: bool = False, button_style: str = None, text_style: str = None,
                 parent: QLayout = None) -> None:
        """
        Initialization method for Group
        Args:
            parent: Parent container
            title: title for Group
            v_orient: vertically orient content.
            init_visible: initialize the contents of the Group as visible or hidden
            label: if supplied apply this label next to the toggle button
            button_style: style sheet to apply to collapse buttons
            text_style: style sheet to apply to informational text
            minus_icon: icon path for minus.
            plus_icon: icon path for plus.
        """
        QGroupBox.__init__(self, parent)
        self._insert = "{0}.{1}.".format(self.__module__, self.__class__.__name__)
        self._log = Logger()

        self.CHECKBOX_ICON = QIcon()
        self.CHECKBOX_ICON.addPixmap(QPixmap("{0}".format(minus_icon)), QIcon.Normal, QIcon.Off)
        self.CHECKBOX_ICON.addPixmap(QPixmap("{0}".format(plus_icon)), QIcon.Normal, QIcon.On)

        if parent:
            self.parent = parent

        if title:
            self.setTitle(title)

        self._main_container = QVBoxLayout(self)
        self._main_container.setContentsMargins(3, 3, 3, 3)

        hbox_collapse_option = QHBoxLayout()
        hbox_collapse_option.setAlignment(QtCore.Qt.AlignRight)
        hbox_collapse_option.setSpacing(0)
        hbox_collapse_option.setContentsMargins(0, 0, 0, 0)
        if label:
            self.label = QLabel(label)
        else:
            self.label = QLabel("")
        if text_style:
            self.label.setStyleSheet(text_style)

        self.toggle_button = QPushButton("")
        self.toggle_button.toggled.connect(self.collapse_widgets)
        self.toggle_button.setIcon(self.CHECKBOX_ICON)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setFlat(True)
        self.toggle_button.setDefault(False)
        if button_style:
            self.toggle_button.setStyleSheet(button_style)
        else:
            self.toggle_button.setStyleSheet("QPushButton {border: none;}")

        hbox_collapse_option.addWidget(self.label)
        if align_label_left:
            hbox_collapse_option.addStretch(1)
        hbox_collapse_option.addWidget(self.toggle_button)
        self._main_container.addLayout(hbox_collapse_option)

        self._main_widget_container = QWidget()

        self._main_widget_container.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        style = "icon-size: 20px;" \
                "background-color: rgb(54, 54, 54);"
        self._main_widget_container.setStyleSheet(style)

        self._main_widget_container.setMinimumHeight(25)
        self._main_container.addWidget(self._main_widget_container)
        if v_orient:
            self._widget_container = QVBoxLayout()
        else:
            self._widget_container = QHBoxLayout()
        self._widget_container.setAlignment(QtCore.Qt.AlignLeft)
        self._widget_container.setContentsMargins(3, 3, 3, 3)

        self._main_widget_container.setLayout(self._widget_container)

        self._main_container.addStretch(1)
        self._main_widget_container.setVisible(init_visible)

        self.setFixedHeight(self.sizeHint().height())

    @property
    def group_box(self) -> Self:
        """Return the group box."""
        return self

    @property
    def main_container(self) -> QLayout:
        """Return main container."""
        return self._main_container

    @property
    def main_widget_container(self) -> QWidget:
        """Return main widget container."""
        return self._main_widget_container

    @property
    def widget_container(self) -> QLayout:
        """Return widget container."""
        return self._widget_container

    def add_layout(self, layout: QLayout) -> Union[Success, Failure]:
        """Add layouts to the classes widget container.

        Args:
            layout: layout to insert.
        """
        if layout:
            self._widget_container.addLayout(layout)
            return Success()
        else:
            msg = "{0}add_layout(): layout Argument missing".format(self._insert)
            self._log.error(msg)
            return Failure(msg)

    def add_widget(self, widget: QWidget) -> Union[Success, Failure]:
        """Add widgets to the classes widget container.

        Args:
            widget: widget to insert
        """
        if widget:
            self._widget_container.addWidget(widget)
            return Success()
        else:
            msg = "{0}add_widget(): widget Argument missing".format(self._insert)
            self._log.error(msg)
            return Failure(msg)

    def collapse_widgets(self, state: bool) -> None:
        """
        private method used to collapse the shelves
        Args:
            state: collapse state of widget
        """
        # IF SINGLE RETURNS FALSE, HIDE BUTTONS
        if not state:
            self._main_widget_container.setVisible(False)
            self.toggle_button.setChecked(False)
        else:
            self._main_widget_container.setVisible(True)
            self.toggle_button.setChecked(True)
        self.setFixedHeight(self.sizeHint().height())

    def set_title(self, title: str = None) -> Union[Success, Failure]:
        """Set title of group box.

        Args:
            title: title of group box.
        """
        if title:
            self.setTitle(title)
            return Success()
        else:
            msg = "{0}set_title(): title Argument missing".format(self._insert)
            self._log.error(msg)
            return Failure(msg)

    def set_label(self, label: str = None) -> Union[Success, Failure]:
        """Set label text for interior label item.

        Args:
            label: text to apply to label.
        """
        if label or label == '':
            self.label.setText(label)
            return Success()
        else:
            msg = "{0}set_label(): label Argument missing".format(self._insert)
            self._log.error(msg)
            return Failure(msg)


class GenericCheckBoxField(QWidget):
    """Create a Value Widget Which represents a checkbox."""

    def __init__(self, parent: QWidget = None, title: str = None) -> None:
        QWidget.__init__(self, parent)

        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        self.check_box = QCheckBox(title)
        container.addSpacerItem(QSpacerItem(25, 25))
        container.addWidget(self.check_box)
        container.addStretch(1)
        self.setLayout(container)


class GenericDropDownField(QWidget):
    """DropDown Field is a Field Title / Value Widget Which represents a combobox."""

    def __init__(self, title: str, options: List[str], title_width: int = 200, parent=None) -> None:
        QWidget.__init__(self, parent)

        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("<b>{0}</b>:".format(title))
        self.title.setMinimumWidth(title_width)
        self.title.setMaximumWidth(title_width)
        self.value = QComboBox()
        self.value.setStyleSheet('background: gray; selection-background-color: darkgray; border-radius: 7px;')
        self.value.addItems(options)
        self.value.setMinimumWidth(300)
        container.addSpacerItem(QSpacerItem(25, 25))
        container.addWidget(self.title)
        container.addSpacerItem(QSpacerItem(25, 25))
        container.addWidget(self.value)
        container.addStretch(1)
        self.setLayout(container)


class GenericTextField(QHBoxLayout):
    """Creates a generic text field."""
    def __init__(self, parent, label, double_it=False, title1_width: int = 120, title2_width: int = 140,
                 value1_width: int = 200, value2_width: int = 200) -> None:
        QHBoxLayout.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        style = 'background: gray; selection-background-color: darkgray; border-radius: 7px;'

        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        self.addLayout(wrapper)
        self.title1 = QLabel("<b>{0}</b>".format(label[0]))

        self.title1.setMinimumWidth(title1_width)
        self.title1.setMaximumWidth(title1_width)
        self.value1 = QLineEdit('')
        self.value1.setStyleSheet(style)
        self.value1.setMinimumWidth(value1_width)
        self.value1.setMaximumWidth(value1_width)
        wrapper.addSpacerItem(QSpacerItem(25, 15))
        wrapper.addWidget(self.title1)
        wrapper.addWidget(self.value1)
        if double_it:
            self.title2 = QLabel("<b>{0}</b>".format(label[1]))
            self.title2.setMinimumWidth(title2_width)
            self.title2.setMaximumWidth(title2_width)
            self.value2 = QLineEdit('')
            self.value2.setStyleSheet(style)
            self.value2.setMinimumWidth(value2_width)
            wrapper.addSpacerItem(QSpacerItem(25, 25))
            wrapper.addWidget(self.title2)
            wrapper.addWidget(self.value2)

        self.addStretch(1)


class GenericLineEditField(QHBoxLayout):
    """Create a Widget which provides a title and a value."""

    def __init__(self, title: str, title_width: int = 200, default_value: str = "", value_width: int = 300,
                 parent=None) -> None:
        QHBoxLayout.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        style = 'background: gray; selection-background-color: darkgray; border-radius: 7px;'

        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        self.addLayout(wrapper)
        self.title = QLabel("<b>{0}</b>:".format(title))
        self.title.setMinimumWidth(title_width)
        self.title.setMaximumWidth(title_width)
        # self.title.setStyleSheet('color: #07080a;font-size:9pt')
        self.value = QLineEdit(default_value)
        self.value.setStyleSheet('background: gray; selection-background-color: darkgray; border-radius: 7px;')

        self.value.setMinimumWidth(value_width)
        self.value.setMaximumWidth(value_width)
        wrapper.addSpacerItem(QSpacerItem(25, 25))
        wrapper.addWidget(self.title)
        wrapper.addSpacerItem(QSpacerItem(25, 25))
        wrapper.addWidget(self.value)
        wrapper.addStretch(1)


class ComboBoxTextField(QHBoxLayout):
    """Create a combo box with a text field."""
    def __init__(self, label1: str, label2: str = None, title_width: int = 120, title_width2: int = 140,
                 combo_items: List[str] = None, size_value1: int = 200, size_value2: int = 200, double_it=False,
                 parent: QWidget = None):
        QHBoxLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        style = 'background: gray; selection-background-color: darkgray; border-radius: 7px;'

        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        self.addLayout(wrapper)
        self.title1 = QLabel("<b>{0}</b>".format(label1))

        self.title1.setMinimumWidth(title_width)
        self.title1.setMaximumWidth(title_width)
        self.value1 = QComboBox()
        self.value1.addItems(sorted(combo_items))
        self.value1.setStyleSheet(style)
        self.value1.setMinimumWidth(size_value1)
        self.value1.setMaximumWidth(size_value1)
        wrapper.addSpacerItem(QSpacerItem(25, 15))
        wrapper.addWidget(self.title1)
        wrapper.addWidget(self.value1)
        if double_it:
            self.title2 = QLabel("<b>{0}</b>".format(label2))
            self.title2.setMinimumWidth(title_width2)
            self.title2.setMaximumWidth(title_width2)
            self.value2 = QLineEdit('')
            self.value2.setStyleSheet(style)
            self.value2.setMinimumWidth(size_value2)
            wrapper.addSpacerItem(QSpacerItem(25, 25))
            wrapper.addWidget(self.title2)
            wrapper.addWidget(self.value2)

        self.addStretch(1)


class SpinBoxField(QHBoxLayout):
    """Create a spin box field."""
    def __init__(self, label1: str, label2: str = "", title_width1: int = 120, title_width2: int = 120,
                 spacer_width: int = 25, value1_width: int = 200, value2_width: int = 200, double_it=False,
                 parent: QWidget=None) -> None:
        QHBoxLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        style = 'background: gray; selection-background-color: darkgray; border-radius: 7px;'

        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        self.addLayout(wrapper)
        self.title1 = QLabel("<b>{0}</b>".format(label1))
        t1w = title_width1
        t2w = title_width2

        self.title1.setMinimumWidth(t1w)
        self.title1.setMaximumWidth(t1w)
        self.value1 = QSpinBox()
        self.value1.setStyleSheet(style)
        self.value1.setMinimumWidth(value1_width)
        self.value1.setMaximumWidth(value1_width)
        wrapper.addSpacerItem(QSpacerItem(spacer_width, 15))
        wrapper.addWidget(self.title1)
        wrapper.addWidget(self.value1)
        if double_it:
            self.title2 = QLabel("<b>{0}</b>".format(label2))
            self.title2.setMinimumWidth(t2w)
            self.title2.setMaximumWidth(t2w)
            self.value2 = QSpinBox()
            self.value2.setStyleSheet(style)
            self.value2.setMinimumWidth(value2_width)
            wrapper.addSpacerItem(QSpacerItem(spacer_width, 25))
            wrapper.addWidget(self.title2)
            wrapper.addWidget(self.value2)

        self.addStretch(1)


class AddRemoveBlock(QWidget):
    """Create a widget with a Label and a + -  Option.

    Notes:
        The + - options execute an incoming add_callback and remove_callback to control the
        adding and removal of the AddRemoveBlock Widget.
    
    Example:
        def _add_new_item(self, index):
            '''Private method used to add a new item object.
            Args:
                index (int): index of new item
            Returns:
                 None
            '''
            while index in self._items:
                index += 1
            self._items[index] = ExpandableItem(parent=self, index=index,
                                                    add_callback=self._add_new_item,
                                                    remove_callback=self._remove_an_item)
            self.item_container.addWidget(self._items[index])

        def _remove_an_item(self, index):
            '''Private method used to remove a item from the item list.
            Args:
                index (int): index of item to remove
            ''
            if len(self._items) > 1:
                self._items[index].deleteLater()
                del self._items[index]
    """

    def __init__(self, title: str, index: int, add_callback: Callable, remove_callback: Callable,
                 set_bg_color: bool = False, background_color: Tuple = None, parent: QWidget = None) -> None:
        QWidget.__init__(self, parent)
        if set_bg_color:
            if not background_color:
                self.setStyleSheet('background-color:#959da5')
            else:
                self.setStyleSheet('background-color:{0}'.format(background_color))
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.autoFillBackground()
        self.title_widget = None
        self.title = title
        self.index = index
        self.add_callback = add_callback
        self.remove_callback = remove_callback
        self.wrapper = QVBoxLayout()
        self.wrapper.setContentsMargins(0, 0, 0, 0)
        self.v_container = QVBoxLayout()
        self._add_container()
        self.setLayout(self.wrapper)

    def _add_container(self, index: int = 1) -> None:
        """Add a container to the widget.

        Args:
            index: index of field
        """

        self.v_container.setContentsMargins(0, 0, 0, 0)
        self.v_container.index = index
        container = QHBoxLayout()
        self.v_container.addLayout(container)
        container.setContentsMargins(0, 0, 0, 0)
        container.index = index
        # ADD HEADER
        h_title_container = QHBoxLayout()
        h_title_container.setContentsMargins(0, 0, 0, 0)
        h_title_container.addSpacerItem(QSpacerItem(25, 25))
        self.title_widget = QLabel("<b>{0}</b>:".format(self.title))
        self.title_widget.setStyleSheet('color: #382500;font-size:10pt')
        self.title_widget.setMinimumWidth(200)
        self.title_widget.setMaximumWidth(200)
        h_title_container.addWidget(self.title_widget)
        h_title_container.addSpacerItem(QSpacerItem(50, 25))
        h_title_container.addStretch(1)
        self.more_btn = QPushButton('+')
        self.more_btn.setFlat(True)
        self.more_btn.setStyleSheet('color: #132333;font-size:16pt; font-style:bold')
        self.more_btn.setMaximumWidth(35)
        self.more_btn.setMaximumHeight(35)
        self.more_btn.setMinimumWidth(35)
        self.more_btn.setMinimumHeight(35)
        self.more_btn.index = index
        self.more_btn.clicked.connect(lambda: self.add_callback(index=self.index + 1))
        h_title_container.addWidget(self.more_btn)
        h_title_container.addSpacerItem(QSpacerItem(15, 15))
        self.less_btn = QPushButton('x')
        self.less_btn.setFlat(True)
        self.less_btn.setStyleSheet('color: #132333;font-size:16pt; font-style:bold')
        self.less_btn.type = 'sequence'
        self.less_btn.setMaximumWidth(35)
        self.less_btn.setMaximumHeight(35)
        self.less_btn.setMinimumWidth(35)
        self.less_btn.setMinimumHeight(35)
        self.less_btn.index = index
        self.less_btn.clicked.connect(lambda: self.remove_callback(index=self.index))
        h_title_container.addWidget(self.less_btn)
        h_title_container.addSpacerItem(QSpacerItem(50, 25))
        self.v_container.addSpacerItem(QSpacerItem(10, 10))
        self.v_container.addLayout(h_title_container)
        self._add_options()
        self.v_container.addSpacerItem(QSpacerItem(10, 20))
        self.wrapper.addLayout(self.v_container)

    def _remove_container(self, index: int, container: QWidget) -> None:
        """Remove a container.

        Args:
            index: index of container to remove.
        """
        # REMOVE FROM VALUES TRACKER

        # CLEAN CONTAINER
        # REMOVE THE EXISTING ITEMS FROM THE ATTRIBUTE DATA SECTION
        for i in reversed(range(container.count())):
            widget = container.itemAt(i).widget()
            if widget:
                container.itemAt(i).widget().setParent(None)
        child = container.takeAt(0)
        while child:
            del child
            child = container.takeAt(0)
        self.remove_callback(index=index)


class FrameBoxWidget(QFrame):
    """Create a simple QFrame Widget with a default 1 px border with a 5 px radius

    Example:
        # MAKE OVER ARCHING CONTAINER
        vbox = QVBoxLayout()
        # INSTANCE THE FRAMEBOX
        frame = FrameBoxWidget()
        # CREATEE A LAYOUT FOR THE FRAMEBOX
        layout = QVBoxLayout(frame)
        # CREATE A FEW WIDGETS AND ADD TO THE FRAMEBOX'S LAYOUT
        widget_a = QLineEdit("test 1")
        widget_b = QLineEdit("test 2")
        layout.addWidget(widget_a)
        layout.addWidget(widget_b)
        # ADD THE WIDGET TO THE OVER ARCHING LAYOUT
        vbox.addWidget(frame)

    """

    def __init__(self, minimum_width: Optional[int] = 200, minimum_height: Optional[int] = 35,
                 style_sheet: Optional[str] = None, parent: QWidget = None) -> None:
        """
        init method used to create a QFrame for overrides
        Args:
            minimum_height: Minimum height of frame
            minimum_width: Minimum width of frame
            style_sheet: Style sheet for frame
        """
        QFrame.__init__(self, parent)
        style = "QFrame{border: 1px solid gray; border-radius: 5px;background-color: none;}"
        if style_sheet:
            style = style_sheet

        self.setMinimumWidth(minimum_width)
        self.setMinimumHeight(minimum_height)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(style)
